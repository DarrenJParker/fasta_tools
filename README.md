# fasta_tools

If you use any of the scripts in this repositoy please cite it as follows:

Parker, D. J. (2016). fasta_tools. Zenodo. https://zenodo.org/record/59775

NOTE: help messages can be displayed for all scripts by running them without any arguments provided (i.e. python [name of script]) or specifying -h (python [name of script] -h) .
All scripts written in python3.4 or higher.

## generic scripts

Some basic scripts for commonly performed tasks on fasta files.

* extract_fasta_v0.3.py | extract fasta seqs specified by name (or select all but those specified (invert option))
* unwrap_fasta.py | unwrap a wrapped fasta file 
* fasta_select_by_len | select seqs of specified length (less-than, greater-than, or range) 
* fasta_len_0.2.py | calc min, min length, max length, mean length, N50, and base comp of fasta sequences 
* fasta_len_all_seqs.py | get len of all seqs
* fasta_remove_duplicate_sequences.py | removes duplicate sequences from a fasta file.

## Alignments

* alignment_base_split.py | takes a fasta alignments as input, and outputs 3 fasta alignments each a different position (1,2,3)
* alignment_concat.py takes a number of separate fasta file alignments as input, and concats them 
* [Trimming alignments](Alignment_trimming)
