[![Build Status](https://travis-ci.org/tleonardi/bedparse.svg?branch=master)](https://travis-ci.org/tleonardi/bedparse)

# Bedparse
Bedparse is a simple python module and CLI tool to perform common operations on BED files.

It offers the following functionality:
* Filtering of transcripts based on annotations
* Joining of annotation files based on transcript names
* Conversion from GTF to BED format
* Conversion from UCSC to Ensembl chromosome names (and viceversa)
* Conversion from bed12 to bed6
* Promoter reporting
* Intron reporting
* CDS reporting
* UTR reporting 

## Motivation
The BED (Browser Extensible Data) format is a plain text file format commonly used in bioinformatics to represent genomic features (e.g. genes, transcripts, peaks, regulatory regions, etc.). Each line in the file represents a genomic feature and consists of up to 12 tab-separated fields that specify:
1. chromosome name
2. start coordinate in the chromosome
3. end coordinate in the chromosome
4. feature name
5. feature score
6. strand
7. thick start (conventionally the start codon for protein coding transcripts)
8. thick end (conventionally the stop codon for protein coding transcripts)
9. rgb color for visualisation in genome browsers
10. number of connected blocks (conventionally the number of exons)
11. comma separated list of blocks size
12. comma separated list of block starts relative to field 2 (i.e. genomic start of the feature)

One of the major advantages of the BED format over many of its alternatives is that each line includes all the information required to define an individual transcript. This characteristic allows to perform numerous operations on BED a file as part of unix pipe, for example using GNU awk. For example, the following is a common approach to extract gene promoters (here defined as 500bp around the gene start):

```
awk 'BEGIN{OFS=FS="\t"}{print $1,$2-500,$3+500,$4,$5}' transcritpome.bed > promoters.bed
```

If we wanted to do the same by taking the strand into account:

```
awk 'BEGIN{OFS=FS="\t"}{if($6=="+"){print $1,$2-500,$2+500,$4,$5}else{print $1,$3-500,$3+500,$4,$5}}' transcritpome.bed > promoters_stranded.bed
```

These operations, albeit conceptually simple, are long to type and prone to typos. Bedparse greatly simplifies the process:

```
bedparse promoter transcritpome.bed > promoters_stranded.bed
```
or

```
bedparse promoter --unstranded transcritpome.bed > promoters.bed
```
for disregarding the strand.

Internally, bedparse processes a bedfile line by line by instantiating objects of the bedline class. The bedline class implements an init() method that performs several checks on each field in order to ensure the correctness of the format, whereas the other methods of the class implement all the operations descrbied below (see functionality). Despite the simplicity of most of the operations supported by bedparse, all functions are thouroughly and rigourously tested through an automated test suit to ensure the accuracy and correctness of the results.
Additionally, bedparse also provides to conversion operations: gtf2bed allows converting Ensembl/Gencode Gene transfer format (GTF) files into bed format; convertChr implements an internal dictionary that allows conversion of human and mouse chrosome names between the two most widely used formats, i.e. the Ensembl and the UCSC naming schemes.

## Installation

```
pip install bedparse
```

## Usage

The basic syntax in the form: `bedparse subcommanda [parameters]`.

For a list of all subcommands and a brief explanation of what they do type: `bedparse --help`

For a detailed explanation of each subcommand and a list of its paramters use the `--help` options after the subcommanda name. E.g.: `bedparse promoter --help`

```
> bedparse --help
usage: bedparse [-h] [--version]
                {3pUTR,5pUTR,cds,promoter,introns,filter,join,gtf2bed,bed12tobed6,convertChr}
                ...

Perform various simple operations on BED files.

positional arguments:
  {3pUTR,5pUTR,cds,promoter,introns,filter,join,gtf2bed,bed12tobed6,convertChr}
                        sub-command help
    3pUTR               Prints the 3' of coding genes.
    5pUTR               Prints the 5' of coding genes.
    cds                 Prints the CDS of coding genes.
    promoter            Prints the promoters of transcripts.
    introns             Prints BED records corresponding to the introns of
                        each transcript in the original file.
    filter              Filters a BED file based on an annotation.
    join                Joins a BED file with an annotation file using the BED
                        name (col4) as the joining key.
    gtf2bed             Converts a GTF file to BED12 format.
    bed12tobed6         Converts a BED12 file to BED6 format
    convertChr          Convert chromosome names between UCSC and Ensembl
                        formats

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
```


### 3'/5' UTRs
This commands report the 5' or 3' UTRs of each coding transcript in the BED file. The UTRs are defined as the regions between transcript start/end and CDS start/end (the CDS, in turn, is defined as the region between thickStart and thickEnd). Transcripts with an undefined CDS (i.e. with thickStart and thickEnd set to the same value) are not reported.

```
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse 3pUTR transcripts.bed 
chr1	167787921	167790819	ENST00000392121.7	0	+	167787921	167787921	0	1	2898,	0,

```
### CDS
Report the CDS of each coding transcript in the BED file. Transcripts with distinct values of thickStart and thickEnd are considered coding. Transcripts without CDS are not reported." 

```
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse cds transcripts.bed 
chr1	167722151	167787921	ENST00000392121.7	0	+	167722151	167787921	0	3	91,167,102,	0,43431,65668,
```



### Promoters
This command reports the promoter of each transcript in the input BED file. The promoter is defined as a fixed interval around the TSS.                                                                                                     

```
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse promoter transcripts.bed 
chr1	167721488	167722488	ENST00000392121.7

> bedparse promoter --up 100 --down 100 transcripts.bed 
chr1	167721888	167722088	ENST00000392121.7
```


### Introns
Reports BED12 lines corresponding to the introns of each transcript. Unspliced transcripts are not reported.

```
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse introns transcripts.bed 
chr1	167722242	167787819	ENST00000392121.7	0	+	167722242	167722242	0	2	43340,22070,	0,43507,
```


### Filter
Filters a BED file based on an annotation file. BED entries with a name (i.e. col4) that appears in the specified column of the annotation are printed to stdout. For efficiency reasons this command doesn't perform BED validation.

```
> cat transcripts.bed 
chr1	67092164	67231852	ENST00000371007.6	0	-
chr1	67092175	67127261	ENST00000371006.5	0	-
chr1	67092175	67127261	ENST00000475209.6	0	-
chr1	67092394	67134970	ENST00000371004.6	0	-
chr1	67092396	67127261	ENST00000621590.4	0	-
chr1	67092947	67134977	ENST00000544837.5	0	-
chr1	67093558	67231853	ENST00000448166.6	0	-
chr1	67096295	67134977	ENST00000603691.1	0	-
chr1	201283451	201332993	ENST00000263946.7	0	+
chr1	201283451	201332993	ENST00000367324.7	0	+

> cat filter.txt 
GeneX	ENST00000263946.7	Other_field
GeneY	ENST00000367324.7	Another_field

> bedparse filter --annotation filter.txt --column 2 transcripts.bed 
chr1	201283451	201332993	ENST00000263946.7	0	+
chr1	201283451	201332993	ENST00000367324.7	0	+
```


### Join
Adds the content of an annotation file to a BED file as extra columns. The two files are joined by matching the BED Name field (column 4) with a user-specified field of the annotation file. 

```
> cat transcripts.bed
chr1	67092164	67231852	ENST00000371007.6	0	-
chr1	67092175	67127261	ENST00000371006.5	0	-
chr1	67092175	67127261	ENST00000475209.6	0	-
chr1	67092394	67134970	ENST00000371004.6	0	-
chr1	67092396	67127261	ENST00000621590.4	0	-
chr1	67092947	67134977	ENST00000544837.5	0	-
chr1	67093558	67231853	ENST00000448166.6	0	-
chr1	67096295	67134977	ENST00000603691.1	0	-
chr1	201283451	201332993	ENST00000263946.7	0	+
chr1	201283451	201332993	ENST00000367324.7	0	+

> cat annotation.txt
GeneX	ENST00000263946.7	Other_field
GeneY	ENST00000367324.7	Another_field

> bedparse join --column 2 --annotation annotation.txt transcripts.bed
chr1	67092164	67231852	ENST00000371007.6	0	-	.
chr1	67092175	67127261	ENST00000371006.5	0	-	.
chr1	67092175	67127261	ENST00000475209.6	0	-	.
chr1	67092394	67134970	ENST00000371004.6	0	-	.
chr1	67092396	67127261	ENST00000621590.4	0	-	.
chr1	67092947	67134977	ENST00000544837.5	0	-	.
chr1	67093558	67231853	ENST00000448166.6	0	-	.
chr1	67096295	67134977	ENST00000603691.1	0	-	.
chr1	201283451	201332993	ENST00000263946.7	0	+	GeneX	Other_field
chr1	201283451	201332993	ENST00000367324.7	0	+	GeneY	Another_field

> bedparse join --column 2 --annotation annotation.txt --noUnmatched transcripts.bed 
chr1	201283451	201332993	ENST00000263946.7	0	+	GeneX	Other_field
chr1	201283451	201332993	ENST00000367324.7	0	+	GeneY	Another_field

```

# Convert GTF to BED
Converts a GTF file to BED12 format. This tool supports the Ensembl GTF format. The GTF file must contain 'transcript' and 'exon' features in field 3. If the GTF file also annotates 'CDS' 'start_codon' or 'stop_codon' these are used to annotate the thickStart and thickEnd in the BED file.

# Convert BED12 to BED6
Convert the BED12 format into BED6 by reporting a separate line for each block of the original record. 

```
> cat transcripts.bed 
chr1	67092164	67231852	ENST00000371007.6	0	-	67093004	67127240	0	8	1440,187,70,113,158,92,86,7,	0,3070,4087,23187,33587,35001,38977,139681,

> bedparse bed12tobed6 transcripts.bed 
chr1	67092164	67093604	ENST00000371007.6	0	-
chr1	67095234	67095421	ENST00000371007.6	0	-
chr1	67096251	67096321	ENST00000371007.6	0	-
chr1	67115351	67115464	ENST00000371007.6	0	-
chr1	67125751	67125909	ENST00000371007.6	0	-
chr1	67127165	67127257	ENST00000371007.6	0	-
chr1	67131141	67131227	ENST00000371007.6	0	-
chr1	67231845	67231852	ENST00000371007.6	0	-
```

# Convert chromosome names
Convert chromosome names between UCSC and Ensembl formats. The conversion supports the hg38 assembly up to patch 11 and the mm10 assembly up to patch 4. By default patches are not converted (because the UCSC genome browser does not support them), but can be enabled using the -p flag. When the BED file contains a chromsome that is not recognised, by default the program stops and throws an error. Alternatively, unrecognised chrosomes can be suppressed (-s) or artificially set to 'NA' (-a).

```
> cat transcripts.bed 
chr1	67092164	67231852	ENST00000371007.6	0	-
chr22_KI270928v1_alt	137191	137686	ENST00000630841.1	0	-
chr1_KI270706v1_random	45985	46062	ENST00000611371.2	0	+
chrM	3229	3304	ENST00000386347.1	0	+

> bedparse convertChr --assembly hg38 --target ens transcripts.bed 
1	67092164	67231852	ENST00000371007.6	0	-
CHR_HSCHR22_3_CTG1	137191	137686	ENST00000630841.1	0	-
KI270706.1	45985	46062	ENST00000611371.2	0	+
MT	3229	3304	ENST00000386347.1	0	+
```
