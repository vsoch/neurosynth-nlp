#! /usr/bin/env python

import csv, os, sys

APP_HOME = os.environ['APP_HOME']

# Get cognitive atlas concepts for distant supervision
import pandas
import pickle
import numpy
import sys
import re

ARR_DELIM = '~^~'

# Retrieve concepts from the cognitive atlas
input_pickle = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/concept_relations.pkl"
concept_pickle = pickle.load(open(input_pickle,"rb"))

# Retrieve concepts from the cognitive atlas
concept_names = concept_pickle["concept_names"]
concept_ids = concept_pickle["concept_ids"]
vocab_stemmed = concept_pickle["vocab_stemmed"]
pairs = concept_pickle["pairs"]            # pairs of concepts
related_concepts = concept_pickle["related_concepts"]
relationdf = concept_pickle["relation_df"]

# For each input tuple
for row in sys.stdin:
    parts = row.strip().split('\t')
    sentence_id, c1_id, c1_text, c2_id, c2_text = parts

    c1_text = c1_text.strip()
    c2_text = c2_text.strip()
    c1_text_lower = c1_text.lower()
    c2_text_lower = c2_text.lower()

    # DS rule 1: true if they appear in spouse KB, false if they appear in non-spouse KB
    is_true = '\N'
    if (c1_text_lower, c2_text_lower) in pairs or \
       (c2_text_lower, c1_text_lower) in pairs:
       is_true = '1'
    # We don't currently have negative training cases
    #elif (p1_text_lower, p2_text_lower) in non_spouses or \
    #     (p2_text_lower, p1_text_lower) in non_spouses:
    #     is_true = '0'
    # DS rule 3: false if they appear to be in same person
    elif (c1_text == c2_text) or (c1_text in c2_text) or (c2_text in c1_text):
         is_true = '0'

    # Output relation candidates into output table
    print '\t'.join([
        c1_id, c2_id, sentence_id,
        "%s-%s" %(c1_text, c2_text),
        is_true,
        "%s-%s" %(c1_id, c2_id),
        '\N'   # leave "id" blank for system!
    ])
