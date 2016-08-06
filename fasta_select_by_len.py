## fasta_select_by_len 

import sys

args = sys.argv
arg_len = len(args)

if arg_len <5:
	print("\n**** Written by DJP, 24/11/15 in Python 3.4 ****\n")
	print("This program takes a fasta file as input.") 
	print("It outputs a fasta file filtered by specified length.")
	print("\n**** USAGE **** \n")
	print("fasta_select_by_len.py [name of fasta file] [max len] [min len] [output file]\n")
	print("\n**** EXAMPLE ****\n")
	

	print("to output sequences greater than 200bp:")
	print("fasta_select_by_len.py [name of fasta file] [max] [200] [output file]\n")
	
	print("to output sequences less than 200bp:")
	print("fasta_select_by_len.py [name of fasta file] [200] [min] [output file]\n")

	print("to output sequences between 400 and 200bp:")
	print("fasta_select_by_len.py [name of fasta file] [400] [200] [output file]\n")



else:
	input_fasta = args[1]
	greater_than = args[2]
	less_than = args[3]
	out_file = args[4]
	
	
	name = []
	seq = []

	seq_dict = {}

	file_in = open(input_fasta)
	for line in file_in:
		line = line.rstrip("\n")
		if line.startswith(">"):
			line = line.replace(">", "")
			name.append(line)
		else:
			seq.append(line)


	for element in range(0,len(name)):
		name1 = name[element]
		seq1 = seq[element]
		seq_dict[name1] = seq1

	#print(seq_dict)	
	#print(seq_dict.get("contig_99"))
	
	output_file = open(out_file,"w")
	if less_than != "min" and greater_than == "max":
		print("\nOutputting sequences greater-than or equal to " + str(less_than))
		for el in seq_dict:
			seq_len = len(seq_dict.get(el))
			#print(seq_len)
			if seq_len >= int(less_than):
				output_file.write(">" + el + "\n")
				output_file.write(seq_dict.get(el) + "\n")
						
	elif less_than == "min" and greater_than != "max":
		print("\nOutputting sequences less-than or equal to " + str(greater_than))
		for el in seq_dict:
			seq_len = len(seq_dict.get(el))
			#print(seq_len)
			if seq_len <= int(greater_than):
				output_file.write(">" + el + "\n")
				output_file.write(seq_dict.get(el) + "\n")

	elif less_than != "min" and greater_than != "max":
		print("\nOutputting sequences between " + str(greater_than) + " and " + str(less_than))
		for el in seq_dict:
			seq_len = len(seq_dict.get(el))
			#print(seq_len)
			if seq_len <= int(greater_than) and seq_len >= int(less_than):
				output_file.write(">" + el + "\n")
				output_file.write(seq_dict.get(el) + "\n")
	else:
		print("Please specify max and min values")


