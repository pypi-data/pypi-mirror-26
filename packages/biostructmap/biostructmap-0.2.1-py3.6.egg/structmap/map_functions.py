"""A collection of methods that can be used to map data to a set of residues
within a PDB structure.

These methods all take the form:

def some_method(structure, data, residues, ref):
    ...
    return final_data

Required input parameters include:
    structure: a pdb structure object (Structure)
    data: a set of initial sequence-aligned data that is later filtered,
        and some function used to summarise filtered data.
    residues: a list of residues over which to filter input data. Note that
        filtering of initial data is not *required*, but is normally
        incorporated within the body of the defined function.
    ref: a dictionary mapping PDB residue numbers (key) to a reference sequence
        where the first residue in the sequence is indexed as 1, and
        incremented from there (value).

It is possible to write user-defined functions to pass to the Structure.map()
method following the above format ie. for the incorporation of novel amino
acid scales.

Note that departures from these input parameter conventions will be noted
in function docstrings, but otherwise can be assumed to follow the above
parameter convention.
"""
from __future__ import absolute_import, division

from Bio.SeqUtils import seq1, ProtParamData
from Bio.Data.SCOPData import protein_letters_3to1
import numpy as np
from .seqtools import _construct_sub_align_from_chains
from . import gentests


def _count_residues(_structure, _data, residues, _ref):
    """Simple function to count the number of residues within a radius.

    Returns:
        int: Number of residues within a radius"""
    return len(residues)

def _tajimas_d(_structure, alignments, residues, ref):
    """"Calculate Tajimas D for selected residues within a PDB chain.
    input is Chain object, multiple sequence alignment object,
    list of surrounding residues, and a dictionary giving mapping
    of PDB residue number to codon positions.

    Args:
        alignments (dict): A dictionary of multiple sequence alignments
            for each unique chain in the protein structure. Dictionary keys
            should be chain IDs.
        ref: A dictionary mapping PDB residue number to codon positions
            relative to the supplied multiple sequence alignment.
    Returns:
        float: Tajima's D value. Returns None if Tajima's D is undefined.
    """
    chains = alignments.keys()
    #filter list of residues based on those that have mapped codons:
    ref_residues = [ref[x] for x in residues if x in ref]  # Returns [('A', (15,16,17)), ...]
    # Remove duplicate items (i.e. same data point, different chains) from
    # list of residues and set chain identifier to match alignment keys.
    codons = set([(chain, x[1]) for chain in chains
                  for x in ref_residues if x[0] in chain])
    #Get alignment bp from selected codons
    sub_align = _construct_sub_align_from_chains(alignments, codons, fasta=True)
    #Compute Tajima's D using selected codons.
    tajd = gentests.tajimas_d(sub_align)
    return tajd


def _default_mapping(_structure, data, residues, ref, ignore_duplicates=True):
    """"Calculate an average of all data points over selected residues.

    Returns:
        float: Average of all data points within a radius.
    """
    chains = data.keys()
    #filter list of residues based on those that have mapped reference
    ref_residues = [ref[x] for x in residues if x in ref]
    residues = [(chain, x[1]) for chain in chains
                for x in ref_residues if x[0] in chain]
    if ignore_duplicates:
        residues = set(residues)
    data_points = [data[res[0]][res[1]] for res in residues]
    if data_points:
        average = np.mean(data_points)
    else:
        average = None
    return average


def _snp_mapping(_structure, data, residues, ref, ignore_duplicates=True,
                 output_count=False):
    """"Calculate the percentage of SNPs over selected residues.
    Data is a list of residues that contain SNPs.

    Args:
        data: List of residues that are polymorphic, aligned to reference seq.
        ignore_duplicates (bool): Ignore duplicate data points (i.e. on two
            separate chains) if True.
        output_percent (bool): Output the total number of SNPs within each
            radius if True. Default behaviour is to return a percentage of SNPs.

    Returns:
        float: Proportion of residues within a radius that are polymorphic.
    """
    chains = data.keys()
    #filter list of residues based on those that have mapped reference
    ref_residues = [ref[x] for x in residues if x in ref]
    residues = [(chain, x[1]) for chain in chains
                for x in ref_residues if x[0] in chain]
    if ignore_duplicates:
        residues = set(residues)

    data = [(chain, snp) for chain, snps in data.items() for snp in snps]
    #Find the intersection between the residues which contain SNPs and
    #the selected residues on the Structure
    snp_xor_res = [residue for residue in residues if residue in data]
    num_snps = len(snp_xor_res)
    if output_count:
        output = num_snps
    else:
        try:
            output = num_snps / len(residues) * 100
        #If no residues are mapped onto the reference sequence, return None.
        except ZeroDivisionError:
            output = None
    return output


def _map_amino_acid_scale(structure, data, residues, _ref):
    """
    Compute average value for amino acid propensity scale.

    Args:
        data (str): A string representing an amino acid propensity scale.
            Options are:
            'kd' -  Kyte & Doolittle index of hydrophobicity
            'Flex' - Flexibility, Normalized flexibility parameters (B-values)
            'hw' - Hydrophilicity, Hopp & Wood
            'em' - Surface accessibility, Emini Surface fractional probability
            'ja' - Surface accessibility, Janin Interior to surface transfer
                   energy scale

    Returns:
        float: Average propensity scale score over residues within a radius.
    """
    first_model = sorted(structure.models)[0]
    #Get a list of all amino acids within window, converted to one letter code
    aminoacids = [seq1(structure[first_model][res[0]][res[1]].resname,
                       custom_map=protein_letters_3to1)
                  for res in residues]
    scales = {'kd': ProtParamData.kd, # Kyte & Doolittle index of hydrophobicity
              # Flexibility
              # Normalized flexibility parameters (B-values),
              # average (Vihinen et al., 1994)
              'Flex': ProtParamData.Flex,
              # Hydrophilicity
              # Hopp & Wood
              # Proc. Natl. Acad. Sci. U.S.A. 78:3824-3828(1981).
              'hw': ProtParamData.hw,
              # Surface accessibility
              # 1 Emini Surface fractional probability
              'em': ProtParamData.em,
              # 2 Janin Interior to surface transfer energy scale
              'ja': ProtParamData.ja}
    if data in scales:
        scale = scales[data]
    else:
        scale = data
    #Compute mean of scale over all residues within window
    result = np.mean([scale[aa] for aa in aminoacids])
    return result
