#!/usr/bin/bash

#study download and split sra files

# Access the input directory value from environment variable

_ids_file_="bioproject_sample_ids.txt"


if [[ $(awk '{print $2}'  $_ids_file_ | grep "PRJ") ]];
then
	echo "Error: Study ID should be in first column, file format error in $_ids_file_"; 
	exit 1
fi


if [ -s $_ids_file_ ]
then
	while read -r col1 col2;
	do
		echo "prefetch" -O data_sets/$col1 $col2;
	done <  $_ids_file_ |sh	
else
	echo -e  "Error: \"$_ids_file_\" list of sample ids file not found"
	exit 1
fi


#validation: check all the study are downloaded or not in single .sra  format

while read -r col1 col2;
do
	for i in data_sets/$col1/$col2;
	do
		echo $i;
		ls $i | wc -l;
	done | sed 'N;s/\n/ /g' | awk '{
		if ($2>1 || $2==0) 
		print "Error: " $1 " this study not downloaded properly"
	}'
done < $_ids_file_


#Run fastq-dump command and save the result under raw_reads directory

while read -r col1 col2;
do
	cmd=$(echo "fastq-dump" -O data_sets/$col1/raw_reads/ "--split-3" data_sets/$col1/$col2/*.sra)
	eval $cmd 
	if [ "$(find data_sets/$col1/raw_reads/ -type f \( -name '*_1.fastq' -o -name '*_2.fastq' -o -name '*_R1.fastq' -o -name '*_R2.fastq' -o -name '_R1_001.fastq' -o -name '*_R2_001.fastq' \))" ]
	then
		echo  "Sample split: Successfully"
	else
		echo  "Error: Study-ID: $col1  sample-ID: $col2 may be samples have multiple run, it did't splits sra reads into forward/reverse fastq format" | tee -a warning
	fi

done < $_ids_file_ 
