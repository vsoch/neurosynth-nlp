#!/usr/bin/env bash

CURRENT_DIRECTORY=$PWD
cd $WORK
mkdir SOFTWARE
cd SOFTWARE
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-04-20.zip
unzip stanford-corenlp-full-2015-04-20.zip

# http://nlp.stanford.edu/software/basic-compiling.txt
cd stanford-corenlp-full-2015-04-20
mkdir src
cd src
jar -xf ../stanford-corenlp-3.5.2-sources.jar
cd $WORK/SOFTWARE
wget http://www.us.apache.org/dist/ant/binaries/apache-ant-1.9.6-bin.zip
unzip apache-ant-1.9.6-bin.zip 
cd $WORK/SOFTWARE/stanford-corenlp-full-2015-04-20
module load java64/1.8.0
$WORK/apache-ant-1.9.6/bin/ant

# Install python wrapper
cd $WORK/SOFTWARE
git clone https://github.com/brendano/stanford_corenlp_pywrapper
cd stanford_corenlp_pywrapper
pip install . --user

echo "# Stanford CoreNLP/Ant" >> ~/.bashrc
echo "module load java64/1.8.0" >> ~/.bashrc
echo "export PATH=$PATH:$WORK/SOFTWARE/stanford-corenlp-full-2015-04-20" >> ~/.bashrc
echo "export PATH=$PATH:$WORK/SOFTWARE/apache-ant-1.9.6-bin/bin" >> ~/.bashrc
cd $CURRENT_DIRECTORY


