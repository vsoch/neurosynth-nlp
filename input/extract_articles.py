#!/usr/bin/env python2

import os
import sys
import pandas
import pickle
from textblob import TextBlob
from pubmed import Pubmed
from glob import glob

output_file = sys.argv[1]

# First download nltk stuffs
home=os.environ["HOME"]
if not os.path.exists("%s/nltk_data" %home):
   import nltk
   nltk.download('all')

# Download neurosynth data
df = pandas.read_csv("database.txt",sep="\t")
pmids = df.id.unique().tolist()

print "NeuroSynth database has %s unique PMIDs" %(len(pmids))

# download abstract text
email = "vsochat@stanford.edu"
pm = Pubmed(email,pmc=False)
articles1 = pm.get_many_articles(pmids[:10000])
articles2 = pm.get_many_articles(pmids[10000:])
articles = articles1.copy()
articles.update(articles2)

if not os.path.exists("articles.pkl"):
    pickle.dump(articles,open("articles.pkl","wb"))

# Write articles to file
#88390|"<text><p>sentence1</p><p>sentence2</p><p></text>"
#88390|"<text><p>sentence1</p><p>sentence2</p><p></text>"
# We should use utf-8 http://www.postgresql.org/docs/9.0/static/multibyte.html

filey = open(output_file,"wb")
count = 0
for pmid, article in articles.iteritems():
    print "Parsing %s of %s" %(count,len(articles))
    filey.write('%s|"<text>' %pmid)
    abstract = article.getAbstract()
    blob = TextBlob(abstract)
    for sentence in blob.sentences:
        sentence = '<p>%s</p>' %sentence.raw.replace("\t","").replace("|"," ").replace("\n","").replace("\r","")
        filey.write(sentence.replace("}","").replace("{","").encode("utf-8"))
    filey.write('</text>"\n')
    count = count+1
filey.close()
