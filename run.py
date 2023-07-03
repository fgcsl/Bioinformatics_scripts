#!/usr/bin/python3

import subprocess

# Execute download_samples.py
subprocess.run(['python3', 'download_samples.py'], check=True)

# Execute mergeblast.py
subprocess.run(['python3', 'mergeblast.py'], check=True)

# Execute Primer_sequence.py
subprocess.run(['python3', 'get_primer_seq.py'], check=True)

# Execute extract_sample.py 
subprocess.run(['python3', 'extract_sample.py'], check=True)

# Execute download2_samples.py
#subprocess.run(['python3', 'download2_samples.py'], check=True)
