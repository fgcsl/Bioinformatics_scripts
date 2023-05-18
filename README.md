# Bioinformatics_scripts
## 1. To download bioproject study from NCBI
### Requirements 
Download SRA Tool form the link (https://www.metagenomics.wiki/tools/short-read/ncbi-sra-file-format/sra-tools-install)

### Step:1
Open bioproject_ids.txt file and edit it with your bioproject list which you want to download

### Step:3
Run "download_raw_reads.sh" Script in the terminal. This script will read all the ids from bioproject_ids.txt file and download all the samples in fastq format

```
$chmod +X download_raw_reads.sh
$./download_raw_reads.sh

*Note you will get all downloaded sample with BioprojectID folder in the raw_reads directory
```
