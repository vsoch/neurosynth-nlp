#! /usr/bin/env python

import csv, os, sys

APP_HOME = os.environ['APP_HOME']

# Get cognitive atlas concepts for distant supervision
from cognitiveatlas.api import get_concept
from nlp import do_stem, find_phrases, stem_phrases
import pandas
import numpy
import sys
import re

ARR_DELIM = '~^~'

# Retrieve concepts from the cognitive atlas
concepts = get_concept()
concept_names = concepts.pandas["name"].tolist()
concept_ids = concepts.pandas["id"].tolist()
vocab_stemmed = stem_phrases(concept_names)

# First generate a matrix of relationships, put a 1 for is-a
pairs = set()            # pairs of concepts
related_concepts = set() # concepts that are related to something

relationdf = pandas.DataFrame(0,index=vocab_stemmed,columns=vocab_stemmed)
for c in range(0,len(concepts.json)):
    concept = concepts.json[c]
    cid = concept["id"]
    if "relationships" in concept:
        for relation in concept["relationships"]:
            if relation["relationship"] == "kind of":
                # We have assertions for undefined concepts, so we need to check
                if cid in concept_ids and relation["id"] in concept_ids:
                    stem1 = stem_phrases([concept["name"]])[0]
                    relation_concept = get_concept(id=relation["id"])
                    stem2 = stem_phrases([relation_concept.json[0]["name"]])[0]
                    relationdf.loc[stem1,stem2] = 1
                    relationdf.loc[stem2,stem1] = 1
                    pairs.add((stem1,stem2))
                    related_concepts.add(stem1)
                    related_concepts.add(stem2)

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
