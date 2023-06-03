import subprocess
import pandas as pd
import os
import glob
import sys
import re

from pathlib import Path
path_to_file = "bioproject_sample_ids.txt"
path = Path(path_to_file)

if not os.path.exists(path_to_file):
    print(path_to_file +" not exist")
    sys.exit(1)

bbmershell="/home/dbt-cmi/data/tools/bbmap/bbmerge.sh"

if not os.path.exists(bbmershell):
    print(bbmershell +" bbmerge.sh not found. you can add a correct path in LINE no 13 on mergeblast.py and try again.")
    sys.exit(1)


columns_names=["pro_id", "sample_id"]
df=pd.read_csv(path_to_file, names=columns_names, sep=' ')
study_id=df.iloc[:,0]
sample_id=df.iloc[:,1]

for index, row in df.iterrows():
    study_id = row[0]
    sample_id = row[1]
    sra_path=("data_sets/{}/{}/{}.sra".format(study_id, sample_id, sample_id))
    for sra in glob.glob(sra_path):
        print ("")
        print("Merging on Process: Processing study ID: {}, Sample ID: {}".format(study_id, sample_id))
        print ("")
        merging_command = [
            bbmershell,
            "in1=" + os.path.dirname(os.path.dirname(sra)) + "/raw_reads/" + sample_id + "_1.fastq",
            "in2=" + os.path.dirname(os.path.dirname(sra)) + "/raw_reads/" + sample_id + "_2.fastq",
            "out=" + os.path.dirname(os.path.dirname(sra)) + "/output/"+sample_id+".fastq"
        ]
        subprocess.run(merging_command)

        check_reads=(os.path.dirname(os.path.dirname(sra))+"/raw_reads/"+sample_id+"_1.fastq")
        
        #Warning message for worng fasta(raw_reads) format, which not having paired sequence. Those study will not preceed for merging steps
        if not os.path.exists(check_reads):
            warning_message = "Warning: Study ID: {} - Failed to merge raw reads. Raw reads not found.".format(study_id)
            print(warning_message)

            with open ("error.log","a") as file:
                print(warning_message, file=file)


########### seqtk fastq to fasta

def seqtk_blastn(df):
    for index, row in df.iterrows():
        study_id = row[0]
        sample_id = row[1]
        output_path=("data_sets/{}/output/{}.fastq".format(study_id, sample_id))
        fasta_list=output_path.replace("fastq","fasta")
        t20=os.path.dirname(fasta_list)+"/t20_seq.fas"
        
        if os.path.exists(output_path):
            
            seqtk_shell = [
                "seqtk seq -a " + output_path + " > " + output_path.replace("fastq","fasta")
            ]

            #top 60 Extract only few reads from SRR*.fasta from each study

            extraxt_60_reads = [
                "head -60 " + fasta_list + " > " + t20
                
            ]

            subprocess.run(seqtk_shell)
            subprocess.run(extraxt_60_reads)
            
        else:
            seqtk_error=("Error: Study ID: "+ study_id +" - fastq file not found, faild to change fastq to fasta format")
            print(seqtk_error)
            with open ("error.log","a") as file:
                print(seqtk_error, file=file)
                
seqtk_blastn(df)


for index, row in df.iterrows():
        study_id = row[0]
        sample_id = row[1]
        output_dir=("data_sets/{}/output".format(study_id))
        output_path=("data_sets/{}/output/{}.fastq".format(study_id, sample_id))
        fasta_list=output_path.replace("fastq","fasta")
        
        if os.path.exists(output_dir+"/blastn_output.txt"):
            if os.stat(output_dir+"/blastn_output.txt").st_size==0:
                blastn_empty_err=("Error: Study ID:" + study_id + " - Faild blastn_output.txt is empty")
        else:
            blastn_notexist_err="Error: Study ID: " + study_id + " - Faild blastn_output.txt file not exist."
            print(blastn_notexist_err)
            with open("error.log","a") as file:
                    print(blastn_notexist_err, file=file)
            #print("Error: Study ID: {} faild blastn_output.txt file not exist.".format(study_id))
            
# Error handling - 
# Extract error study ids from error.log file and remove if from bioproject_sample_ids.txt

error_file="error.log"
prj_ids = set()
with open(error_file,"r") as file:
    for line in file:
        match = re.search(r"Study ID: (PRJ\w+)", line)
        if match:
            prj_ids.add(match.group(1))
            
prj_ids=list(prj_ids)
#print(prj_ids)
copy =[
    "cp", "bioproject_sample_ids.txt", "refine_bioproject_sample_ids.txt"
]
subprocess.run(copy)

for i in prj_ids:
    delete_shell = "sed -i '/{}/d' refine_bioproject_sample_ids.txt".format(i)
    subprocess.run(delete_shell, shell=True)
