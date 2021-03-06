## Usage
```text
usage: bedparse [-h] [--version]
                {3pUTR,5pUTR,cds,promoter,introns,filter,join,gtf2bed,bed12tobed6,convertChr,validateFormat}
                ...

Perform various simple operations on BED files.

positional arguments:
  {3pUTR,5pUTR,cds,promoter,introns,filter,join,gtf2bed,bed12tobed6,convertChr,validateFormat}
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
    validateFormat      Check whether the BED file adheres to the BED format
                        specifications

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
```

The basic syntax in the form: `bedparse sub-command [parameters]`.

For a list of all sub-commands and a brief explanation of what they do, use: `bedparse --help`

For a detailed explanation of each subcommand and a list of its parameters, use the `--help` option after the subcommand's name, e.g.: `bedparse promoter --help`

---

### 3'/5' UTRs

#### Usage
```text
> bedparse 3pUTR --help
usage: bedparse 3pUTR [-h] [bedfile]
```

Report the 5' or 3' UTRs of each coding transcript in the BED file. 

UTRs are defined as the region between transcript start/end and CDS start/end (the CDS is in turn defined as the region between thickStart and thickEnd).

Transcripts with an undefined CDS (i.e. with thickStart and thickEnd set to the same value) are not reported.

#### Examples
```text
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse 3pUTR transcripts.bed 
chr1	167787921	167790819	ENST00000392121.7	0	+	167787921	167787921	0	1	2898,	0,

```

---

### CDS

#### Usage
```text
> bedparse cds --help
usage: bedparse cds [-h] [--ignoreCDSonly] [bedfile]

Report the CDS of each coding transcript (i.e. transcripts with distinct
values of thickStart and thickEnd). Transcripts without CDS are not reported.

positional arguments:
  bedfile          Path to the BED file.

optional arguments:
  -h, --help       show this help message and exit
  --ignoreCDSonly  Ignore transcripts that only consist of CDS.
```

#### Examples
```text
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse cds transcripts.bed 
chr1	167722151	167787921	ENST00000392121.7	0	+	167722151	167787921	0	3	91,167,102,	0,43431,65668,
```

---

### Promoters
This command reports the promoter of each transcript in the input BED file. The promoter is defined as a fixed interval around the TSS.                                                                                                     

#### Usage
```text
> bedparse promoter --help
usage: bedparse promoter [-h] [--up UP] [--down DOWN] [--unstranded] [bedfile]

Report the promoter of each transcript, defined as a fixed interval around its
start.

positional arguments:
  bedfile       Path to the BED file.

  optional arguments:
    -h, --help    show this help message and exit
    --up UP       Get this many nt upstream of each feature.
    --down DOWN   Get this many nt downstream of each feature.
    --unstranded  Do not consider strands.
```

#### Examples
```text
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse promoter transcripts.bed 
chr1	167721488	167722488	ENST00000392121.7

> bedparse promoter --up 100 --down 100 transcripts.bed 
chr1	167721888	167722088	ENST00000392121.7
```

---

### Introns
Reports BED12 lines corresponding to the introns of each transcript. Unspliced transcripts are not reported.

#### Usage

```text
> bedparse introns --help
usage: bedparse introns [-h] [bedfile]

Report BED12 lines corresponding to the introns of each transcript. Unspliced
transcripts are not reported.

positional arguments:
  bedfile     Path to the BED file.

optional arguments:
  -h, --help  show this help message and exit
```

#### Examples
```text
> cat transcripts.bed 
chr1	167721988	167790819	ENST00000392121.7	0	+	167722151	167787921	0	3	254,167,3000,	0,43594,65831,

> bedparse introns transcripts.bed 
chr1	167722242	167787819	ENST00000392121.7	0	+	167722242	167722242	0	2	43340,22070,	0,43507,
```

---

### Filter
Filters a BED file based on an annotation file. BED entries with a name (i.e. col4) that appears in the specified column of the annotation are printed to stdout. For efficiency reasons this command doesn't perform BED validation.

#### Usage

```text
> bedparse filter --help
usage: bedparse filter [-h] --annotation ANNOTATION [--column COLUMN]
                       [--inverse]
                       [bedfile]

Filters a BED file based on an annotation. BED entries with a name (i.e. col4)
that appears in the specified column of the annotation are printed to stdout.
For efficiency reasons this command doesn't perform BED validation.

positional arguments:
  bedfile               Path to the BED file.

optional arguments:
  -h, --help            show this help message and exit
  --annotation ANNOTATION, -a ANNOTATION
                        Path to the annotation file.
  --column COLUMN, -c COLUMN
                        Column of the annotation file (1-based, default=1).
  --inverse, -v         Only report BED entries absent from the annotation
                        file.
```

#### Examples
```text
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

---

### Join
Adds the content of an annotation file to a BED file as extra columns. The two files are joined by matching the BED Name field (column 4) with a user-specified field of the annotation file. 

#### Usage

```text
> bedparse join --help
usage: bedparse join [-h] --annotation ANNOTATION [--column COLUMN]
                     [--separator SEPARATOR] [--empty EMPTY] [--noUnmatched]
                     [bedfile]

Adds the content of an annotation file to a BED file as extra columns. The two
files are joined by matching the BED Name field (column 4) with a user-
specified field of the annotation file.

positional arguments:
  bedfile               Path to the BED file.

optional arguments:
  -h, --help            show this help message and exit
  --annotation ANNOTATION, -a ANNOTATION
                        Path to the annotation file.
  --column COLUMN, -c COLUMN
                        Column of the annotation file (1-based, default=1).
  --separator SEPARATOR, -s SEPARATOR
                        Field separator for the annotation file (default tab)
  --empty EMPTY, -e EMPTY
                        String to append to empty records (default '.').
  --noUnmatched, -n     Do not print unmatched lines.
