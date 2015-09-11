#!/usr/bin/env python2

import os
import sys
import pandas
from textblob import TextBlob
from pubmed import Pubmed
from glob import glob

output_file = sys.argv[1]

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
#pickle.dump(articles,open("articles.pkl","wb"))

# Write articles to file
#88390,"<text>
#<p>
#sentence1
#</p>
#<p>
#sentence2
#</p>
#<p>
#</text>"

filey = open(output_file,"wb")
count = 0
for pmid,article in articles.iteritems():
    print "Parsing %s of %s" %(count,len(articles))
    filey.writelines('%s,"<text>\n' %pmid)
    abstract = article.getAbstract()
    blob = TextBlob(abstract)
    for sentence in blob.sentences:
        sentence = sentence.format("utf-8"),replace(","," ")
        filey.writelines('<p>\n%s\n</p>\n' %sentence)
    filey.writelines('</text>"\n')
    count = count + 1
filey.close()
