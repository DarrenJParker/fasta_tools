#### alignment_trimmer.py
##


import sys
import os
import getopt

try:
	opts, args = getopt.getopt(sys.argv[1:], 'i:o:m:Rh', ['input_file=', 'output_file=', 'min_midgap_len=', 'RAWFASTA','help'])
																					 	
except getopt.GetoptError:
	print('ERROR getting options, please see help by specifing -h')
	sys.exit(2) ### close ofter error from try
	
	
arg_len = len(opts)

if arg_len == 0:
	print('No options provided. Please see help by specifing -h')
	sys.exit(2)

do_midgap_trim = 'NO' ## default not to do midgap trimming, unless specify a midgap len
infilespec = 'NO'
outfilespec = 'NO'
do_rawfasta = 'NO'

#print (opts) ## see args
for opt, arg in opts:
	if opt in ('-h', '--help'):
		print("\n**** alignment_trimmer.py | Written by DJP, 18/07/16 in Python 3.5 in Lausanne, Swiss ****\n")
		print("This program takes an alignment file as input") 
		print("It trims alignments to remove regions with gaps in two main ways")
		print("\t1: it trims gaps from the ends of the alignment")
		print("\t2: (OPTIONAL) it trims gaps from inside the alignment iteratively, starting with the closest to the end of the alignment (greater than minimum gapsize), until no gaps larger than minimum gapsize")
		print("It outputs a trimmed alignment file and a .stats.csv file")
		print("\nNOTE: gaps should be encoded as '-'")
		print("\n**** USAGE **** \n")
		print("alignment_trimmer.py -i [fasta alignment file] -o [name of out file] [options] \n")
		print("OPTIONS")
		print("-m\tminimum gapsize to be kept in for internal gaps. Note specifing this parameter causes interior-gap trimming to be switched on (default off)")
		print("-R\tOutput kept alignment region WITHOUT gap characters ('-') i.e. output trimmed, unaligned seq. Unaligned seqs are outputted to *_without_gaps.fa (default off)")
		
		
		print("\n**** EXAMPLES  ****\n")
	
		
		print("example_align_file_test.fa:")
		
		print(">seq1")
		print("AAAGGGGGGGGGGGGGGGGGGGGGAGAGACACGGCAGCAGCGCAGCGCAGCGCGCGAGCAGCCAGGCACGACGAGCACGCGACGAC-----")
		print(">seq13")
		print("AAAGGGGG------GGGGGGGGGGAGAGACACGGCAGCAGCGCAGCGCAGCGCGCGAGCAGCCAGGCACGACGAGCACGCGACGACGACGA")
		print(">seq14")
		print("---GGGGGGGGGGGGGGGGGGGAGAGACACGGCAGCAGCGC----CGCAGCGCGCGAGCAGCCAGG------GAGCACGCGACGACGACGA")
		
		
		print("\n**** EXAMPLE 1 - end-trimming only  ****\n")
		print("alignment_trimmer.py -i example_align_file_test.fa -o outfile1.fa")
		
		print("\noutfile1.fa:")
		print(">seq1")
		print("GGGGGGGGGGGGGGGGGGGGGAGAGACACGGCAGCAGCGCAGCGCAGCGCGCGAGCAGCCAGGCACGACGAGCACGCGACGAC")
		print(">seq13")
		print("GGGGG------GGGGGGGGGGAGAGACACGGCAGCAGCGCAGCGCAGCGCGCGAGCAGCCAGGCACGACGAGCACGCGACGAC")
		print(">seq14")
		print("GGGGGGGGGGGGGGGGGGGAGAGACACGGCAGCAGCGC----CGCAGCGCGCGAGCAGCCAGG------GAGCACGCGACGAC")
		
		print("\n**** EXAMPLE 2 - end-trimming and trimming internal gaps  ****\n")
		print("alignment_trimmer.py -i example_align_file_test.fa -o outfile2.fa -m 5")
		
		print("\noutfile2.fa:")
		print(">seq1")
		print("GGGGGGGGGGAGAGACACGGCAGCAGCGCAGCGCAGCGCGCGAGCAGCCAGG")
		print(">seq13")
		print("GGGGGGGGGGAGAGACACGGCAGCAGCGCAGCGCAGCGCGCGAGCAGCCAGG")
		print(">seq14")
		print("GGGGGGGGAGAGACACGGCAGCAGCGC----CGCAGCGCGCGAGCAGCCAGG\n")
		
		

		sys.exit(2)
	elif opt in ('-i', '--input_file'):
		infilespec = 'YES'
		seqF1 = arg
	elif opt in ('-o', '--output_file'):
		outfilespec = 'YES'
		outF1 = arg
	elif opt in ('-m', '--min_midgap_len'):
		do_midgap_trim = 'YES'
		smallest_gap_allow = arg
	elif opt in ('-R', '--RAWFASTA'):
		do_rawfasta = 'YES'
	else:
		print("i dont know")
		sys.exit(2)

