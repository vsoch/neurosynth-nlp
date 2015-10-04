import csv, os, sys

# Get cognitive atlas concepts for distant supervision
from cognitiveatlas.api import get_concept
from nlp import do_stem, find_phrases, stem_phrases
import pandas
import pickle
import numpy
import sys
import re

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

concepts = {"concepts":concepts.json,"concept_names":concept_names,"concept_ids":concept_ids,
            "vocab_stemmed":vocab_stemmed,"pairs":pairs,"related_concepts":related_concepts,
            "relation_df":relationdf}

# Save to pickle to load from scripts
pickle.dump(concepts,open("concept_relations.pkl","wb"))
