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

