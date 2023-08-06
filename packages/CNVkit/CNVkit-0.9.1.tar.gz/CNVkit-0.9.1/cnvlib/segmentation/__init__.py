"""Segmentation of copy number values."""
from __future__ import absolute_import, division, print_function
from builtins import map

import locale
import logging
import math
import os.path
import tempfile

import numpy as np
import pandas as pd
from Bio._py3k import StringIO
from skgenome import tabio

from .. import core, parallel, params, smoothing, vary
from ..cnary import CopyNumArray as CNA
from . import cbs, flasso, haar, none


def do_segmentation(cnarr, method, threshold=None, variants=None,
                    skip_low=False, skip_outliers=10, min_weight=0,
                    save_dataframe=False, rlibpath=None,
                    processes=1):
    """Infer copy number segments from the given coverage table."""
    if variants:
        variants = variants.heterozygous()
    if not threshold:
        threshold = {'cbs': 0.0001,
                     'flasso': 0.005,
                     'haar': 0.001,
                     'none': np.nan,
                    }[method]
    logging.info("Segmenting with method '%s', significance threshold %g, "
                 "in %s processes", method, threshold, processes)

    # NB: parallel cghFLasso segfaults in R ('memory not mapped'),
    # even when run on a single chromosome
    if method == 'flasso':
        # ENH segment p/q arms separately
        # -> assign separate identifiers via chrom name suffix?
        cna = _do_segmentation(cnarr, method, threshold, variants, skip_low,
                               skip_outliers, min_weight, save_dataframe, rlibpath)
        if save_dataframe:
            cna, rstr = cna
            rstr = _to_str(rstr)

    else:
        with parallel.pick_pool(processes) as pool:
            rets = list(pool.map(_ds, ((ca, method, threshold, variants,
                                        skip_low, skip_outliers, min_weight,
                                        save_dataframe, rlibpath)
                                       for _, ca in cnarr.by_arm())))
        if save_dataframe:
            # rets is a list of (CNA, R dataframe string) -- unpack
            rets, r_dframe_strings = zip(*rets)
            # Strip the header line from all but the first dataframe, then combine
            r_dframe_strings = map(_to_str, r_dframe_strings)
            rstr = [next(r_dframe_strings)]
            rstr.extend(r[r.index('\n') + 1:] for r in r_dframe_strings)
            rstr = "".join(rstr)
        cna = cnarr.concat(rets)

    if save_dataframe:
        return cna, rstr
    return cna


def _to_str(s, enc=locale.getpreferredencoding()):
    if isinstance(s, bytes):
        return s.decode(enc)
    return s


def _ds(args):
    """Wrapper for parallel map"""
    return _do_segmentation(*args)


def _do_segmentation(cnarr, method, threshold, variants=None,
                     skip_low=False, skip_outliers=10, min_weight=0,
                     save_dataframe=False, rlibpath=None):
    """Infer copy number segments from the given coverage table."""
    if not len(cnarr):
        return cnarr

    filtered_cn = cnarr.copy()
    # Filter out bins with no or near-zero sequencing coverage
    if skip_low:
        filtered_cn = filtered_cn.drop_low_coverage(verbose=False)
    # Filter by distance from rolling quantiles
    if skip_outliers:
        filtered_cn = drop_outliers(filtered_cn, 50, skip_outliers)
    # Filter by bin weights
    if min_weight:
        weight_too_low = (filtered_cn["weight"] < min_weight).fillna(True)
    else:
        weight_too_low = (filtered_cn["weight"] == 0).fillna(True)
    n_weight_too_low = weight_too_low.sum() if len(weight_too_low) else 0
    if n_weight_too_low:
        filtered_cn = filtered_cn[~weight_too_low]
        if min_weight:
            logging.debug("Dropped %d bins with weight below %s",
                          n_weight_too_low, min_weight)
        else:
            logging.debug("Dropped %d bins with zero weight",
                          n_weight_too_low)

    if len(filtered_cn) != len(cnarr):
        logging.info("Dropped %d / %d bins on chromosome %s",
                     len(cnarr) - len(filtered_cn),
                     len(cnarr), cnarr["chromosome"].iat[0])
    if not len(filtered_cn):
        return filtered_cn

    seg_out = ""
    if method == 'haar':
        segarr = haar.segment_haar(filtered_cn, threshold)

    elif method == 'none':
        segarr = none.segment_none(filtered_cn)

    elif method in ('cbs', 'flasso'):
        # Run R scripts to calculate copy number segments
        rscript = {'cbs': cbs.CBS_RSCRIPT,
                   'flasso': flasso.FLASSO_RSCRIPT,
                  }[method]

        filtered_cn['start'] += 1  # Convert to 1-indexed coordinates for R
        with tempfile.NamedTemporaryFile(suffix='.cnr', mode="w+t") as tmp:
            filtered_cn.data.to_csv(tmp, index=False, sep='\t',
                                    float_format='%.6g', mode="w+t")
            tmp.flush()
            script_strings = {
                'probes_fname': tmp.name,
                'sample_id': cnarr.sample_id,
                'threshold': threshold,
                'rlibpath': ('.libPaths(c("%s"))' % rlibpath if rlibpath else ''),
            }
            with core.temp_write_text(rscript % script_strings,
                                      mode='w+t') as script_fname:
                seg_out = core.call_quiet('Rscript', '--vanilla', script_fname)
        # Convert R dataframe contents (SEG) to a proper CopyNumArray
        # NB: Automatically shifts 'start' back from 1- to 0-indexed
        segarr = tabio.read(StringIO(seg_out.decode()), "seg", into=CNA)
        if method == 'flasso':
            segarr = squash_segments(segarr)
        segarr = repair_segments(segarr, cnarr)

    else:
        raise ValueError("Unknown method %r" % method)

    segarr.meta = cnarr.meta.copy()
    if variants:
        # Re-segment the variant allele freqs within each segment
        newsegs = [haar.variants_in_segment(subvarr, segment, 0.01 * threshold)
                   for segment, subvarr in variants.by_ranges(segarr)]
        segarr = segarr.as_dataframe(pd.concat(newsegs))
        segarr['baf'] = variants.baf_by_ranges(segarr)

    segarr['gene'], segarr['weight'], segarr['depth'] = \
            transfer_fields(segarr, cnarr)
    segarr.sort_columns()
    if save_dataframe:
        return segarr, seg_out
    else:
        return segarr


