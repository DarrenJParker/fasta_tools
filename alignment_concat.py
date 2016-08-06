##### alignment_concat

import sys
import os

args = sys.argv
arg_len = len(args)


if arg_len <3:
	print("\n**** alignment_concat.py | Written by DJP, 07/04/16 in Python 3.5 in SA / Edinburgh train ****\n")
	print("This program takes a number of seperate fasta file alignments as input, and concats them") 
	print("\n**** WARNING **** \n")
	print("Sequences in each file must be in order before use!\n")	
	print("Species name in output is taken to be the first part of the fasta seq (before '-' delim). If no '-' delim, the species name is just that in the first fasta file!\n")	
	print("\n**** USAGE **** \n")
	print("alignment_base_split.py [extention of files that want concatenating] [name of output file]\n")
	
	
	print("\n**** EXAMPLE fasta file ****\n")
	
	print(">speciesA-gene1\nATTATACACCACGACGAGCAGCAGCCGAGCACGACGCGAG")
	print(">speciesB-gene1\nCCCCCCCCCCCGAGCAGCAGCCGAGCACGACGCGAGCAGC")
	print(">speciesC-gene1\nGGGGGGGGCCACGACGAGCAGCAGCCGAGCACGACGCGAG\n\n")


	

else:
	file_ext = args[1]
	out_name = args[2]

	### get filenames
	a = os.listdir()
	a1 = []
	for el in a:
		if el.endswith(file_ext): 
			a1.append(el)
	
	### get sp names from first_file
	
	species_names = []
	seq_file_a = open(a1[0])
	for line in seq_file_a:
		line = line.rstrip('\n')
		if line.startswith(">"):
			line = line.rsplit('-')
			line = line[0]
			line = line.split('>')
			line = line[1]
			species_names.append(line)
	
	
	#### read all seqs in 		
	all_seqs = []		
	for fi in a1:
		seq_file_1 = open(fi)
		count_seq = 0
		for line in seq_file_1:
			line = line.rstrip('\n')
			if not line.startswith('>'):
				count_seq = count_seq + 1
				all_seqs.append(line)
				#print(line)
	#print(all_seqs)

	print('\nI think there are ' + str(count_seq) + ' sequences in the alignment')
	print('\nI think the species are ' + str(species_names) + '\n')
	all_seqs_len = len(all_seqs)

	### function to cat seqs
	def get_nth (seq, start, end, iter): # start = seq number, end = total N seqs, iter = number of seqs in file
		base_0 = ""
		for number in range(start, end, iter): 
			seq_t = seq[number]
			base_0 = base_0 + seq_t	
		return(base_0)

	output_file = open(out_name, "w")
	for nu in range(0,count_seq,1):
		b1 = get_nth(all_seqs, nu, all_seqs_len, count_seq)
		#print(b1 + '\n')
		output_file.write('>' + species_names[nu] + '\n' + b1 + "\n")
		
	#b1 = get_nth(all_seqs, 1, all_seqs_len, 4)
	#print(b1 + '\n')