if infilespec == 'NO':
	print("Please specify an input file! For more info see help with option -h")
	sys.exit(2)

if outfilespec == 'NO':
	print("Please specify an output file! For more info see help with option -h")
	sys.exit(2)

if do_midgap_trim == 'NO':
	print("\nNOTE: Only trimming gaps from the ends of the alignment. Gaps in the interior of the alignment are kept as -m option not specified\n")
	
##### FIRST unwrap fasta - precautionary will be necessary for some files 
### note making a temp unwrapped fasta file  - removed at end
output_fasta_name = seqF1 + ".TEMP_extract_fasta_file" 

output_file = open(output_fasta_name, "w")
#print("Unwrapping fasta file\n")
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

seq_length = 0 ### will be the same for all seqs as they are aligned

done = 0
seq_file_1 = open(output_fasta_name)
for line in seq_file_1:
	lineA = line.rstrip("\n")
	if lineA.startswith(">"):
		lineB = lineA.replace(">", "")
		name_list.append(lineB)
	else:
		seq_list.append(lineA)
		seq_length = len(lineA)
		done = done + 1
		done_divide = done / 1000
		if done_divide.is_integer():
			print("Read " + str(done) + " sequences from " + seqF1)


for element in range(0,len(name_list)):
	name1 = name_list[element]
	seq1 = seq_list[element]
	seq_dict[name1] = seq1

seq_N = str(len(name_list))

#print ("\nLoaded " + seq_N + " seqeunces from " + seqF1 + ".\n")
	
	
## tidyup
seq_file_1.close()
os.remove(output_fasta_name)
#print("\nFinished\n")

###########################################################################################################################
## end-gaptrimming function
## function to trim off alingment gaps from the ends a set of sequences
## returns a trimmed dict
	
import re

def end_trimmer(seq_dicty):

	trim_from_start = 0
	trim_from_end = seq_length
	
	#print(trim_from_end)
	
	
	for el in seq_dicty:
		seq = seq_dicty.get(el)
		start_gap = re.search('^--*', seq) #### matches if there is a gap (-) at the start of the seq
		end_gap = re.search('--*$', seq) #### matches if there is a gap (-) at the start of the seq

		if start_gap != None:
			end_of_start_gap_match = start_gap.end()
			if end_of_start_gap_match > trim_from_start:
				trim_from_start = end_of_start_gap_match

		if end_gap != None:
			start_of_end_gap_match = end_gap.start()
			if start_of_end_gap_match < trim_from_end:
				trim_from_end = start_of_end_gap_match 
	
	trimmed_seqs = {}
	for el in seq_dicty:
		seq = seq_dicty.get(el)
		trimmed_seq = seq[trim_from_start:trim_from_end]
		trimmed_seqs[el] = trimmed_seq
		
	return trimmed_seqs


############################################################################################################################################################
#### mid gap trimming function


## function to trim alingment gaps from the middle a set of sequences
## returns a trimmed dict

import numpy as np


