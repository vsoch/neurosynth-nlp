#!/usr/bin/python

# This script will extract a single article (all paragraphs) on the launcher grid.

"""
118238@10\tSen.~^~Barack~^~Obama~^~and~^~his~^~wife~^~,~^~Michelle~^~Obama~^~,~^~have~^~released~^~eight~^~years~^~of~^~joint~^~returns~^~.\tO~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~DURATION~^~DURATION~^~O~^~O~^~O~^~O
"""

from stanford_corenlp_pywrapper import CoreNLP
import os
import sys

# Prepare the parser
proc = CoreNLP(configdict={'annotators':'tokenize, ssplit, pos, parse, lemma, ner'},
               output_types=["pos","parse"], 
               corenlp_jars=["/work/02092/vsochat/wrangler/SOFTWARE/stanford-corenlp-full-2015-04-20/*"])

input_file = sys.argv[1]
output_file = sys.argv[2]

# Any errors will have entries written to an error file for inspection
error_file = output_file.replace(".txt",".err")
filey = open(input_file,"rb")
lines = filey.readlines()[0]
filey.close()

# Format expected to be:
# "12345|<text><p>hello this is text, sentence one!</p><p>sentence two!</p></text>"
article_id,text = lines.split("|")
text =  text.replace("</text>","").replace("<text>","").strip("\n").replace('"',"")
paragraphs = text.split("<p>")
paragraphs = [p for p in paragraphs if p]

# Writing to output file, format should look like
# 101226,
# A spokesman at the British Embassy here declined to comment .,
#"{A,spokesman,at,the,British,Embassy,here,declined,to,comment,.}",
#"{a,spokesman,at,the,British,Embassy,here,decline,to,comment,.}",
#"{DT,NN,IN,DT,NNP,NNP,RB,VBD,TO,VB,.}",
#"{""root(ROOT-0, declined-8)"",""det(spokesman-2, A-1)"",""nsubj(declined-8, spokesman-2)"",""det(Embassy-6, the-4)"",""nn(Embassy-6, British-5)"",""prep_at(spokesman-2, Embassy-6)"",""advmod(declined-8, here-7)"",""aux(comment-10, to-9)"",""xcomp(declined-8, comment-10)""}",
# "{O,O,O,O,ORGANIZATION,ORGANIZATION,O,O,O,O,O}",
# 9,
# 101226@9

filey = open(output_file,"w")

# This is a function to return a dependency structure to input into database
def dependency_structure(words,dependency):
    word = dependency[0]
    start = dependency[1]
    end = dependency[2]
    structure = word.encode("utf-8") 
    # Indexing starts at 1, so we add 1
    if word == "root":
        structure = "%s(ROOT-%s, %s-%s)" %(structure,start+1,words[end],end+1)
    else:
        structure = "%s(%s-%s, %s-%s)" %(structure,words[start],start+1,words[end],end+1)
    return structure.encode("utf-8")

for p in range(0,len(paragraphs)):
    paratext = paragraphs[p].replace("<p>","").replace("</p>","").replace("\t"," ").replace('"',"''").replace(",","")
    sentence_id = "%s@%s" %(article_id,p)
    try:
        nlp = proc.parse_doc(paratext)
        wordslist = nlp["sentences"][0]["tokens"]
        text = '"%s"' %(",".join(wordslist))
        # All commas must be replaced with "" from here on
        wordslist = [x.replace(',','""') for x in wordslist]
        words = "{%s}" %(",".join(wordslist))
        lemmas = [x.replace(',','""') for x in nlp["sentences"][0]["lemmas"]]
        lemmas = "{%s}" %(",".join(lemmas))
        pos = [x.replace(',','""') for x in nlp["sentences"][0]["pos"]]
        pos = "{%s}" %(",".join(pos))
        ner = "{%s}" %(",".join(nlp["sentences"][0]["ner"]))
        # This is a lookup for the terms, using the words
        dependencies = "{%s}" %(",".join(['""%s""' %(dependency_structure(wordslist,x)) for x in nlp["sentences"][0]["deps_cc"]]))
        # document_id | sentence | words | lemma | pos_tags | dependencies | ner_tags | sentence_offset | sentence_id 
        for_database = '%s,%s,"%s","%s","%s","%s","%s",%s,%s\n' %(article_id,text,words,lemmas,pos,dependencies,ner,p,sentence_id)
        filey.writelines(for_database)
    except:  
        if not os.path.exists(error_file):
            efiley = open(error_file,"w")
        efiley.writelines("%s|%s\n" %(sentence_id,paratext))

filey.close()
if os.path.exists(error_file):
    efiley.close()
