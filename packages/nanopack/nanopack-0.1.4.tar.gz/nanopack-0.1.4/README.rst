NANOPACK
========

Easily install all my Oxford Nanopore processing and analysis scripts at
the same time.

Installation
------------

``pip install nanopack`` ## Updating ``pip install nanopack --upgrade``

Scripts
-------

**`NanoPlot <https://github.com/wdecoster/NanoPlot>`__**: creating many
relevant plots derived from reads (fastq), alignments (bam) and albacore
summary files. Examples can be found in `the gallery on my
blog <https://gigabaseorgigabyte.wordpress.com/2017/06/01/example-gallery-of-nanoplot/>`__.

**`NanoFilt <https://github.com/wdecoster/nanofilt>`__**: Streaming
script for filtering a fastq file based on a minimum length and minimum
quality cut-off. Also trimming nucleotides from either read ends is an
option.

**`NanoStat <https://github.com/wdecoster/nanostat>`__**: Quickly create
a statistical summary from reads, an alignment or a summary file

**`NanoLyse <https://github.com/wdecoster/nanolyse>`__**: Streaming
script for filtering a fastq file to remove reads mapping to the lambda
phage genome (control DNA used in nanopore sequencing). Uses
`minimap2/mappy <https://github.com/lh3/minimap2>`__.

Modules
-------

**`nanoget <https://github.com/wdecoster/nanoget>`__**: Functions for
extracting features from reads, alignments and albacore summary data.

**`nanomath <https://github.com/wdecoster/nanomath>`__**: Functions for
mathematical processing and calculating statistics

**`nanoplotter <https://github.com/wdecoster/nanoplotter>`__**:
Appropriate plotting functions, heavily using the seaborn module
