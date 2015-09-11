DROP TABLE IF EXISTS sentences CASCADE;
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


DROP TABLE IF EXISTS concept_mentions CASCADE;
CREATE TABLE concept_mentions(
  sentence_id text,
  start_position int,
  length int,
  text text,
  mention_id text  -- unique identifier for concept_mentions
  );


DROP TABLE IF EXISTS region_mentions CASCADE;
CREATE TABLE region_mentions(
  sentence_id text,
  start_position int,
  length int,
  text text,
  mention_id text  -- unique identifier for region_mentions
  );
