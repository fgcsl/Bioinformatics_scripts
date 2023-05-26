# Amplicon region and Primer deduction

### Requirements 
Download SRA Tool form the link (https://www.metagenomics.wiki/tools/short-read/ncbi-sra-file-format/sra-tools-install)

## Step 1. Download Raw sequences (SRR) from NCBI and Perform fasterq-dump for extract data in Fastq from SRA-accessions

### 1) Open bioproject_sample_ids.txt file and edit it with your bioproject and sample ID's which you want to download

### 2) Run "download_raw_reads.sh" Script in the terminal. This script will read all the ids from bioproject_ids.txt file and it will download all the samples in fastq format

```
$chmod 755 download_raw_reads.sh
$./download_raw_reads.sh

*Note you will get all downloaded sample with BioprojectID folder in the data_sets directory
```
## Step 2. Merging sequence and perform blastn with silva database




