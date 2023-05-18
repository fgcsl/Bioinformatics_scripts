#!/usr/bin/bash

#study download and split sra files

if [ -f bioproject_ids.txt ]
then
        mkdir prefetch_data
        while read -r line; 
        do
                echo "prefetch $line && mkdir prefetch_data/$line && mv SRR* prefetch_data/$line";
        done < bioproject_ids.txt |sh
else
        echo "\"bioproject_ids.txt\" list of ids file not found"
fi

#validation: check all the study are downloaded or not in single .sra formatt
for i in prefetch_data/*/*;
do
        echo $i;
        ls $i | wc -l;
done | sed 'N;s/\n/ /g' | awk '{
                                if ($2>1 || $2==0) 
                                        print "\033[5;41m Error:\033[0m \033[1;41m " $1 " \033[0m\033[45mthis study not downloaded properly\033[0m"
                                }'

#Run fastq-dump command and save the result under raw_reads directory

mkdir -p raw_reads
for _split_sra in prefetch_data/*/*/*; do
    cmd=$(echo "$_split_sra" | cut -d "/" -f2 | sed 's/.*/fastq-dump -O raw_reads\/& --split-3/g')
    eval "$cmd" "$_split_sra"
    echo -e "\033[42mSample split:\033[0m \033[44;5mSuccessfully\033[0m"
done
