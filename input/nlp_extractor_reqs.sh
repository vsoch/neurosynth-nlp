#!/usr/bin/env bash
# Set up / install sbt to compile to nlp_extractor in deepdive

CURRENT_DIRECTORY=$PWD
cd $HOME
mkdir SOFTWARE
cd SOFTWARE
wget https://dl.bintray.com/sbt/native-packages/sbt/0.13.9/sbt-0.13.9.tgz
tar xvfz sbt-0.13.9.tgz
wget http://downloads.typesafe.com/scala/2.11.7/scala-2.11.7.tgz
tar xvfz scala-2.11.7.tgz

echo "# Scala and sbt" >> ~/.bashrc
echo "export PATH=$PATH:$WORK/SOFTWARE/sbt/bin" >> ~/.bashrc
echo "export PATH=$PATH:$WORK/SOFTWARE/scala-2.11.7/bin" >> ~/.bashrc
cd $CURRENT_DIRECTORY