def mid_trimmer(seq_dicty1, allowed_size):
	
	
	allow_sz = int(allowed_size)
	gap_dict = {} ### uniq dict of gaps
	
	done = set()
	seq_len = 0
	for el2 in seq_dicty1:
		seq = seq_dicty1.get(el2)
		seq_len = len(seq)
		mid_gaps = re.finditer('--*', seq) ### finds all matches
		gap_n = 0
		for el in mid_gaps:
			if str(el) not in done:
				done.add(str(el))
				gap_n = gap_n + 1
				start1 = el.start()
				end1 = el.end()
				mid_size = el.end() - el.start()
				mid_size_half = mid_size  / 2
				gap_mid_point = start1 + mid_size_half
				gap_mid_point2 = int(np.ceil(gap_mid_point)) #### round up
				bases_from_end = seq_len - gap_mid_point2
				game_name = "Gap_" + str(gap_n) + "_" + el2
				gap_dict[game_name] = [start1, end1, mid_size, gap_mid_point2, bases_from_end]
		
	
	#### get list of gaps > than allowed size
	
	
	gaps_bigger_than_allow = []
	uniq_endpoints = set()
	for el in gap_dict:
		gapinfo = gap_dict.get(el)
		mid_size = gapinfo[2]
		if mid_size > allow_sz:
			gaps_bigger_than_allow.append(el)
	
	
	
	### find what the closest to the end is 
	
	closest = seq_len + 100
	for el in gaps_bigger_than_allow:
		gapinfo = gap_dict.get(el)
		mid_size = gapinfo[2]
		dist_from_s = gapinfo[0]
		dist_from_e = gapinfo[4]
		smallest_dist = seq_len + 100
		if dist_from_s > dist_from_e:
			smallest_dist = dist_from_e
		else:
			smallest_dist = dist_from_s
		
		if smallest_dist < closest:
			closest = smallest_dist
	
	

	closest_list = []
	for el in gaps_bigger_than_allow:
		gapinfo = gap_dict.get(el)
		mid_size = gapinfo[2]
		dist_from_s = gapinfo[0]
		dist_from_e = gapinfo[4]
		smallest_dist = seq_len + 100
		if dist_from_s > dist_from_e:
			smallest_dist = dist_from_e
		else:
			smallest_dist = dist_from_s
		
		if smallest_dist == closest:
			closest_list.append(el)
	
	
	### of the closest gaps how big is the largest?
	
	biggest_gap = 0
	for el in closest_list:
		gapinfo = gap_dict.get(el)
		mid_size = gapinfo[2]
		if mid_size > biggest_gap:
			biggest_gap = mid_size 

	
	closest_biggest = []
	for el in closest_list:
		gapinfo = gap_dict.get(el)
		mid_size = gapinfo[2]
		if mid_size == biggest_gap:
			closest_biggest.append(el)

	
	gap_to_do = ""
	
	#### if two eqidist for end same size gaps - pick one at 3 prime end
	
	nearest_3prime = 0
	if len(closest_biggest) > 1:
		for el in closest_biggest:
			gapinfo = gap_dict.get(el)
			endcord = gapinfo[1]
			if endcord > nearest_3prime:
				nearest_3prime = endcord
		
		for el in closest_biggest:
			gapinfo = gap_dict.get(el)
			endcord = gapinfo[1]
			if endcord == nearest_3prime:
				gap_to_do = el
	else:
		gap_to_do = closest_biggest[0]	
				

	#print (gap_to_do)
	
	trimmed_mid_seqs = {}
	for el in seq_dicty1:
		seq = seq_dicty1.get(el)
		mid_seq_len = seq_len / 2
		gapinfo = gap_dict.get(gap_to_do)
		gapsta = gapinfo[0]
		gapend = gapinfo[1]
		midpoint = gapinfo[3]
		if midpoint > mid_seq_len:
			trimmed_seq = seq[0:gapsta]
			trimmed_mid_seqs[el] = trimmed_seq
		elif midpoint < mid_seq_len:
			trimmed_seq = seq[gapend:seq_len]
			trimmed_mid_seqs[el] = trimmed_seq
		elif midpoint == mid_seq_len: ### if equal - trim 3' end
			trimmed_seq = seq[0:gapsta]
			trimmed_mid_seqs[el] = trimmed_seq
		else:
			print("ERROR")
	
	#print(trimmed_mid_seqs)
		
	return trimmed_mid_seqs
	
	

	
	
	
####################################################################################################################################################################################
###	Trimming proper
####################################################################################################################################################################################
### so I found that i want to interate this as after the first trim I might still have alingment gaps at the end after a single trim:
### ATTATATTACAGGA------AA
### ATTATATTACAGGAA-----AA
### ATTATATTACAGGAGG------

