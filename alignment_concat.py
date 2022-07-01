##### alignment_concat

import sys
import os
import getopt

try:
	opts, args = getopt.getopt(sys.argv[1:], 'i:d:D:o:s:n:g:e:f:h')
																						
except getopt.GetoptError:
	print('ERROR getting options, please see help by specifing -h')
	sys.exit(2) ### close ofter error from try
	
	
arg_len = len(opts)

if arg_len == 0:
	print('No options provided. Please see help by specifing -h')
	sys.exit(2)

in_dir_name = None
file_ext  = ".fa"
out_name  = "testout.fa"
delim_g_str = "-"
delim_s_str = "-"
new_delim_str = "_"
sp_group_pos  = 1
gene_name_pos = 2
filter_filename = None
#print (opts) ## see args
for opt, arg in opts:
	if opt in ('-h'):
		print("\n**** alignment_concat.py | Written by DJP, 07/04/16 in Python 3.5 in SA / Edinburgh train ****\n")
		print("\n**** Re-written by DJP, 08/04/20 in Python 3.5 in Lausanne ****\n")
		print("This program takes a number of seperate fasta file alignments as input, and concats them") 
		print("Sequences in each file DO NOT need be in order before use\n")	
		print("\n**** USAGE **** \n")
		print("python3 alignment_concat.py -i [input dir] -o [output file] \n")
		print("\n**** OPTIONS **** \n")
		print("\t-e\tfile extention. Default = .fa")		
		print("\t-d\tdelim to get gene name from header. Default = -")
		print("\t-D\tdelim to get sp name from header. Default = -")
		print("\t-n\tnew delim for output file. Default = _")
		print("\t-s\tIndex for sp name after spliting. Default = 1")
		print("\t-g\tIndex for gene name after spliting. Default = 2")	
		print("\t-f\tfilter filename. Specify if want to filter out any genes")
		
		print("\n**** EXAMPLE fasta file ****\n")
	
		print(">speciesA-gene1\nATTATACACCACGACGAGCAGCAGCCGAGCACGACGCGAG")
		print(">speciesB-gene1\nCCCCCCCCCCCGAGCAGCAGCCGAGCACGACGCGAGCAGC")
		print(">speciesC-gene1\nGGGGGGGGCCACGACGAGCAGCAGCCGAGCACGACGCGAG\n\n")

		print("\n**** EXAMPLE code ****\n")
		print("python3 alignment_concat.py -i in_dir -e .fa -D - -d - -s 1 -g 2 -n _\n\n")
		
		
	
		sys.exit(2)
	elif opt in ('-i'):
		in_dir_name  = arg
	elif opt in ('-e'):
		file_ext   = arg	
	elif opt in ('-o'):
		out_name = arg
	elif opt in ('-d'):		
		delim_g_str = arg
	elif opt in ('-D'):		
		delim_s_str = arg
	elif opt in ('-s'):		
		sp_group_pos = int(arg)
	elif opt in ('-g'):		
		gene_name_pos = int(arg)
	elif opt in ('-n'):		
		new_delim_str = arg
	elif opt in ('-f'):		
		filter_filename = arg
	else:
		print("i dont know")
		sys.exit(2)



## Read seqs, unwrap, add into a dict
### read in file

seq_dict = {}
N_seqs_per_file = set()
all_new_names = set()
gene_name_set = set()
sp_name_set = set()

path = in_dir_name
for path, subdirs, files in os.walk(path):
	for name in files:
		if name.endswith(file_ext):
			#print (os.path.join(path, name))
			curr_file = open(os.path.join(path, name))
			
			output_fasta_name = name + ".TEMP_extract_fasta_file" 

			output_file = open(output_fasta_name, "w")
			count = 0

			for line in curr_file:
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
			seq_len = set()

			done = 0
			seq_file_1 = open(output_fasta_name)
			for line in seq_file_1:
				lineA = line.rstrip("\n")
				if lineA.startswith(">"):
					lineB = lineA.replace(">", "")
					sp        = lineB.split(delim_s_str)[sp_group_pos -1]
					gene_name = lineB.split(delim_g_str)[gene_name_pos -1]
					new_name = sp + new_delim_str + gene_name
					gene_name_set.add(gene_name)
					sp_name_set.add(sp)
					#print(new_name)
					if new_name not in all_new_names:
						all_new_names.add(new_name)
					else:
						print("New names are not unique. FIX THIS before going on.")
						sys.exit(2)
					name_list.append(new_name)
				else:
					seq_list.append(lineA)
					done = done + 1
		
			for element in range(0,len(name_list)):
				name1 = name_list[element]
				seq1 = seq_list[element]
				seq_dict[name1] = seq1
				seq_len.add(len(seq1))
				
			N_seqs_per_file.add(len(name_list))
			if len(seq_len) != 1:
				print("alignments not the same length. FIX THIS")
				sys.exit(2)
			#print(seq_dict)
			## tidyup
			seq_file_1.close()
			os.remove(output_fasta_name)
						
print("\n\nTotal number of seqs read: " + str(len(seq_dict)))
if len(N_seqs_per_file) != 1:
	print("Different files have different number of sequences. FIX THIS")
	sys.exit(2)
else:
	print("Number of seqs per file: " + str(list(N_seqs_per_file)[0]))
	
#print(sp_name_set)

if filter_filename == None:
	print("Number of alignments to be joined: " + str(len(gene_name_set)))

sp_name_list_s = sorted(list(sp_name_set))
gene_name_list_s = sorted(list(gene_name_set))


###########################################################################################
### if filtering genes to a subset

if filter_filename != None:
	gene_name_set_f = set()
	
	filter_file = open(filter_filename)
	for line in filter_file:
		line = line.strip()
		gene_name_set_f.add(line)
	
	gene_name_list_f = []
	for el in gene_name_list_s:
		if el in gene_name_set_f :
			gene_name_list_f.append(el)
		
	gene_name_list_s = gene_name_list_f
	
	print("Number of alignments to be joined after filtering: " + str(len(gene_name_list_s)))



######################################################################
## output

out_fa_file = open(out_name, "w")
align_len = 0

N_sp = 0
for s in sp_name_list_s:
	out_fa_file.write(">" + s + "\n")
	N_sp = N_sp + 1
	for g in gene_name_list_s:
		rec = seq_dict.get(s + new_delim_str + g)
		out_fa_file.write(rec)
		if N_sp == 1:
			align_len = align_len + len(rec)
	out_fa_file.write("\n")
	
print("Alignment length: " + str(align_len))
	
print("\nOutput alignment file: " + out_name + "\n")

print("\nFinished, JMS\n\n")
