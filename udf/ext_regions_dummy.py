#! /usr/bin/env python

# Sample input data (piped into STDIN):
'''
118238@10\tSen.~^~Barack~^~Obama~^~and~^~his~^~wife~^~,~^~Michelle~^~Obama~^~,~^~have~^~released~^~eight~^~years~^~of~^~joint~^~returns~^~.\tO~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~DURATION~^~DURATION~^~O~^~O~^~O~^~O
118238@12\tDuring~^~the~^~2004~^~presidential~^~campaign~^~,~^~we~^~urged~^~Teresa~^~Heinz~^~Kerry~^~,~^~the~^~wealthy~^~wife~^~of~^~Sen.~^~John~^~Kerry~^~,~^~to~^~release~^~her~^~tax~^~returns~^~.\tO~^~O~^~DATE~^~O~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~O~^~O~^~O

For example, this sentence:

the cerebellum is part of the hypothalamus and so is the anterior of the hypothalamus
(yes, it's nonsense)

Will produce objects of format:

(start,length,text)

[(1, 1, ['cerebellum']), 
(6, 1, ['hypothalamu']), 
(14, 1, ['hypothalamu'])]


'''

from nlp import find_phrases
import json
import re
import numpy
import sys

json_lookup = sys.argv[1]
start = int(sys.arv[2])
end = int(sys.argv[3])

ARR_DELIM = '~^~'
input_file = "../input/dummy_sentences.tsv"

filey = open(input_file,"rb")
lines = filey.readlines()
filey.close()

# Read in the json with brain regions
region_dict = json.load(open(json_lookup,"rb"))

# Make a big list of all regionnames
regions = []
for r in region_dict:
    regions = regions + r["variants"]

# For-loop for each row in the input query
for l in range(start,end):
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
            insert_statement = "INSERT INTO region_mentions values ('%s',%s,%s,'%s','%s');" %(sentence_id,start_position,length," ".join(text),mention_id)
            os.system('deepdive sql "%s"' %insert_statement)
    except:
        print "Error with line %s" %line

