#!/usr/bin/python

# This will prepare output directories and input text to run on SLURM launcher to run
# the stanford parser in parallel, and then import into a database in an expected format

import os

input_file = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/input/articles.txt"
jobs_directory = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/.job"
output_base = '/work/02092/vsochat/wrangler/DATA/NEUROSYNTH-NLP/corenlp'
filey = open(input_file,"rb")
lines = filey.readlines()
filey.close()

# File for launcher commands
launcher_file = "%s/nlp_extract.job" %(jobs_directory)
lfiley = open(launcher_file,"wb")

# Create output directories
output_directory = "%s/sentences" %(output_base)
extractions_directory = "%s/extractions" %(output_base)
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
if not os.path.exists(extractions_directory):
    os.mkdir(extractions_directory)

for l in range (0,len(lines)):
    line = lines[l]
    article_id,text = line.split("|")
    # Make an article text file to read from
    article_text = "%s/%s_sentences.txt" %(output_directory,article_id)
    article_output = "%s/%s_extractions.txt" %(extractions_directory,article_id)
    filey = open(article_text,"wb")
    filey.writelines(line)
    filey.close()
    # Write command to launcher file
    lfiley.writelines("python /home/02092/vsochat/SCRIPT/neurosynth-nlp/slurm/1.nlp_parser.py %s %s\n" %(article_text,article_output))

lfiley.close()
