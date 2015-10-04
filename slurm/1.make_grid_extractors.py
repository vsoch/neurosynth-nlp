#!/usr/bin/python

import numpy

# This script will use the deepdive database to get relationship extractions in a more
# controlled fashion.

# First, generate a file with concept mentions and region mentions

deepdive sql "COPY (SELECT * From region_mentions) TO STDOUT WITH CSV;" >> region_mentions.csv
deepdive sql "COPY (SELECT * From concept_mentions) TO STDOUT WITH CSV;" >> concept_mentions.csv

# We will write to a single text file commands to run on the launcher, the number depending on how
# the running of it works. The input is expected to be:
# 1.run_extractions.py concept_relations.pkl X,X,X,X|X,X,X,X|X,X,X,X output_pickle
# where each of the X statements is an entry from the concepts table, separted by "|"

output_folder = "/work/02092/vsochat/wrangler/DEEPDIVE/neurosynth-nlp/related_concepts"
input_pickle = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/concept_relations.pkl"
concept_mentions = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/concept_mentions.csv"

# Read in the concepts to get the total number of mentions
concept_mentions = open(concept_mentions,"rb").readlines()
number_tasks = X
tasks_per_run = numpy.ceil(len(concept_mentions)/number_tasks))


### RELATED CONCEPT EXTRACTION ##################################################################
# Here we write the job file to extract related concepts
start = 0
slurm_file = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/.job/related_concepts.job."
filey = open(slurm_file,"wb")
for n in range(number_tasks):
    tasks = concept_mentions[start:start+tasks_per_run]
    tasks = "|".join(tasks)
    output_pickle = "%s/%s.pkl" %(output_folder,n)
    filey.writelines("python /home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/1.ext_has_related_concept.py %s %s %s\n" %(input_pickle,tasks,output_pickle))
    start = start+tasks_per_run

filey.close()


### CONCEPT-REGION EXTRACTION ##################################################################
# Here we write the job file to extract related regions/concepts

# write after the above is tested and working!
