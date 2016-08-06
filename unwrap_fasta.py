### unwrap a fasta file

import sys

args = sys.argv
arg_len = len(args)

if arg_len <3:
	print("\n**** Written by DJP, 23/11/15 in Python 3.4 ****\n")
	print("This program takes a wrapped fasta file as input.") 
	print("It outputs an unwrapped fasta file.")
	print("\n**** USAGE **** \n")
	print("unwrap_fasta.py [name of fasta file] [name of output file]\n")

else:	
	input_fasta = args[1]
	output_fasta = args[2]


	output_file = open(output_fasta, "w")

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