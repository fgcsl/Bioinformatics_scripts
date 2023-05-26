#!/usr/bin/bash

#DBT-CMI
#Pipeline for 16S amplicon based analysis
#Paired end FastQC

bbmershell="/home/dbt-cmi/data/tools/bbmap/bbmerge.sh"

if [[ -f $bbmershell ]]
then
	for i in data_sets/*/raw_reads; 
	do 
		echo $bbmershell in1=$(echo $i/*_1.fastq) in2=$(echo $i/*_2.fastq) out=$(echo $i/*_1.fastq | sed 's/raw_reads/output/g' | sed 's/_1.fastq/.fastq/g'); 
	done | sed '/*/d' |sh

	# Warning message for worng fasta(raw_reads) format, which not having paired sequence. Those study will not preceed for merging steps
        for i in data_sets/*/raw_reads;
        do
                echo $bbmershell in1=$(echo $i/*_1.fastq) in2=$(echo $i/*_2.fastq) out=$(echo $i/*_1.fastq | sed 's/raw_reads/output/g' | sed 's/_1.fastq/.fastq/g');
        done | grep "*"  | awk '{print $2}' | awk -F "/" '{print "Warning: raw reads input file error Merging not done for " $2 " study"}' | tee -a warning

	
	# Check if merged Fastq file exists then show successfull message in the terminal
	if ls data_sets/*/output/*.fastq >/dev/null 2>&1; then
  		echo -e "\033[44;5mbbmer Successfully completed.\033[0m \033[42mYou can see output under data_sets/YOUR_Project_id/output directory\033[0m"
	else
  		echo -e "\033[5;41mError: \033[0m \033[1;41m bbmerge not done\033[0m"
		exit 1
	fi



	# change sequence format (fastq to fasta) for performing blastn  using seqtk.

	if ! command -v seqtk &> /dev/null; #check seqtk is inatall or not
	then
		echo -e "\033[5;41mError: \033[0m \033[1;41m seqtk is not installed. Please install seqtk.\033[0m"
  	  	exit 1
	else
		for i in  data_sets/*/output/*fastq;
		do 
			echo "seqtk seq -a" $i ">" $(echo $i | sed 's/.fastq/.fasta/g' ); 
		done |sh
	fi
else
	echo -e "\033[5;41mError: \033[0m \033[1;41m bbmerge.sh not found. you can add a correct path in LINE no 7 of mergeblast.sh script and try again.\033[0m"
	exit 1
	
fi


# makedb and  blastn

outputs="data_sets/*/output"

if [[ -f silva.fasta ]]
then
	makeblastdb -in silva.fasta -dbtype nucl -out silvadb_out/silva
else
	echo -e "\033[5;41mError:\033[0m \033[1;41msilva.fasta file not found in the current working directory\033[0m"
	exit 1
fi


#Extract only few reads from SRR*.fasta from each study

if [ "$(find $(echo "$outputs") -name '*.fasta' -type f)" ];
then
	for _list_fasta_ in $(echo "$outputs")/*.fasta;
	do
		echo head -60 $_list_fasta_ ">" $(echo $(dirname $_list_fasta_)/t20_seq.fas) |sh;  #Extract top 60 line (i.e 30 sequences)
	done
else
	echo -e  "\033[5;41mError:\033[0m \033[1;41mmereged fasta input files not found.\033[0m"
	exit 1
fi



# save blast result in output directory because if we save it in a diff directori like blast_out so we have to create PNRJxxx for every study which will use more memory

if [ "$(find $(echo "$outputs") -name '*.fas' -type f )" ];
then
	for _list_top_20seq_ in $(echo "$outputs")/t20_seq.fas;
	do
		echo "blastn -query  $_list_top_20seq_ -db silvadb_out/silva -out $(echo $(dirname $_list_top_20seq_))/blastn_output.txt -outfmt \"6 sstart send evalue bitscore pident qcovs\" -subject_besthit -max_target_seqs=1"; 
	done |sh
else
	echo -e "\033[5;41mError:\033[0m \033[1;41mtop 20 sequence fas files not found.\033[0m"
	exit 1
fi

