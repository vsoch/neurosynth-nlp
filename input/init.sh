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
if ! [[ -e articles.csv ]]; then
    python extract_articles.py articles.csv
fi

# Create articles table
deepdive sql "
  CREATE TABLE articles(
    article_id bigint,    -- identifier of article
    text       text       -- all text in the article
  );
"

deepdive sql "COPY articles FROM STDIN CSV" <./articles.csv

# load the data into database
deepdive sql "COPY sentences FROM STDIN CSV" <./articles.csv
