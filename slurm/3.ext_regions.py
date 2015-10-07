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
import os
import sys

json_lookup = sys.argv[1]
sentences_file = sys.argv[2]
start = int(sys.argv[3])
end = int(sys.argv[4])
error_file = sys.argv[5]

# Get sentences
sentences_file = open(sentences_file,"rb")
sentences = sentences_file.readlines()[start:end]
sentences_file.close()

# PARSE SENTENCES HERE.
lines = [s.strip("\n") for s in sentences]

# We will write to an output file
output_file = error_file.replace(".err",".txt")
filey = open(output_file,'w')

# Read in the json with brain regions
region_dict = json.load(open(json_lookup,"rb"))

# Make a big list of all regionnames
regions = []
for r in region_dict:
    regions = regions + r["variants"]

# For-loop for each row in the input query
for l in range(0,len(lines)):
    try:
        line = lines[l]
        # Find phrases that are continuous words tagged with PERSON.
        sentence_id, words_str = line.strip().replace('"','').strip('}').split('{')
        sentence_id = sentence_id.strip(",")
        words = words_str.split(",")
        words = [w.replace(")","").replace("(","") for w in words]
        phrases = find_phrases(words,regions)
        # Insert into mentions table
        for start_position, length, text in phrases:
            mention_id =  '%s_%d' % (sentence_id, start_position)
            insert_statement = "INSERT INTO region_mentions values ('%s',%s,%s,'%s','%s');\n" %(sentence_id,start_position,length," ".join(text),mention_id)
            filey.writelines(insert_statement);
    except:
        if not os.path.exists(error_file):
            efiley = open(error_file,"w")
        efiley.writelines("%s\n" %(line))
        print "Error with line %s" %line
    
filey.close()
if os.path.exists(error_file):
    efiley.close()
