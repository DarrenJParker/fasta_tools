## fasta len 

import sys
import os

args = sys.argv
arg_len = len(args)

if arg_len <2:
	print("\n**** Written by DJP, 11/11/18 in Python 3.4 ****\n")
	print("This program takes a fasta file as input.") 
	print("It removes sequences that have exactly the same sequence.")
	print("\n**** USAGE **** \n")
	print("python3 fasta_remove_duplicate_sequences.py [name of fasta file] \n")

else:
	input_fasta = args[1]
	
	##### FIRST unwrap fasta - precautionary will be necessary for some files 
	### note making a temp unwrapped fasta file  - removed at end
	output_fasta_name = input_fasta + ".TEMP_extract_fasta_file" 

	output_file = open(output_fasta_name, "w")
	print("Unwrapping fasta file\n")
	count = 0
	in_file = open(input_fasta)
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
	
	
	name = []
	seq = []
	all_seq = ""
	
	seq_dict = {}
	
	seq_count = 0
	file_in = open(output_fasta_name)
	for line in file_in:
		line = line.rstrip("\n")
		if line.startswith(">"):
			seq_count = seq_count + 1
			line = line.replace(">", "")
			name.append(line)
		else:
			seq.append(line)
			all_seq = all_seq + line
	
	### output if not a duplicate
	
	seen_seqs = set()
	number_of_dup_seqs = 0
	
	output_file = open(input_fasta.replace(".fa", "").replace(".fasta", "") + "_nodups.fa", "w")
	
	for element in range(0,len(name)):
		name1 = name[element]
		seq1 = seq[element].upper()
		if seq1 not in seen_seqs:
			seen_seqs.add(seq1)
			output_file.write(">" + name1 + "\n" + seq1 + "\n")
			#seq_dict[name1] = seq1
		else:
			number_of_dup_seqs = number_of_dup_seqs + 1


	print("\n\nNumber of seqs in " + input_fasta + " = " + str(seq_count))
	print("Number of duplicate seqs = " + str(number_of_dup_seqs))
	print("Outputting "  + str(seq_count - number_of_dup_seqs) + " seqs to " + input_fasta.replace(".fa", "").replace(".fasta", "") + "_nodups.fa")	

	## tidyup
	
	file_in.close()
	os.remove(output_fasta_name)

	
	print("\n\nFinished, Bliss Wagoner\n\n")

