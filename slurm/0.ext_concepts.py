#! /usr/bin/env python

# Sample input data (piped into STDIN):
'''
118238@10\tSen.~^~Barack~^~Obama~^~and~^~his~^~wife~^~,~^~Michelle~^~Obama~^~,~^~have~^~released~^~eight~^~years~^~of~^~joint~^~returns~^~.\tO~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~DURATION~^~DURATION~^~O~^~O~^~O~^~O
118238@12\tDuring~^~the~^~2004~^~presidential~^~campaign~^~,~^~we~^~urged~^~Teresa~^~Heinz~^~Kerry~^~,~^~the~^~wealthy~^~wife~^~of~^~Sen.~^~John~^~Kerry~^~,~^~to~^~release~^~her~^~tax~^~returns~^~.\tO~^~O~^~DATE~^~O~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~O~^~O~^~O

For example, this sentence:

"'visual working memory is a part of life satisfaction is anxiety , and emotion'"

Will produce objects of format:

(start,length,text)

[(0, 3, ['visual', 'work', 'memori']), 
(1, 2, ['work', 'memori']), 
(2, 1, ['memori']), 
(10, 1, ['anxieti']), 
(7, 2, ['life', 'satisfact']), 
(10, 1, ['anxieti']), 
(13, 1, ['emot'])]

'''

from cognitiveatlas.api import get_concept
from nlp import do_stem, find_phrases
import re
import numpy
import sys

ARR_DELIM = '~^~'
input_file = "../input/dummy_sentences.tsv"

# Retrieve concepts from the cognitive atlas
concepts = get_concept().pandas
concept_names = concepts["name"].tolist()

filey = open(input_file,"rb")
lines = filey.readlines()
filey.close()

# For-loop for each row in the input query
for l in range(0,len(lines)):
    try:
        line = lines[l]
        # Find phrases that are continuous words tagged with PERSON.
        sentence_id, words_str, ner_tags_str = line.strip().split('\t')
        words = words_str.split(ARR_DELIM)
        words = [w.replace(")","").replace("(","") for w in words]
        phrases = find_phrases(words,concept_names)
        # Insert into mentions table
        for start_position, length, text in phrases:
            mention_id =  '%s_%d' % (sentence_id, start_position)
            insert_statement = "INSERT INTO concept_mentions values ('%s',%s,%s,'%s','%s');" %(sentence_id,start_position,length," ".join(text),mention_id)
            os.system('deepdive sql "%s"' %insert_statement)
    except:
        print "Error with line %s" %line


