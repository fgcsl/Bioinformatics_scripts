#!/usr/bin/python3

import fileinput
import subprocess
import os

# Open the file for reading and skip the first line
with fileinput.input(files=('hypervariable_region.txt')) as f:
    for line_num, line in enumerate(f):
        if line_num != 0:
            # Extract the first column from each line
            column = [line.split()[0]]
            for project in column:
                  path=os.path.join("data_sets/",project)
                    # Execute the grep command using subprocess
                  with open(path+'/bio_sample_ids.txt', 'a') as output_file:
                    subprocess.run(['grep', project, 'ALL_sample_list'], stdout=output_file, check=True)
 
 # sed '1d' hypervariable_region.txt | awk '{print $1}' | sed 's/.*/grep "&" ALL_sample_list/g'
