#!/usr/bin/python

# This will be a dummy script to read in articles, parse into sentences, and read into the sentences table in the expected format

"""
118238@10\tSen.~^~Barack~^~Obama~^~and~^~his~^~wife~^~,~^~Michelle~^~Obama~^~,~^~have~^~released~^~eight~^~years~^~of~^~joint~^~returns~^~.\tO~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~DURATION~^~DURATION~^~O~^~O~^~O~^~O
"""

import pandas
import os

delim = "~^~"
NER = "O"

input_file = "input/articles.txt"
output_file = "input/dummy_sentences.tsv"
filey = open(input_file,"rb")
lines = filey.readlines()
filey.close()

# Open output file for writing
filey = open(output_file,"wb")

for l in range (0,len(lines)):
    line = lines[l]
    print "Parsing line %s of %s" %(l,len(lines))
    article_id,text = line.split("|")
    text =  text.replace("</text>","").replace("<text>","").strip("\n").replace('"',"")
    paragraphs = text.split("<p>")
    paragraphs = [p for p in paragraphs if p]
    for p in range(0,len(paragraphs)):
        paratext = paragraphs[p].replace("<p>","").replace("</p>","")
        words = paratext.split(" ")
        words = [w.replace(" ","") for w in words if w]
        pid = "%s@%s" %(article_id,p)
        textline = delim.join(words)
        nerline = delim.join([NER]*len(words))
        output_line = "%s\t%s\t%s\n" %(pid,textline,nerline)
        # Write to file
        filey.writelines(output_line)


filey.close()
