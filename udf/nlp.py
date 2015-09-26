#!/usr/bin/env python

"""

NLP Functions for use with deepdive neurosynth-nlp

"""

from textblob import TextBlob, Word
from nltk.stem.porter import *
from nltk.stem import *
import numpy
import pandas
import re

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/07/25 $"
__license__ = "Python"

# Return list of stemmed phrases
def stem_phrases(phrases):
    stemmed = []
    for phrase in phrases:
        phrase = phrase.split(" ")
        if isinstance(phrase,str):
            phrase = [phrase]
        single_stemmed = do_stem(phrase)
        stemmed.append(" ".join(single_stemmed).encode("utf-8"))
    return stemmed

"""
get_match:

Function to get a match: start, length, text, from a sentence

Returns dictionary with:
  
  start_index
  length
  text
  found_indices: updated binary [0,1] list of found indices in entirephrase

"""
def get_match(phrasematch,entirephrase,found_indices):
    full_concept = phrasematch.split(" ")
    foundmatch = True
    # We should not find words that have already been found :)
    findices = [i for i in range(0,len(found_indices)) if found_indices[i] == 1]
    for found_index in findices:
        entirephrase[found_index] = "XXXXXXXXXXXXXXXX"
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
                foundmatch=False
    # Missing any one word, not a match
    else:
        foundmatch = False
    if foundmatch == True:
        start_index = entirephrase.index(full_concept[0])
        length = len(full_concept)
        text = entirephrase[start_index:start_index+length]   
        # Update found indices
        found_indices[start_index:start_index+length]=1   
    else:
        start_index = 0
        length = 0
        text = ""
    result = {"start_index":start_index,
              "length":length,
              "text":text,
              "found_indices":found_indices}
    return result

# Use get_match to find a list of phrases with get_match (above)
"""
words: a list of words
vocabulary: a list of words / phrases to find in the words
repeat: the number of times to run over the phrase
(in case of repeats of same in one sentence)

"""
def find_phrases(words,vocabulary,repeat=2):
    vocabulary = numpy.unique(vocabulary).tolist()
    vocabulary = [v.encode("utf-8") for v in vocabulary]
    # We will stem phrases, and search for them across the stemmed words
    vocab_stemmed = stem_phrases(vocabulary)
    stemmed = [s.encode("utf-8") for s in do_stem(words)]
    # Make a long regular expression
    regexp = "*|".join(regions_stemmed) + "*"
    phrases = []
    # We need to keep track of indices that have found items
    found_indices = numpy.zeros(len(stemmed))
    # We run it twice in case of repeats in a sentence
    for r in range(0,repeat):
        # Search the sentence for any concepts:
        if re.search(regexp," ".join(stemmed)):
            for c in range(0,len(stemmed)):
                for single_stemmed in vocab_stemmed:
                    if re.match("%s" %(stemmed[c]),single_stemmed):
                        match_result = get_match(single_stemmed,stemmed,found_indices)
                        found_indices = match_result["found_indices"]
                        start_index = match_result["start_index"]
                        length = match_result["length"]
                        text = match_result["text"]
                        # A non match returns a length of 0
                        if length != 0:
                            phrases.append((start_index, length, text))            
    return phrases


# Stem words (does not return unique)
def do_stem(words):
    stemmer = PorterStemmer()
    if isinstance(words,str):
        words = [words]
    stems = []
    for word in words:
        stems.append(stemmer.stem(word))
    return [s.lower() for s in stems]


def get_total_words(text):

    totalwords = 0

    # Dictionary
    if isinstance(text,dict):
        for label,sentences in text.iteritems():
            if isinstance(sentences,str):
                sentences = [sentences]
            for sentence in sentences:
                blob =  TextBlob(sentence)
                words = do_stem(blob.words)
                totalwords += len(words)
        return totalwords    

    # String or list
    elif isinstance(text,str):
        text = [text]
    for sentence in text:
        blob =  TextBlob(sentence)
        words = do_stem(blob.words)
        totalwords += len(words)
    return totalwords


def get_term_counts(terms,text):
    if isinstance(text,dict):
        return get_term_counts_dict(terms,text)
    elif isinstance(text,str):
        text = [text]
        return get_term_counts_list(terms,text)

def get_term_counts_list(terms,text):
    # Convert words into stems
    stems = do_stem(terms)

    # data frame hold counts
    counts = pandas.DataFrame(0,columns=["count"],index=stems)

    for sentence in text:
        blob =  TextBlob(sentence)
        words = do_stem(blob.words)
        words = [w for w in words if w in stems]
        counts.loc[words] = counts.loc[words] + 1
    return counts        
    

def get_term_counts_dict(terms,text):
    # Convert words into stems
    stems = do_stem(terms)

    # data frame hold counts
    counts = pandas.DataFrame(0,columns=["count"],index=stems)

    for label,sentences in text.iteritems():
        if isinstance(sentences,str):
            sentences = [sentences]
        for sentence in sentences:
            blob =  TextBlob(sentence)
            words = do_stem(blob.words)
            words = [w for w in words if w in stems]
            counts.loc[words] = counts.loc[words] + 1
    return counts        