## will trim to:

### ATTATATTACAGGA--
### ATTATATTACAGGAA-
### ATTATATTACAGGAGG

## on the first iter 

## after a second: 

### ATTATATTACAGGA
### ATTATATTACAGGA
### ATTATATTACAGGA

### Trim while gaps at the ends of any sequence:

## make a copy to trim (just want to keep origs)

trimmed_dict_1 = seq_dict

need_to_end_trim = "YES"

while (need_to_end_trim == "YES"):
	trimmed_dict_1 = end_trimmer(trimmed_dict_1)
	#print("it")
	gap_set = set()
	#print (gap_set)
	for seqname in trimmed_dict_1:
		seq = trimmed_dict_1.get(seqname)
		start_gap = re.search('^--*', seq) #### matches if there is a gap (-) at the start of the seq
		end_gap = re.search('--*$', seq) #### matches if there is a gap (-) at the start of the seq
		gap_set.add(start_gap)
		gap_set.add(end_gap)
	gap_set_len = len(gap_set)
	if gap_set_len > 1:
		need_to_end_trim = "YES"
	else:
		need_to_end_trim = "NO"
	#print (gap_set)

#print(trimmed_dict_1)


	
if do_midgap_trim == "YES":
	
	##################################################################################################################
	### mid-trimming
	smallest_midgap_allowed = int(smallest_gap_allow) 
	
	### making a copy of the end trimmed one
	trimmed_dict_2 = trimmed_dict_1
	
	need_to_end_trim = "YES"
	
	### first loop to check if ANY midgaps are larger than the minimim
	largest_midgap = 0
	for el in trimmed_dict_2:
		seq = trimmed_dict_2.get(el)
		mid_gaps = re.finditer('--*', seq) ### finds all matches
		for el in mid_gaps:
			mid_size = el.end() - el.start()
			if mid_size > largest_midgap:
				largest_midgap = mid_size
	if largest_midgap > smallest_midgap_allowed:
		need_to_end_trim = "YES"
	else:
		need_to_end_trim = "NO"
	
	### if so proceed to iterative trimming
	
	while (need_to_end_trim == "YES"):
		trimmed_dict_2 = mid_trimmer(trimmed_dict_2, smallest_midgap_allowed)
		#print("it")
		largest_midgap = 0
		for el in trimmed_dict_2:
			seq = trimmed_dict_2.get(el)
			mid_gaps = re.finditer('--*', seq) ### finds all matches
			for el in mid_gaps:
				mid_size = el.end() - el.start()
				if mid_size > largest_midgap:
					largest_midgap = mid_size
		if largest_midgap > smallest_midgap_allowed:
			need_to_end_trim = "YES"
		else:
			need_to_end_trim = "NO"
	
	
	#################################################################################################################
	### trim ends again as when doing mid-trim, may? in some circumstaces leave gaps at the end

	trimmed_dict_3 = trimmed_dict_2
	
	need_to_end_trim = "YES"
	
	while (need_to_end_trim == "YES"):
		trimmed_dict_3 = end_trimmer(trimmed_dict_3)
		#print("it")
		gap_set = set()
		#print (gap_set)
		for seqname in trimmed_dict_3:
			seq = trimmed_dict_3.get(seqname)
			start_gap = re.search('^--*', seq) #### matches if there is a gap (-) at the start of the seq
			end_gap = re.search('--*$', seq) #### matches if there is a gap (-) at the start of the seq
			gap_set.add(start_gap)
			gap_set.add(end_gap)
		gap_set_len = len(gap_set)
		if gap_set_len > 1:
			need_to_end_trim = "YES"
		else:
			need_to_end_trim = "NO"
	
	aling_len = 0
	end_trimmed_seq_len = 0
	seq3_lens = []
	
	### output trimmed sequences 
	out_file = open(outF1, 'w')
	for el in name_list:
		end_trimmed_seq = trimmed_dict_1.get(el)
		end_trimmed_seq_len = len(end_trimmed_seq)
		seq3 = trimmed_dict_3.get(el)
		aling_len = len(seq3)
		gaps_remaining = seq3.count("-")
		seq_len = aling_len - gaps_remaining
		seq3_lens.append(seq_len)
		out_file.write(">" +  el + "\n" + seq3 + "\n" )
	
	
	
	#### stats
	
	stats_out_name = outF1 + ".trimming.stats.csv"
	
	seq3_lens_sorted = sorted(seq3_lens)
	shortest_seq = seq3_lens_sorted[0]
	longest_seq = seq3_lens_sorted[-1]
	seq_len_range = longest_seq - shortest_seq 
	align_prop = round(aling_len / seq_length * 100, 1)
	
	statout_file = open(stats_out_name , 'w')
	statout_file.write("Filename,orig_aling_len,after_end_trim,after_all_trim,%alignremaining,shortest_seq,longest_seq,seq_len_diff\n")
	statout_file.write(seqF1 + "," + str(seq_length) + "," + str(end_trimmed_seq_len) + "," + str(aling_len) + "," + str(align_prop) + "," + str(shortest_seq) + "," + str(longest_seq) + "," + str(seq_len_range) + "\n")
	
	
	### output aligned region without gaps in 
	if do_rawfasta == 'YES':
		out_file = open(outF1 + "_without_gaps.fa", 'w')
		for el in name_list:
			end_trimmed_seq = trimmed_dict_1.get(el)
			end_trimmed_seq_len = len(end_trimmed_seq)
			seq3 = trimmed_dict_3.get(el)
			seq4 = seq3.replace("-", "")
			out_file.write(">" +  el + "\n" + seq4 + "\n" )
		
	
	# for el in name_list:
	# 	seq = seq_dict.get(el)
	# 	seq2 = trimmed_dict_1.get(el)
	# 	seq3 = trimmed_dict_3.get(el)
	# 	#print ("ORIG" + "\n" + seq )
	# 	print ("END" + "\n" + seq2 )
	# 	print ("TRIMMED2" + "\n" + seq3 )


