"""Supporting functions for the 'antitarget' command."""
from __future__ import absolute_import, division, print_function
from builtins import map

import logging
import re

from skgenome import GenomicArray as GA

from .params import INSERT_SIZE, MIN_REF_COVERAGE, ANTITARGET_NAME


def do_antitarget(targets, access=None, avg_bin_size=150000,
                  min_bin_size=None):
    """Derive off-targt ("antitarget") bins from target regions."""
    if not min_bin_size:
        min_bin_size = 2 * int(avg_bin_size * (2 ** MIN_REF_COVERAGE))
    return get_antitargets(targets, access, avg_bin_size, min_bin_size)


def get_antitargets(targets, accessible, avg_bin_size, min_bin_size):
    """Generate antitarget intervals between/around target intervals.

    Procedure:

    - Invert target intervals
    - Subtract the inverted targets from accessible regions
    - For each of the resulting regions:

        - Shrink by a fixed margin on each end
        - If it's smaller than min_bin_size, skip
        - Divide into equal-size (region_size/avg_bin_size) portions
        - Emit the (chrom, start, end) coords of each portion
    """
    if accessible:
        # Chromosomes' accessible sequence regions are given -- use them
        access_chroms, target_chroms = compare_chrom_names(accessible, targets)
        # But filter out untargeted alternative contigs and mitochondria
        untgt_chroms = access_chroms - target_chroms
        # Autosomes typically have numeric names, allosomes are X and Y
        is_canonical = re.compile(r"(chr)?(\d+|[XYxy])$")
        if any(is_canonical.match(c) for c in target_chroms):
            chroms_to_skip = [c for c in untgt_chroms
                              if not is_canonical.match(c)]
        else:
            # Alternative contigs have longer names -- skip them
            max_tgt_chr_name_len = max(map(len, target_chroms))
            chroms_to_skip = [c for c in untgt_chroms
                              if len(c) > max_tgt_chr_name_len]
        if chroms_to_skip:
            logging.info("Skipping untargeted chromosomes %s",
                         ' '.join(sorted(chroms_to_skip)))
            skip_idx = accessible.chromosome.isin(chroms_to_skip)
            accessible = accessible[~skip_idx]
    else:
        # Chromosome accessible sequence regions not known -- use heuristics
        # (chromosome length is endpoint of last probe; skip initial
        # <magic number> of bases that are probably telomeric)
        TELOMERE_SIZE = 150000
        accessible = guess_chromosome_regions(targets, TELOMERE_SIZE)

    pad_size = 2 * INSERT_SIZE
    bg_arr = (accessible.resize_ranges(-pad_size)
              .subtract(targets.resize_ranges(pad_size))
              .subdivide(avg_bin_size, min_bin_size))
    bg_arr['gene'] = ANTITARGET_NAME
    return bg_arr


def compare_chrom_names(a_regions, b_regions):
    a_chroms = set(a_regions.chromosome.unique())
    b_chroms = set(b_regions.chromosome.unique())
    if a_chroms and a_chroms.isdisjoint(b_chroms):
        msg = "Chromosome names do not match between files"
        a_fname = a_regions.meta.get('filename')
        b_fname = b_regions.meta.get('filename')
        if a_fname and b_fname:
            msg += " {} and {}".format(a_fname, b_fname)
        msg += ": {} vs. {}".format(', '.join(map(repr, sorted(a_chroms)[:3])),
                                    ', '.join(map(repr, sorted(b_chroms)[:3])))
        raise ValueError(msg)
    return a_chroms, b_chroms


def guess_chromosome_regions(targets, telomere_size):
    """Determine (minimum) chromosome lengths from target coordinates."""
    endpoints = [subarr.end.iat[-1] for _c, subarr in targets.by_chromosome()]
    whole_chroms = GA.from_columns({
        'chromosome': targets.chromosome.drop_duplicates(),
        'start': telomere_size,
        'end': endpoints})
    return whole_chroms