```

#### Examples
```text
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

---

### Convert GTF to BED
Converts a GTF file to BED12 format. This tool supports the Ensembl GTF format. The GTF file must contain 'transcript' and 'exon' features in field 3. If the GTF file also annotates 'CDS' 'start_codon' or 'stop_codon' these are used to annotate the thickStart and thickEnd in the BED file.

#### Usage
```text
> bedparse gtf2bed --help
usage: bedparse gtf2bed [-h] [--extraFields EXTRAFIELDS]
                        [--filterKey FILTERKEY] [--filterType FILTERTYPE]
                        [gtf]

Converts a GTF file to BED12 format. This tool supports the Ensembl GTF
format. The GTF file must contain 'transcript' and 'exon' features in field 3.
If the GTF file also annotates 'CDS' 'start_codon' or 'stop_codon' these are
used to annotate the thickStart and thickEnd in the BED file.

positional arguments:
  gtf                   Path to the GTF file.

optional arguments:
  -h, --help            show this help message and exit
  --extraFields EXTRAFIELDS
                        Comma separated list of extra GTF fields to be added
                        after col 12 (e.g. gene_id,gene_name).
  --filterKey FILTERKEY
                        GTF extra field on which to apply the filtering
  --filterType FILTERTYPE
                        Comma separated list of filterKey field values to
                        retain.
```

---

### Convert BED12 to BED6
Convert the BED12 format into BED6 by reporting a separate line for each block of the original record. 

#### Usage
```text
> bedparse bed12tobed6 --help
usage: bedparse bed12tobed6 [-h] [--appendExN] [--whichExon {all,first,last}]
                            [--keepIntrons]
                            [bedfile]

Convert the BED12 format into BED6 by reporting a separate line for each block
of the original record.

positional arguments:
  bedfile               Path to the GTF file.

optional arguments:
  -h, --help            show this help message and exit
  --appendExN           Appends the exon number to the transcript name.
  --whichExon {all,first,last}
                        Which exon to return. First and last respectively
                        report the first or last exon relative to the TSS
                        (i.e. taking strand into account).
  --keepIntrons         Add records for introns as well. Only allowed if
                        --whichExon all
```

#### Examples
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

---

### Convert chromosome names
Convert chromosome names between UCSC and Ensembl formats. The conversion supports the hg38 assembly up to patch 11 and the mm10 assembly up to patch 4. By default patches are not converted (because the UCSC genome browser does not support them), but can be enabled using the -p flag. When the BED file contains a chromosome that is not recognised, by default the program stops and throws an error. Alternatively, unrecognised chromosomes can be suppressed (-s) or artificially set to 'NA' (-a).

#### Usage
```text
> bedparse convertChr --help
usage: bedparse convertChr [-h] --assembly ASSEMBLY --target TARGET
                           [--allowMissing] [--suppressMissing] [--patches]
                           [bedfile]

Convert chromosome names between UCSC and Ensembl formats. The conversion
supports the hg38 assembly up to patch 11 and the mm10 assembly up to patch 4.
By default patches are not converted (because the UCSC genome browser does not
support them), but can be enabled using the -p flag. When the BED file
contains a chromosome that is not recognised, by default the program stops and
throws an error. Alternatively, unrecognised chromosomes can be suppressed
(-s) or artificially set to 'NA' (-a).

positional arguments:
  bedfile               Path to the BED file.

optional arguments:
  -h, --help            show this help message and exit
  --assembly ASSEMBLY   Assembly of the BED file (either hg38 or mm10).
  --target TARGET       Desidered chromosome name convention (ucsc or ens).
  --allowMissing, -a    When a chromosome name can't be matched between USCS
                        and Ensembl set it to 'NA' (by default thrown as
                        error).
  --suppressMissing, -s
                        When a chromosome name can't be matched between USCS
                        and Ensembl do not report it in the output (by default
                        throws an error).
  --patches, -p         Allows conversion of all patches up to p11 for hg38
                        and p4 for mm10. Without this option, if the BED file
                        contains contigs added by a patch the conversion
                        terminates with an error (unless the -a or -s flags
                        are present).
```

#### Examples
```text
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

---


### Validate Format
Simply performs format validation on the input BED file. If any line doesn't adhere to the BED specifications the program reports an error and terminates.
The `--fixSeparators` flag replaces fields separated by spaces into fields separated by a single tab. This is useful when writing a BED file by hand or when copy-pasting from a website.

#### Usage
```text
usage: bedparse validateFormat [-h] [--fixSeparators] [bedfile]

Checks whether the BED file provided adheres to the BED format specifications.
Optionally, it can fix field speration errors.

positional arguments:
  bedfile              Path to the BED file.

optional arguments:
  -h, --help           show this help message and exit
  --fixSeparators, -f  If the fields are separated by multiple spaces (e.g.
                       when copy-pasting BED files), replace them into tabs.
```

#### Examples
```text

> cat example.bed 
   chr1  a213941196  213942363
  chr1  213942363  213943530
chr1  213943530         213944697

> bedparse validateFormat -f example.bed 
chr1    213941196       213942363
chr1    213942363       213943530
chr1    213943530       213944697

```




## Implementations notes 
Internally, bedparse processes a bedfile line by line by instantiating objects of the bedline class. The bedline class implements an init() method that performs several checks on each field in order to ensure the correctness of the format, whereas the other methods of the class implement all the bedparse operations (see functionality).