def drop_outliers(cnarr, width, factor):
    """Drop outlier bins with log2 ratios too far from the trend line.

    Outliers are the log2 values `factor` times the 90th quantile of absolute
    deviations from the rolling average, within a window of given `width`. The
    90th quantile is about 1.97 standard deviations if the log2 values are
    Gaussian, so this is similar to calling outliers `factor` * 1.97 standard
    deviations from the rolling mean. For a window size of 50, the breakdown
    point is 2.5 outliers within a window, which is plenty robust for our needs.
    """
    if not len(cnarr):
        return cnarr
    outlier_mask = np.concatenate([
        smoothing.rolling_outlier_quantile(subarr['log2'], width, .95, factor)
        for _chrom, subarr in cnarr.by_chromosome()])
    n_outliers = outlier_mask.sum()
    if n_outliers:
        logging.info("Dropped %d outlier bins:\n%s%s",
                     n_outliers,
                     cnarr[outlier_mask].data.head(20),
                     "\n..." if n_outliers > 20 else "")
    return cnarr[~outlier_mask]


def transfer_fields(segments, cnarr, ignore=params.IGNORE_GENE_NAMES):
    """Map gene names, weights, depths from `cnarr` bins to `segarr` segments.

    Segment gene name is the comma-separated list of bin gene names. Segment
    weight is the sum of bin weights, and depth is the (weighted) mean of bin
    depths.
    """
    if not len(cnarr):
        return [], [], []

    ignore += params.ANTITARGET_ALIASES
    if 'weight' not in cnarr:
        cnarr['weight'] = 1
    if 'depth' not in cnarr:
        cnarr['depth'] = np.exp2(cnarr['log2'])
    seggenes = ['-'] * len(segments)
    segweights = np.zeros(len(segments))
    segdepths = np.zeros(len(segments))
    for i, (_seg, subprobes) in enumerate(cnarr.by_ranges(segments)):
        if not len(subprobes):
            continue
        segweights[i] = subprobes['weight'].sum()
        if subprobes['weight'].sum() > 0:
            segdepths[i] = np.average(subprobes['depth'], weights=subprobes['weight'])
        subgenes = [g for g in pd.unique(subprobes['gene']) if g not in ignore]
        if subgenes:
            seggenes[i] = ",".join(subgenes)
    return seggenes, segweights, segdepths


def squash_segments(segments):
    """Combine contiguous segments."""
    curr_chrom = None
    curr_start = None
    curr_end = None
    curr_genes = []
    curr_log2 = None
    curr_probes = 0
    squashed_rows = []
    for row in segments:
        if row.chromosome == curr_chrom and row.log2 == curr_log2:
            # Continue the current segment
            curr_end = row.end
            curr_genes.append(row.gene)
            curr_probes += 1
        else:
            # Segment break
            # Finish the current segment
            if curr_probes:
                squashed_rows.append((curr_chrom, curr_start, curr_end,
                                      ",".join(pd.unique(curr_genes)),
                                      curr_log2, curr_probes))
            # Start a new segment
            curr_chrom = row.chromosome
            curr_start = row.start
            curr_end = row.end
            curr_genes = []
            curr_log2 = row.log2
            curr_probes = 1
    # Remainder
    squashed_rows.append((curr_chrom, curr_start, curr_end,
                          ",".join(pd.unique(curr_genes)),
                          curr_log2, curr_probes))
    return segments.as_rows(squashed_rows)


# TODO/ENH combine with transfer_fields
# Recalculate segment means, weights, depths here instead of in R
def repair_segments(segments, orig_probes):
    """Post-process segmentation output.

    1. Ensure every chromosome has at least one segment.
    2. Ensure first and last segment ends match 1st/last bin ends
       (but keep log2 as-is).
    """
    segments = segments.copy()
    extra_segments = []
    # Adjust segment endpoints on each chromosome
    for chrom, subprobes in orig_probes.by_chromosome():
        chr_seg_idx = np.where(segments.chromosome == chrom)[0]
        orig_start = subprobes[0, 'start']
        orig_end =  subprobes[len(subprobes)-1, 'end']
        if len(chr_seg_idx):
            segments[chr_seg_idx[0], 'start'] = orig_start
            segments[chr_seg_idx[-1], 'end'] = orig_end
        else:
            null_segment = (chrom, orig_start, orig_end, "-", 0.0, 0)
            extra_segments.append(null_segment)
    if extra_segments:
        segments.add(segments.as_rows(extra_segments))
    return segments
