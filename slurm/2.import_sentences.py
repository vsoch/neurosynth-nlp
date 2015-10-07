#!/usr/bin/python

# This script will read in the output, and import each into the sentences table


import os
from glob import glob
output_base = '/work/02092/vsochat/wrangler/DATA/NEUROSYNTH-NLP/corenlp/extractions'

# Get number of text files with input
input_files = glob("%s/*.txt" %output_base)

# load the data into database
for i in range(len(input_files)):
    os.system('deepdive sql "COPY sentences FROM STDIN CSV" <%s' %input_files[i])


# How many error files? ~300
error_files = glob("%s/*.err" %output_base)
