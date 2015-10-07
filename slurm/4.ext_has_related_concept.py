#! /usr/bin/env python

# Get cognitive atlas concepts for distant supervision
from nlp import do_stem, find_phrases, stem_phrases
import pandas
import pickle
import numpy
import sys
import re
import os

concept_pickle = sys.argv[1]
rows = sys.argv[2]
output_pkl = sys.argv[3]

# Read concept pickle
concept_pickle = pickle.load(open(concept_pickle,"rb"))

# Retrieve concepts from the cognitive atlas
concept_names = concept_pickle["concept_names"]
concept_ids = concept_pickle["concept_ids"]
vocab_stemmed = concept_pickle["vocab_stemmed"]
pairs = concept_pickle["pairs"]            # pairs of concepts
related_concepts = concept_pickle["related_concepts"]
relationdf = concept_pickle["relation_df"]

rows = rows.strip("\n").split("|")
result = pandas.DataFrame(columns=["c1_id","c2_id","sentence_id","relation_text",
                                   "truefalse","relation_id","id"])

# For each input tuple
for row in rows:
    parts = row.strip().split(',')
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
    # DS rule 3: true if they appear to be same concept
    elif (c1_text == c2_text) or (c1_text in c2_text) or (c2_text in c1_text):
         is_true = '1'
    # Output relation candidates into output table
    relation_id = "%s-%s" %(c1_id, c2_id)
    res = [c1_id, c2_id, sentence_id, "%s-%s" %(c1_text, c2_text),
           is_true,relation_id,'\N']   # leave "id" blank for system!
    result.loc[relation_id] = res

result.to_csv(output_pkl,sep="\t")
