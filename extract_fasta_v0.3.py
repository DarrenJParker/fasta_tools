### extract_fasta.py

import sys
import os

args = sys.argv
arg_len = len(args)


if arg_len <6:
	print("\n**** extract_fasta_v0.2.py | Version 0.2 | Written by DJP, 12/01/15 in Python 3.4 ****\n")
	### update 0.1 unwraps the fasta file before searching (as a precaution)
	### update 0.2 allows wanted seq names to be specified on the command line
	### update 0.3 allows unwanted seq names to be specified using invert option
	print("This program takes two input files: a fasta file, and file of sequence names.") 
	print("It outputs fasta sequences if they match those in the list.")
	print("\n**** USAGE **** \n")
	print("extract_fasta_v0.3.py [name of fasta file] [name of list file] [name of output file] [want_as_list_or_file] [invert]\n")
	print("want_as_list_or_file = either 'L' if wanted sequences are specified as a command line list (comma delimited), or 'F' if wanted sequences are specified as a file")
	print("\n invert option = if want to get sequnces in the want file specify 'no', if want to get sequnces NOT in want file specify 'yes' (i.e. invert match)")
	
	print("\n**** EXAMPLE using a want LIST ****\n")
	
	print("extract_fasta_v0.2.py fastafile.fa  seq1,>seq544 outputfile.fa L no\n")
	print("fastafile.fa")
	print(">seq44\nATTATACACCACGACGAGCAGCAGCCGAGCACGACGCGAGCAGC")
	print(">seq1\nCCCCCCCCCCCGAGCAGCAGCCGAGCACGACGCGAGCAGC")
	print(">seq544\nGGGGGGGGCCACGACGAGCAGCAGCCGAGCACGACGCGAGCAGC\n\n")

	print("NOTE: Names in wanted seq names can be given as [>seq1] or [seq1] or a mix. Otherwise names much match those in the input fasta file exactly.")

	
	print("\n**** EXAMPLE using a want FILE ****\n")
	print("extract_fasta_v0.2.py fastafile.fa  wantfile.txt outputfile.fa F no\n")
	print("fastafile.fa")
	print(">seq44\nATTATACACCACGACGAGCAGCAGCCGAGCACGACGCGAGCAGC")
	print(">seq1\nCCCCCCCCCCCGAGCAGCAGCCGAGCACGACGCGAGCAGC")
	print(">seq544\nGGGGGGGGCCACGACGAGCAGCAGCCGAGCACGACGCGAGCAGC\n\n")

	print("wantfile.txt")
	print(">seq1")
	print("seq44\n\n")

	print("NOTE: Names in wantfile can be given as [>seq1] or [seq1] or a mix. Otherwise names much match those in the input fasta file exactly.")

else:
	seqF1 = args[1]
	wantF1 = args[2]
	outF1 = args[3]
	file_or_list = args[4]
	invertor = args[5]

	
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

	seq_N = str(len(name_list))

	print ("\nLoaded " + seq_N + " seqeunces from " + seqF1 + ".\n")
	output_file = open(outF1, "w")

	### get wanted seqs and output them
	lines_in_want_file = 0
	found_seq = 0
	
	if file_or_list == 'F' and invertor == 'no':
		want_file_1 = open(wantF1)
		for line in want_file_1:
			lines_in_want_file = lines_in_want_file + 1
			lineA = line.rstrip("\n")
			lineB = lineA.replace(">", "")
			if lineB in name_list: ### in case blank line left at end or seqs in list not 
				found_seq = found_seq + 1
				output_file.write(">" + lineB + "\n" + seq_dict.get(lineB) + "\n")
		print(str(lines_in_want_file) + " lines read from want file (this includes blank lines).\n")
		print(str(found_seq) + " sequence(s) were found from " + wantF1 + " and added to " + outF1)	
	
	elif file_or_list == 'L' and invertor == 'no':
		want_list = wantF1.rsplit(',')
		for seqname in want_list:
			lines_in_want_file = lines_in_want_file + 1
			lineA = seqname.rstrip("\n")
			lineB = lineA.replace(">", "")
			if lineB in name_list: ### in case blank line left at end or seqs in list not 
				found_seq = found_seq + 1
				output_file.write(">" + lineB + "\n" + seq_dict.get(lineB) + "\n")
		print(str(lines_in_want_file) + " sequence(s) to be extracted were read from command line.\n")
		print(str(found_seq) + " sequence(s) were found from the command line and added to " + outF1)	
	
	elif file_or_list == 'F' and invertor == 'yes':
		want_file_1 = open(wantF1)
		want_list = []
		for line in want_file_1:
			lineA = line.rstrip("\n")
			lineB = lineA.replace(">", "")
			want_list.append(lineB)
		lines_in_want_file = len(want_list)
		want_set = set(want_list)
		for el in name_list:
			if el not in want_set:
				found_seq = found_seq + 1
				output_file.write(">" + el + "\n" + seq_dict.get(el) + "\n")
		print(str(lines_in_want_file) + " lines read from want file (this includes blank lines).\n")
		print(str(found_seq) + " sequence(s) were NOT found from those in the want file and added to " + outF1)	
	
	
	elif file_or_list == 'L' and invertor == 'yes':
		want_list = wantF1.rsplit(',')
		lines_in_want_file = len(want_list)
		want_set = set(want_list)
		for el in name_list:
			if el not in want_set:
				found_seq = found_seq + 1
				output_file.write(">" + el + "\n" + seq_dict.get(el) + "\n")
		print(str(lines_in_want_file) + " sequence(s) to be extracted were read from command line.\n")
		print(str(found_seq) + " sequence(s) were NOT found from those specified on the command line and added to " + outF1)				
	else:
		print("Error: Please specify either 'L' (list) or 'F' (file) for want_as_list_or_file command line argument\n and \nPlease specify either 'no' or 'yes' for the invert command line argument")
	
	
	## tidyup
	seq_file_1.close()
	os.remove(output_fasta_name)
	print("\nFinished\n")
	
	
	
	
	
	
	

	
	
