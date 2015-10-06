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

# Prepare the stanford nlp parser
bash ../slurm/0.prep_core_nlp.sh

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
    sentence_id text
);
"

# If the compiled brain regions file doesn't exist, create it
if ! [[ -e ../udf/NER/brain_regions.json ]]; then
    echo "Generating compiled brain regions json..."
    python ../udf/NER/compile_brain_regions.py ../udf/NER/brain_regions.json "../udf/NER/aba-syn.xml,../udf/NER/bams2004swanson-syn.xml"
fi

# Run nlp extractor to parse into table
# NOTE: IMPORTANT: This will / should be sent to run on the TACC grid
#deepdive run nlp_extract
DEEPDIVE_JDBC_URL='jdbc:postgresql://db1.wrangler.tacc.utexas.edu:5432/deepdive_spouse?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory' deepdive run nlp_extract

# If you get this error:
# ERROR:  must be superuser to create procedural language "plpythonu"
# You or an admin must do:
# sudo apt-get install postgresql-plpython
# deepdive sql 'CREATE LANGUAGE plpythonu;'

# Create tables for mentions
deepdive sql "
  CREATE TABLE concept_mentions(
    sentence_id text,
    start_position int,
    length int,
    text text,
    mention_id text
);
"

deepdive sql "
  CREATE TABLE region_mentions(
    sentence_id text,
    start_position int,
    length int,
    text text,
    mention_id text 
  );
"

# Run pipeline to extract mentions of concepts and regions
# Not tested - this was also done manually because of SSL issues
DEEPDIVE_JDBC_URL='jdbc:postgresql://db1.wrangler.tacc.utexas.edu:5432/deepdive_spouse?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory' deepdive run mentions_extract

# Now we will extract candidates for has_cognitive_process relations, 
# the simplest thing to do is have them in the same sentence

# this is for concept --> concept associations
# we can train this using the cognitive atlas
# however we will need negative assertions as well

# this is for region --> concept associations 
deepdive sql "
CREATE TABLE has_cognitive_concept(
    region_id text,
    concept_id text,
    sentence_id text,
    description text,
    is_true boolean,
    relation_id text,
    id bigint 
);
"

deepdive sql "
CREATE TABLE has_related_concept(
  concept1_id text,
  concept2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, 
  id bigint
);
"

deepdive sql "
CREATE TABLE has_cognitive_concept_features(
  relation_id text,
  feature text
);
"

deepdive sql "
CREATE TABLE has_related_concept_features(
  relation_id text,
  feature text
);
"

# First try extracting related concepts - we only need concept_mentions for this
DEEPDIVE_JDBC_URL='jdbc:postgresql://db1.wrangler.tacc.utexas.edu:5432/deepdive_spouse?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory' deepdive run has_related_concept
