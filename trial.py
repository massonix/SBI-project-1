from Bio.PDB import *
import sys
import os
from Bio import pairwise2

if len(sys.argv)<2:
    inter = None
else:
    inter = sys.argv[1]

if os.path.isdir(inter):
    files_list = []
    for files in os.listdir(inter):
        if files.endswith(".pdb"):
            files_list.append(os.path.join(inter, files))

elif inter is None:
    path = "./"
    files_list = []
    for files in os.listdir(path):
        if files.endswith(".pdb"):
            files_list.append(files)

def GetStructures(pdbfile):
    """
    Given a pdbfile, gets it's structure.
    :param pdbfile: pdb file to open
    :return: structure object
    """
    parser = PDBParser()
    structure = parser.get_structure(pdbfile[0:-4], pdbfile)
    return structure

def Alignsequence(structure1, structure2):
    """
    Given 2 structures, gets the sequence and aligns it
    :param structure1: structure 1 to align
    :param structure2: structure 2 to align
    :return: Alignment
    """
    ppb = PPBuilder()
    for pp in ppb.build_peptides(structure1):
        sequence1 = pp.get_sequence()
    for pp in ppb.build_peptides(structure2):
        sequence2 = pp.get_sequence()

    alignment = pairwise2.align.globalxx(sequence1, sequence2)
    return alignment

class Superimpose(object):

    def __init__(self, structure1, structure2):
        self.structure1 = structure1
        self.structure2 = structure2
        self.si = Superimposer()

    def SuperimposeStructures(self):
        """
        :param structure1: first structure to superimpose
        :param structure2: second structure to superimpose
        :return: rmsd object
            """
        atoms_a = list(self.structure1.get_atoms())
        atoms_b = list(self.structure2.get_atoms())
        if len(atoms_a) > len(atoms_b):
            atoms_a = atoms_a[:len(atoms_b)]
        else:
            atoms_b = atoms_b[:len(atoms_a)]

        self.si.set_atoms(atoms_a, atoms_b)

        return self.si

    def getRMSD(self):

        superimpose = self.SuperimposeStructures()
        rmsd = superimpose.rms

        return rmsd


structures = {}

for file in files_list:
    structures[file] = GetStructures(file)

print(structures)

structures2 = structures.copy()
scores = {}

for file, structure in structures2.items():
    chains1 = list(structure[0].get_chains())
    for file2, structure2 in structures.items():
        chains2 = list(structure2[0].get_chains())
        if file != file2:
            scores[file + file2] = []
            # Alignment1 = Alignsequence(chains1[0], chains2[0])
            # Alignment2 = Alignsequence(chains1[0], chains2[1])
            # Alignment3 = Alignsequence(chains1[1], chains2[0])
            # Alignment4 = Alignsequence(chains1[1], chains2[1])
            # scores[file + file2] = [Alignment1[0][2]/len(list(chains1[0].get_residues())), Alignment2[0][2]/len(list(chains1[0].get_residues())), Alignment3[0][2]/len(list(chains1[1].get_residues())), Alignment4[0][2]/len(list(chains1[0].get_residues()))]

            for chain in chains1:
            #     #chains_copy.remove(chain)
                 for chain2 in chains2:
                     Alignment = Alignsequence(chain, chain2)
                     scores[file + file2].append(Alignment[0][2]/len(list(chain.get_residues())))
            #        if Alignment[0][2]/len(list(chain.get_residues())) > 0.95:
            #             atoms_a = list(chain.get_atoms())
            #             atoms_b = list(chain2.get_atoms())
            #             atoms_a = atoms_a[:len(atoms_b)]
            #             si = Superimposer()
            #             si.set_atoms(atoms_a, atoms_b)
            #             print(si.rms)
            same_chains = list(filter(lambda x: x > 0.95, scores[file + file2]))
            if len(same_chains) == 2 or len(same_chains) == 4:
                rmsd = Superimpose(structure[0], structure2[0])
                print(rmsd.getRMSD())
                print ("same files!")
                



print(scores)








