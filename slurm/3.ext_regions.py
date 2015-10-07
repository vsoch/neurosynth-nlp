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
import sys

json_lookup = sys.argv[1]

ARR_DELIM = '~^~'

# Read in the json with brain regions
region_dict = json.load(open(json_lookup,"rb"))

# Make a big list of all regionnames
regions = []
for r in region_dict:
    regions = regions + r["variants"]

# For-loop for each row in the input query
for row in sys.stdin:
    # Find phrases that are continuous words tagged with PERSON.
    sentence_id, words_str, ner_tags_str = row.strip().split('\t')
    words = words_str.split(ARR_DELIM)
    phrases = find_phrases(words,regions)

    # Pipe back to std-out                    
    for start_position, length, text in phrases:
        print '\t'.join(
          [ str(x) for x in [
            sentence_id,
            start_position,   # start_position
            length,           # length
            " ".join(text),   # text
            '%s_%d' % (sentence_id, start_position)        # mention_id
      ]])
