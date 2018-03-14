from Bio.PDB import *
parser = PDBParser(PERMISSIVE=1)
struct = parser.get_structure("3afa", "3afa.pdb")
model = struct[0]
model2 = struct[0]
chains = list(model.get_chains())
print(chains)

class ChainSelect(Select):
    def __init__(self, chain1):
        self.chain1 = chain1
        #self.chain2 = chain2

    def accept_chain(self, chain):
        if chain.get_id() == self.chain1:
            return 1
        else:
            return 0

for chain1 in model:
    chains.remove(chain1)
    for chain2 in model2:
        pdb_chain_file = 'chain_{}_{}'.format(chain1.get_id(), chain2.get_id())
        io_w_no_h = PDBIO()
        io_w_no_h.set_structure(struct)
        with open(pdb_chain_file, "w") as fp:
            io_w_no_h.save(fp, ChainSelect(chain1.get_id()), write_end=0)
            io_w_no_h.save(fp, ChainSelect(chain2.get_id()), write_end=1)
