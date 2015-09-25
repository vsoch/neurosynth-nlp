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
from nlp import do_stem
import re
import numpy
import sys

ARR_DELIM = '~^~'

# Retrieve concepts from the cognitive atlas
concepts = get_concept().pandas
concept_names = concepts["name"].tolist()
concept_uids = concepts["id"].tolist()

# We will stem concept names, and search for them across sentences
concepts_stemmed = []
for concept_name in concept_names:
    concept_name = concept_name.split(" ")
    if isinstance(concept_name,str):
        concept_name = [concept_name]
    concept_stemmed = do_stem(concept_name)
    concepts_stemmed.append(" ".join(concept_stemmed).encode("utf-8"))

# Make a long regular expression
concept_regexp = "*|".join(concepts_stemmed) + "*"

# Function to get a match: start, length, text,s from a sentence
def get_match(phrasematch,entirephrase):
    full_concept = phrasematch.split(" ")
    foundmatch = True
    indices = []
    for word in full_concept:
        if word in entirephrase:
            indices.append(entirephrase.index(word))
        # Missing any one word, not a match
        else:
            foundmatch = False
    if len(numpy.unique(indices)) == len(full_concept):
        for i in range(0,len(indices)-1):
            # Not in chronological order +1, not a match
            if indices[i]+1 != indices[i+1]:
                foundmatch = False
    # Missing any one word, not a match
    else:
        foundmatch = False
    if foundmatch == True:
        start_index = entirephrase.index(full_concept[0])
        length = len(full_concept)
        text = entirephrase[start_index:start_index+length]      
    else:
        start_index = 0
        length = 0
        text = ""
    return start_index,length,text


# For-loop for each row in the input query
for row in sys.stdin:
    # Find phrases that are continuous words tagged with PERSON.
    sentence_id, words_str, ner_tags_str = row.strip().split('\t')
    words = words_str.split(ARR_DELIM)
    stemmed = [s.encode("utf-8") for s in do_stem(words)]
    phrases = []
    # Search the sentence for any concepts:
    if re.match(concept_regexp," ".join(stemmed)):
        for c in range(0,len(stemmed)):
            for concept_stemmed in concepts_stemmed:
                if re.match("%s" %(stemmed[c]),concept_stemmed):
                    print "%s matches %s" %(stemmed[c],concept_stemmed)
                    start_index,length,text = get_match(concept_stemmed,stemmed)
                    # A non match returns a length of 0
                    if length != 0:
                        phrases.append((start_index, length, text))            

# Pipe back to std-out                    
for start_position, length, text in phrases:
    print '\t'.join(
      [ str(x) for x in [
        sentence_id,
        start_position,   # start_position
        length, # length
        text,  # text
        '%s_%d' % (sentence_id, start_position)        # mention_id
      ]])
