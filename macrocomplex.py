import argparse
import os
import os.path


parser = argparse.ArgumentParser(description="This program reads the input files with protein interactions and returns the possible macrocomplexes.")

parser.add_argument('-i', '--input',
					dest = "infiles",
					action = "store",
					default = None,
					help = "Input PDB files or directory with PDB files.")

parser.add_argument('-v', '--verbose',
					dest = "verbose",
					action = "store_true",
					default = "False",
					help = "Print log in stderr")

parser.add_argument('-k', '--num_chains',
					dest = "k",
					action = "store",
					default = None,
					type = int,
					help = "Maximum number of total chains on the Macrocomplex.")

parser.add_argument('-st', '--stoich',
					dest = "stoichiometry",
					action = "save",
					default = None,
					type = dict,
					help = "Dictionary with the stoichiometry of the Macrocomplex.")

parser.add_argument('-o', '--output',
					dest = "outfile",
					action = "store",
					default = None,
					help = "Name for the outfile")

parser.add_argument('-n','--network',
					dest = "network",
					action = "store_true",
					default = "False",
					help = "Gives the network of the interactions")

parser.add_argument('-opt','--optimization',
					dest = "optimization",
					action = "store_true",
					default = "False",
					help = "Optimize the output")

parser.add_argument('-cn','--contact_num',
					dest = "contact_num",
					action = "store",
					default = None,
					type = int,
					help = "Maximum number of permited contacts")


options = parser.parse_args()

#Looking for the input file

if os.path.isdir(options.infiles):
	files_list = []
	for files in os.listdir(options.infiles):
		if files.endswith(".pdb"):
			files_list.append(os.path.join(options.infiles, files))
else:
	path = "./"
	files_list = []
	for files in os.listdir(path):
		if files.endswith(".pdb"):
			files_list.append(files) 





