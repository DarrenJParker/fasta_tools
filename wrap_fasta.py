import sys
import os
import getopt
import decimal
from decimal import *
import re
import collections

try:
	opts, args = getopt.getopt(sys.argv[1:], 'i:w:h')
																						
except getopt.GetoptError:
	print('ERROR getting options, please see help by specifing -h')
	sys.exit(2) ### close ofter error from try
	
	
arg_len = len(opts)

if arg_len == 0:
	print('No options provided. Please see help by specifing -h')
	sys.exit(2)

in_file_name = None
wrap_len     = 80

#print (opts) ## see args
for opt, arg in opts:
	if opt in ('-h'):
		print("\n**** wrap_fasta.py | Written by DJP, 22/07/22 in Python 3.5 in Porto ****\n")
		print("Wraps fasta seqs to desired len")	
		print("\n**** Usage****\n")
		print("python3 wrap_fasta.py -i [fasta file] -w [wrap len, default = 80] \n\n")
		sys.exit(2)
	elif opt in ('-i'):
		in_file_name  = arg
	elif opt in ('-w'):
		wrap_len  = int(arg)
	else:
		print("i dont know")
		sys.exit(2)

## takes fasta file, unwraps it, and adds seqs to a dict
def fasta_to_dict(in_fasta_file_name):
	output_fasta_name = in_fasta_file_name + ".TEMP_extract_fasta_file" 
	
	output_file = open(output_fasta_name, "w")
	print("\nUnwrapping fasta file")
	count = 0
	in_file = open(in_fasta_file_name)
	for line in in_file:
		count = count + 1
		line = line.rstrip("\n")
		if line.startswith(">") and count == 1:
			output_file.write(line + "\n")
		elif line.startswith(">") and count > 1:
			output_file.write("\n" + line + "\n")
		else: 
			output_file.write(line)	
	
	output_file.close()
	
	
	### add seqs to dictionary
	name_list = []
	seq_list = []
	seq_dict = {}
	
	done = 0
	seq_file_1 = open(output_fasta_name)
	for line in seq_file_1:
		lineA = line.rstrip("\n")
		if lineA.startswith(">"):
			lineB = lineA.lstrip(">")
			name_list.append(lineB)
		else:
			seq_list.append(lineA)
			done = done + 1
			seq_len = len(lineA)
	
	for element in range(0,len(name_list)):
		name1 = name_list[element]
		seq1 = seq_list[element].replace(" ", "") ## remove gaps if seq comes from gblocks 
		seq_dict[name1] = seq1

	## tidyup
	seq_file_1.close()
	os.remove(output_fasta_name)
	
	print("Read " + str(done) + " sequences from " + in_fasta_file_name)
	
	return(seq_dict)

seq_dict = fasta_to_dict(in_file_name)

seq_list = []
for el in seq_dict:
	seq_list.append(el)


outfile = open(in_file_name.replace(".fasta", "").replace(".fa", "") + "_w" + str(wrap_len) + ".fa", "w") 
for s in sorted(seq_list):
	seq = seq_dict.get(s)
	outfile.write(">" + s + "\n")
	for i in range(0, len(seq), wrap_len):
		#print(seq[i:i+wrap_len])
		outfile.write(seq[i:i+wrap_len] + "\n")
		
print("Wrapped seqs to " + str(wrap_len) + "\n")

print("Done, Aurora\n\n")
		
	




