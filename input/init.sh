#!/usr/bin/env bash
# A script for initializing database for the spouse example in DeepDive's walk-through
set -eux
cd "$(dirname "$0")"  # move into the directory where this script is

# If neurosynth data not downloaded, get it
if ! [[ -e database.txt ]]; then
    echo "Downloading neurosynth-data..."
    git clone https://github.com/neurosynth/neurosynth-data
    tar -xzvf neurosynth-data/current_data.tar.gz
    rm -rf neurosynth-data
fi

# If articles not extracted, extract them
if ! [[ -e articles.txt ]]; then
    python extract_articles.py articles.txt
fi

# Create articles table
deepdive sql "
  CREATE TABLE articles(
    article_id bigint,    -- identifier of article
    text       text       -- all text in the article
  );
"

deepdive sql "COPY articles FROM STDIN DELIMITER AS '|'" <./articles.txt

# Compile the Stanford parser
if hash sbt 2>/dev/null; then
    echo "Please see nlp_extractor_reqs.sh to set up sbt for the nlp_extractor"
else
    cd $DEEPDIVE_HOME/examples/nlp_extractor
    sbt stage
    cd "$(dirname "$0")"
fi

# Create sentences table
deepdive sql "
  CREATE TABLE sentences(
    document_id text,
    sentence text,
    words text[],
    lemma text[],
    pos_tags text[],
    dependencies text[],
    ner_tags text[],
    sentence_offset bigint,
    sentence_id text -- unique identifier for sentences
);
"

# load the data into database
deepdive sql "COPY sentences FROM STDIN CSV" <./articles.csv

