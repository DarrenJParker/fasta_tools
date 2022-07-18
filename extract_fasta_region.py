import sys
import os
import getopt
import decimal
from decimal import *
import re
import collections

try:
	opts, args = getopt.getopt(sys.argv[1:], 'f:s:c:Nh')
																						
except getopt.GetoptError:
	print('ERROR getting options, please see help by specifing -h')
	sys.exit(2) ### close ofter error from try
	
	
arg_len = len(opts)

if arg_len == 0:
	print('No options provided. Please see help by specifing -h')
	sys.exit(2)

in_file_name = None
seq_name     = None
coords 		 = None
output_file  = True 

#print (opts) ## see args
for opt, arg in opts:
	if opt in ('-h'):
		print("\n**** extract_fasta_region.py | Written by DJP, 18/07/22 in Python 3.5 in Porto ****\n")
		print("Extracts a region of a sequence from a fasta file")	
		print("\n**** Usage ****\n")
		print("python3 extract_fasta_region.py -f [fasta file] -o [seq name] -c [coordinates (x-x)] \n")
		print("\n**** Options ****\n")
		print("-c\tcoordinates in gff style sep by a '-'. For example to extract the first base specify -c 1-1 [default: all bases]")
		print("-N\tNo output file [default: on]\n\n")
		sys.exit(2)
	elif opt in ('-f'):
		in_file_name  = arg
	elif opt in ('-s'):
		seq_name = arg
	elif opt in ('-c'):
		coords = arg
	elif opt in ('-N'):
		output_file = False
	else:
		print("i dont know")
		sys.exit(2)

if seq_name == None:
	print("\nError. No seq name specified. Specify with -s.\n")
	sys.exit(2)
else:
	seq_name  = seq_name.strip().strip(">")
	print("\nGetting seq: " + seq_name)

	if coords == None:
		print("No coords specified so taking the whole seq")
	else:
		print("from " + coords)
	


### takes fasta file, unwraps it, and adds seqs to a dict
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


all_seq_dict = fasta_to_dict(in_file_name)

seq_w = all_seq_dict.get(seq_name)
if seq_w == None:
	print("\n\nError sequence " + seq_name + " not found in " + in_file_name + "\n\n")
	sys.exit(2)


start_c = None
end_c   = None

if coords == None:
	start_c = 1
	end_c   = len(seq_w)


else:
	coords = coords.split("-")
	if len(coords) != 2:
		print("error getting coords. Should be two integers seperated by a - (e.g. 1:1000)")
	else:
		start_c = int(coords[0])
		end_c   = int(coords[1])
		if start_c > end_c:
			print("\nstart cood > than end coord. Setting to end coord.\n")
			start_c = end_c
		if start_c < 1:
			print("\nstart cood should be >=1. Setting to 1.\n")
			start_c = 1
		if start_c > len(seq_w):
			print("\nstart cood should be <=seq len. Setting to seq len.\n")
			start_c = len(seq_w)
		
		if end_c > len(seq_w):
			print("\nend cood should be <=seq len. Setting to seq len.\n")
			end_c = len(seq_w)

extracted_seq = seq_w[start_c -1: end_c]

print("\n>" + seq_name + ":" + str(start_c) + "-" + str(end_c))
print(extracted_seq)



if output_file != False:
	out_file = open(seq_name + "_" + str(start_c) + "-" + str(end_c) + ".fa", "w")
	out_file.write(">" + seq_name + ":" + str(start_c) + "-" + str(end_c) + "\n" + extracted_seq + "\n")

print("\nFinished, Raphidioptera\n\n")


