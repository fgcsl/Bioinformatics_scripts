# Amplicon region and Primer deduction

### Requirements 
1. python3

2. Python Modules:
```
import subprocess
import sys
import os
import glob
import pandas as pd
```

3. Download SRA Tool form the link (https://www.metagenomics.wiki/tools/short-read/ncbi-sra-file-format/sra-tools-install)
4. Download bbtools and local-blast
5. Silvadb: silva.fasta

#### Step 1. Download Raw sequences (SRR) from NCBI and Perform fasterq-dump for extract data in Fastq from SRA-accessions

1) Open bioproject_sample_ids.txt file and edit it with your bioproject and sample ID's which you want to download

2) Run "download_raw_reads.py" python script from the terminal. This script will read all the ids from bioproject_ids.txt file and it will download all the samples in fastq format

```
$ python3 download_raw_reads.py

*Note you will get all downloaded sample with BioprojectID folder in the data_sets directory
```
#### Step 2. Merging sequence and perform blastn with silva database

1) edit line no 7 of mergeblast.sh script according to your bbmerge.sh path(to find path use below command)

```
$ locate bbmerge.sh
```

2) run mergeblast.py python script

```
$ python3 mergeblast.py
```


### Outputs will be store under data_sets directory

```
01. data_sets => this is the main folder all the downloaded and output file will be stored under this directory
        - PNRJ1 PNRJ2 PNRJ3 .... PNRJn => Project id directories (output of prefetch)
                - ERR1612265 => it stores ERR1612265.sra file (output of prefetch)
                - raw_reads =>  it stores raw reads _1.fastq, _2.fastq (output of fastq-dump)
                - output => storing outputs of merging=.fasta seqtk=top20_seq.fa, blastn_out=out.txt
02. silvadb_out => stored makedb outputs





