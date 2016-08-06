##### alignment_base_split

import sys
import os

args = sys.argv
arg_len = len(args)


if arg_len <2:
	print("\n**** alignment_base_split.py | Written by DJP, 07/04/16 in Python 3.5 in Edinburgh / SA train ****\n")
	print("This program takes a fasta alignments as input, and outputs 3 fasta alignments:\n first codon (seq_name_base + _first_position.fa)\nsecond codon (seq_name_base + _second_position.fa)\n third codon (seq_name_base + _third_position.fa)") 
	print("\n**** WARNING **** \n")
	print("base name for output is taken to be the part of the file name before the first '.' \n")	
	print("\n**** USAGE **** \n")
	print("alignment_base_split.py [name of fasta alignment file] \n")

else:
	seqF1 = args[1]

	### add seqs to dictionary
	name_list = []
	seq_list = []
	seq_dict = {}

	seq_name = seqF1
	done = 0
	seq_file_1 = open(seq_name)
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

	seq_N = str(len(name_list))

	print ("\nLoaded " + seq_N + " seqeunces from " + seqF1 + ".\n")
	
	### split by base
	
	seq_name_base = seq_name.rsplit('.') ### beware if name of fasta file has more than one '.'
	seq_name_base = seq_name_base[0]
	
	output_file_0 = open(seq_name_base + '_first_position.fa', "w")
	output_file_1 = open(seq_name_base + '_second_position.fa', "w")
	output_file_2 = open(seq_name_base + '_third_position.fa', "w")
	
	for el in name_list: # keep order
		seq = seq_dict.get(el)
		#seq = seq.upper()
		seq_len = len(seq)
		
		base_0 = ""
		for number in range(0, seq_len, 3):  ## range to give codon 1,2, or 3
			seq_t = seq[number]
			base_0 = base_0 + seq_t
		#print(el + base_0)
		output_file_0.write('>' + el + '\n' + base_0 + '\n')
		
		base_1 = ""
		for number in range(1, seq_len, 3):  ## range to give codon 1,2, or 3
			seq_t = seq[number]
			base_1 = base_1 + seq_t
		#print(el + base_1)
		output_file_1.write('>' + el + '\n' + base_1 + '\n')
		
		base_2 = ""
		for number in range(2, seq_len, 3):  ## range to give codon 1,2, or 3
			seq_t = seq[number]
			base_2 = base_2 + seq_t
		#print(el + base_2)
		output_file_2.write('>' + el + '\n' + base_2 + '\n')
		
	
	
	
