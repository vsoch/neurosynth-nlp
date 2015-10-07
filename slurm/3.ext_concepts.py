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

from nlp import do_stem, find_phrases
import sys
import pickle

ARR_DELIM = '~^~'

# Retrieve concepts from the cognitive atlas
concept_pickle = "/home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/slurm/concept_relations.pkl"
concept_pickle = pickle.load(open(concept_pickle,"rb"))

# Retrieve concepts from the cognitive atlas
concept_names = concept_pickle["concept_names"]
concept_ids = concept_pickle["concept_ids"]

# For-loop for each row in the input query
for row in sys.stdin:
    # Find phrases that are continuous words tagged with PERSON.
    sentence_id, words_str, ner_tags_str = row.strip().split('\t')
    words = words_str.split(ARR_DELIM)
    phrases = find_phrases(words,concept_names)

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
