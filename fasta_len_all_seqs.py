### extract_fasta.py

import sys
import os

args = sys.argv
arg_len = len(args)


if arg_len <2:
	print("\n**** fasta_len_all_seqs.py  | Written by DJP, 01/05/16 in Python 3.4 in Lausanne ****\n")
	print("This program takes a fasta file as input") 
	print("It outputs the length of each sequence.")
	print("\n**** USAGE **** \n")
	print("fasta_len_all_seqs.py [name of fasta file] \n")


else:
	seqF1 = args[1]
	
	##### FIRST unwrap fasta - precautionary will be necessary for some files 
	### note making a temp unwrapped fasta file  - removed at end
	output_fasta_name = seqF1 + ".TEMP_extract_fasta_file" 

	output_file = open(output_fasta_name, "w")
	print("Unwrapping fasta file\n")
	count = 0
	in_file = open(seqF1)
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
			lineB = lineA.replace(">", "")
			name_list.append(lineB)
		else:
			seq_list.append(lineA)
			done = done + 1
			done_divide = done / 1000
			if done_divide.is_integer():
				print("Read " + str(done) + " sequences from " + seqF1)


	for element in range(0,len(name_list)):
		name1 = name_list[element]
		seq1 = seq_list[element]
		seq_dict[name1] = seq1

	

	output_file_1 = open(seqF1 + "_lengths" + '.fa', "w")
	for el in name_list:
		a1 = str(len(seq_dict.get(el)))
		output_file_1.write(el + '\t' + a1 + '\n')
		#print(a1)
	
	
	## tidyup
	seq_file_1.close()
	os.remove(output_fasta_name)
	print("\nFinished\n")
	
	
	
	
	
	
	

	
	
