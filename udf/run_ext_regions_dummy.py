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

json_lookup = "../udf/NER/brain_regions.json"
json_lookup = os.path.abspath(json_lookup)
start = int(sys.arv[2])
end = int(sys.argv[3])

ARR_DELIM = '~^~'
input_file = "../input/dummy_sentences.tsv"

filey = open(input_file,"rb")
lines = filey.readlines()
filey.close()

iters = len(lines)/10

# For-loop for each row in the input query
for i in range(0,iters):
    start = iters*10
    end = start + 10
    filey = ".jobs/ext_region_%s.job" %(i)
    filey = open(filey,"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=ext_region_%s\n" %(i))
    filey.writelines("#SBATCH --output=.out/ext_region_%s.out\n" %(i))
    filey.writelines("#SBATCH --error=.out/ext_region_%s.err\n" %(i))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=64000\n")
    filey.writelines("python /home/02092/vsochat/SCRIPT/deepdive/neurosynth-nlp/udf/ext_regions_dummy.py %s %s %s" %(json_lookup, stard, end))
    filey.close()
    os.system("sbatch " + ".jobs/ext_region_%s.job" %(i)) 


