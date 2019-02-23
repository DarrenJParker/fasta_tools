## Scripts

* **alignment_trimmer.py** |  This program takes an alignment file as input. It trims alignments to remove regions with gaps in two main ways 
    * it trims gaps from the ends of the alignment 
    * it trims gaps from inside the alignment iteratively, starting with the closest to the end of the alignment (greater than minimum gapsize), until there are no gaps larger than minimum gapsize 

## Running alignment_trimmer.py

* To see options of running alignment_trimmer.py see the help file using: `python3 alignment_trimmer.py -h`

* To run alignment_trimmer.py on a bunch of alignment files, just use a simple bash for loop (here with the test data):

```
# from the fasta_tool directory:

## first make an output dir 
mkdir Alignment_trimming/output_trim

# run a for loop
for i in Alignment_trimming/test_data/*.fa; do
        foo1=`echo "$i" | sed 's/\.fa//'`
        foo2=`echo $foo1"_Trimmed.fa" | sed 's/.*\///'`
        foo2_out=`echo "./Alignment_trimming/output_trim/"$foo2`
        echo $foo2_out
        python3 Alignment_trimming/alignment_trimmer.py -i $i -o $foo2_out -m 3 -R
done
```

# Why should I trim my alignments before RNA-seq analysis?

(So I here I am imagining a situation where you have 1-to-1 orthologous sequences from related species, and want to compare expression differences)

Count-based methods for detecting DE (such as edgeR, DESeq) assume that features being compared are the same length in the conditions being compared. If you violate this assumption you will run into problems. As an example let's imagine a situation where we have a gene that is twice as long in one condition (e.g. species) as in the other but with the same expression level (Fig. 1).

<img src="https://github.com/DarrenJParker/fasta_tools/blob/master/Alignment_trimming/Figs_for_readme/Fig1.png" width="500">

**Fig 1** | Reads mapping to a gene with different lengths in two conditions.

Since the gene is twice as long in condition 1 vs condition 2, we will map twice as many reads to it. Since edgeR doesn't know this it will think that the expression level of the gene is twice as high in condition 1.

Now we could just correct for length here (and there are a bunch of ways to do this) which would give us what we want (in Fig 1: 48/4 = 12, 24/2 = 12). The problem is that the situation in Fig. 1 is an idealised situation. Typically reads do not map equally across a gene (for lots of reasons), so we may actually have a situation like that shown in Fig 2 (where reads are harder to map the yellow and red parts of the gene). Again we have equal expression, but because reads are not distributed equally when we correct for length we end up with expression seeming higher in condition 2.

<img src="https://github.com/DarrenJParker/fasta_tools/blob/master/Alignment_trimming/Figs_for_readme/Fig2.png" width="500">

**Fig 2** | Reads mapping to a gene with different lengths in two conditions - with simple length correction.

So I think the best way to make things comparable is to make sure that you are using the same region of a gene in each treatment (Fig. 3)

<img src="https://github.com/DarrenJParker/fasta_tools/blob/master/Alignment_trimming/Figs_for_readme/Fig3.png" width="500">

**Fig 3** | Reads mapping to a gene with different lengths in two conditions - after alignment trimming.


And how do we do this?

1. Take the gene (transcript) sequence from each condition and align them.
2. Use alignment_trimmer.py to trim the alignments (use python3 alignment_trimmer.py, see above for usage)

