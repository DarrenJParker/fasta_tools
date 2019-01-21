* **alignment_trimmer.py** |  This program takes an alignment file as input. It trims alignments to remove regions with gaps in two main ways 
    * it trims gaps from the ends of the alignment 
    * it trims gaps from inside the alignment iteratively, starting with the closest to the end of the alignment (greater than minimum gapsize), until there are no gaps larger than minimum gapsize 