elif do_midgap_trim == "NO":
	### output trimmed sequences 
	
	aling_len = 0
	seq3_lens = []
	
	out_file = open(outF1, 'w')
	for el in name_list:
		seq3 = trimmed_dict_1.get(el)
		aling_len = len(seq3)
		gaps_remaining = seq3.count("-")
		seq_len = aling_len - gaps_remaining
		seq3_lens.append(seq_len)
		out_file.write(">" +  el + "\n" + seq3 + "\n" )
	
	#### stats
	
	stats_out_name = outF1 + ".trimming.stats.csv"
	
	seq3_lens_sorted = sorted(seq3_lens)
	shortest_seq = seq3_lens_sorted[0]
	longest_seq = seq3_lens_sorted[-1]
	seq_len_range = longest_seq - shortest_seq 
	align_prop = round(aling_len / seq_length * 100, 1)
	
	
	
	statout_file = open(stats_out_name , 'w')
	statout_file.write("Filename,orig_aling_len,after_end_trim,%alignremaining,shortest_seq,longest_seq,seq_len_diff\n")
	statout_file.write(seqF1 + "," + str(seq_length) + "," + str(aling_len) + "," + str(align_prop) + "," + str(shortest_seq) + "," + str(longest_seq) + "," + str(seq_len_range) + "\n")
	
	
	### output aligned region without gaps in 
	if do_rawfasta == 'YES':
		out_file = open(outF1 + "_without_gaps.fa", 'w')
		for el in name_list:
			seq3 = trimmed_dict_1.get(el)
			seq4 = seq3.replace("-", "")
			out_file.write(">" +  el + "\n" + seq4 + "\n" )
	
		
	#print(str(seq_length) + "," + str(aling_len) + "," + str(align_prop) + "," + str(shortest_seq) + "," + str(longest_seq) + "," + str(seq_len_range))
		
	
	# for el in name_list:
	# 	seq = seq_dict.get(el)
	# 	seq2 = trimmed_dict_1.get(el)
	# 	print ("ORIG" + "\n" + seq )
	# 	print ("TRIMMED" + "\n" + seq2 )


else:
	print("Error with setting midgap trimming")

print("\nFinished, Don Rumata.\n")
