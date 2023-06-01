## Author: This script Written by  Abhishek Khatri 
## Remember to edit bioproject_sample_ids.txt file

import subprocess
import sys
import os
import glob
import pandas as pd

from pathlib import Path

def download_data(id_file):
    path = Path(id_file)

    if path.is_file():
        columns_names = ["pro_id", "sample_id"]
        df = pd.read_csv(id_file, names=columns_names, sep=' ')
        study_id = df.iloc[:, 0]
        sample_id = df.iloc[:, 1]

        if study_id.str.startswith("PRJ").all():
            for index, row in df.iterrows():
                study_id = row[0]
                sample_id = row[1]
                prefetch_command = [
                    "prefetch",
                    "-O",
                    "data_sets/{}".format(study_id),
                    "{}".format(sample_id)
                ]
                # Run the command as a subprocess
                subprocess.run(prefetch_command)
        else:
            error_message = "Error: Input file error, make sure Study Id (PRJ NCBI bioproject id) should be first column"
            print_and_save_error(error_message)
            sys.exit(1)
    else:
        error_message = "File doesn't exist"
        print_and_save_error("Error: {} {}".format(id_file, error_message))


def print_and_save_error(error_message):
    print(error_message)
    with open("error.log", "a") as file:
        print(error_message, file=file)


def validate_downloads(df):
    for index, row in df.iterrows():
        study_id = row[0]
        sample_id = row[1]
        sra_path = ("data_sets/{}/{}/{}.sra".format(study_id, sample_id, sample_id))

        if not os.path.exists(sra_path):
            warning_message = "Warning: Study ID: {}, Sample ID: {} The data was not downloaded properly. Further analysis will not proceed.".format(study_id, sample_id)
            print_and_save_warning(warning_message)


def print_and_save_warning(warning_message):
    print(warning_message)
    with open("warning.log", "a") as file:
        print(warning_message, file=file)


def run_fastq_dump(df):
    for index, row in df.iterrows():
        study_id = row[0]
        sample_id = row[1]
        sra_path = ("data_sets/{}/{}/{}.sra".format(study_id, sample_id, sample_id))

        for sra in glob.glob(sra_path):
            fasterq_command = [
                "fastq-dump",
                "-O",
                os.path.dirname(os.path.dirname(sra)) + "/raw_reads",
                "--split-3",
                sra
            ]
            subprocess.run(fasterq_command)

            raw_reads_path = ("{}/{}_1.fastq".format(os.path.dirname(os.path.dirname(sra)) + "/raw_reads", sample_id))

            if not os.path.exists(raw_reads_path):
                error_message = "Error: {}. Failed to split SRA reads into forward/reverse fastq format. It is possible that the samples have multiple runs.".format(os.path.dirname(os.path.dirname(raw_reads_path)))
                print_and_save_warning(error_message)


id_file = "bioproject_sample_ids.txt"

download_data(id_file)

columns_names = ["pro_id", "sample_id"]
df = pd.read_csv(id_file, names=columns_names, sep=' ')

validate_downloads(df)
run_fastq_dump(df)
