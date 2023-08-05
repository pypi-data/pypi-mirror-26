"""A collection of tools to handle genomic tests, in particular Tajima's D.

Part of the biostructmap package.
"""
from __future__ import absolute_import, division, print_function

from io import StringIO
from Bio import AlignIO
import dendropy

from .seqtools import _sliding_window_var_sites

def tajimas_d(alignment, window=None, step=3):
    """
    Uses DendroPy package to calculate Tajimas D.

    Notes:
        Several optimisations are used to speed up the calculation, including
        memoisation of previous window result, which is used if no new
        polymorphic sites are added/subtracted.

    Args:
        alignment (str/Bio.Align.MultipleSequenceAlignment): A multiple sequence
            alignment string in FASTA format or a multiple sequence alignment
            object, either as a Bio.Align.MultipleSequenceAlignment or a
            biostructmap.SequenceAlignment object.
        window (int, optional): The size of the sliding window over which
            Tajima's D is calculated. Default is None, in which case a
            single Tajima's D value is calculated for the multiple sequence
            alignment.
        step (int, optional): Step size for sliding window calculation.
            Default step size of 3 (ie. one codon).
    Returns:
        float/dict: If window parameter is None, returns a single value for
            Tajima's D. Otherwise a dict mapping genome window midpoint to
            calculated Tajima's D values is returned.
    """
    if window:
        if isinstance(alignment, str):
            alignment = AlignIO.read(StringIO(alignment), 'fasta')
        results = {}
        prev_win = None
        prev_d = None
        slide = _sliding_window_var_sites(alignment, window, step=step)
        for i, win in enumerate(slide):
            centre = i*step + 1 + (window-1)/2
            if win == prev_win:
                results[centre] = prev_d
            else:
                current_d = _tajimas_d(win)
                results[centre] = current_d
                prev_d = current_d
                prev_win = win
        return results
    else:
        return _tajimas_d(alignment)

def _tajimas_d(alignment):
    """
    Uses DendroPy to calculate tajimas D.

    If Tajima's D is undefined (ie. Dendropy Tajima's D method raises a
    ZeroDivisionError), then this method returns None.

    Args:
        alignment (str/Bio.Align.MultipleSequenceAlignment): A multiple sequence
            alignment string in FASTA format or a multiple sequence alignment
            object, either as a Bio.Align.MultipleSequenceAlignment or a
            biostructmap.SequenceAlignment object.

    Returns:
        float: Tajima's D value. Returns None if Tajima's D is undefined.
    """
    if not isinstance(alignment, str):
        data = alignment.format('fasta')
    else:
        data = alignment
    if not alignment or len(alignment[0]) == 0:
        return None
    try:
        seq = dendropy.DnaCharacterMatrix.get(data=data,
                                              schema='fasta')
        taj_d = dendropy.calculate.popgenstat.tajimas_d(seq)
    except ZeroDivisionError:
        taj_d = None
    return taj_d

def nucleotide_diversity(alignment):
    """
    Use DendroPy to calculate nucleotide diversity.

    If nucleotide diversity is undefined, returns None.

    Args:
        alignment (str/Bio.Align.MultipleSequenceAlignment): A multiple sequence
            alignment string in FASTA format or a multiple sequence alignment
            object, either as a Bio.Align.MultipleSequenceAlignment or a
            biostructmap.SequenceAlignment object.

    Returns:
        float: Nucleotide diversity value. Returns None if nucleotide
            diversity is undefined.
    """
    if not isinstance(alignment, str):
        data = alignment.format('fasta')
    else:
        data = alignment
    if not alignment or len(alignment[0]) == 0:
        return None
    seq = dendropy.DnaCharacterMatrix.get(data=data, schema='fasta')
    diversity = dendropy.calculate.popgenstat.nucleotide_diversity(seq)
    return diversity

def wattersons_theta(alignment):
    """
    Use DendroPy to calculate Watterson's Theta.

    If Watterson's Theta is undefined, returns None.

    Args:
        alignment (str/Bio.Align.MultipleSequenceAlignment): A multiple sequence
            alignment string in FASTA format or a multiple sequence alignment
            object, either as a Bio.Align.MultipleSequenceAlignment or a
            biostructmap.SequenceAlignment object.

    Returns:
        float: Watterson's Theta value. Returns None if Watterson's Theta is
            undefined.
    """
    if not isinstance(alignment, str):
        data = alignment.format('fasta')
    else:
        data = alignment
    if not alignment or len(alignment[0]) == 0:
        return None
    seq = dendropy.DnaCharacterMatrix.get(data=data, schema='fasta')
    theta = dendropy.calculate.popgenstat.wattersons_theta(seq)
    return theta
