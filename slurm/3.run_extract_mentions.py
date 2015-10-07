#!/usr/bin/python

import numpy
import os

# This script will use the deepdive database to get relationship extractions in a more
# controlled fashion.

# We will submit a script to launcher where each line is a start and end index into sentences. We will prepare both of those files now
concept_pickle = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/concept_relations.pkl"
sentences_file = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/input/sentences.csv"

sentences = open(sentences_file,"rb")
sentences_input = sentences.readlines()
sentences.close()

number_tasks = 32*24
tasks_per_run = int(numpy.ceil(len(sentences_input)/number_tasks))

# Let's keep track of sentences with errors so we can fix
mentions_output = "/work/02092/vsochat/wrangler/DATA/NEUROSYNTH-NLP/mentions"
if not os.path.exists(mentions_output):
    os.mkdir(mentions_output)

### CONCEPT MENTION EXTRACTION
##################################################################
start = 0
slurm_file = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/.job/concept_mentions.job"
filey = open(slurm_file,"wb")
for n in range(number_tasks):
    end = start+tasks_per_run
    error_file = "%s/concepts_%s.err" %(mentions_output,n)
    # We just need words
    filey.writelines('python /home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/3.ext_concepts.py %s %s %s %s %s\n' %(concept_pickle,sentences_file,start,end,error_file))
    start = start+tasks_per_run

filey.close()


json_lookup = "../udf/NER/brain_regions.json"
json_lookup = os.path.abspath(json_lookup)

### REGION MENTION EXTRACTION
##################################################################
start = 0
slurm_file = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/.job/region_mentions.job"
filey = open(slurm_file,"wb")
for n in range(number_tasks):
    end = start+tasks_per_run
    error_file = "%s/regions_%s.err" %(mentions_output,n)
    filey.writelines("python /home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/3.ext_regions.py %s %s %s %s %s\n" %(json_lookup,sentences_file,start,end,error_file))
    start = start+tasks_per_run

filey.close()
