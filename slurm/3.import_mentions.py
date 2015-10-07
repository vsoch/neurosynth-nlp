#!/usr/bin/python

# This script will read in the output, and import each into the mentions table

import os
from glob import glob
output_base = '/work/02092/vsochat/wrangler/DATA/NEUROSYNTH-NLP/mentions'


# REGION MENTIONS ############################################################
# Get number of text files with input
input_files = glob("%s/region*.txt" %output_base)

# load the data into database
for i in range(1,len(input_files)):
    os.system('deepdive sql "COPY region_mentions FROM STDIN CSV" <%s' %input_files[i])

# How many error files? 
error_files = glob("%s/region*.err" %output_base)

# CONCEPT MENTIONS ############################################################

input_files = glob("%s/concept*.txt" %output_base)

# Try writing to database
for i in range(0,len(input_files)):
    os.system('deepdive sql "COPY concept_mentions FROM STDIN CSV" <%s' %input_files[i])
