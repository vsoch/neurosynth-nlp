CREATE TABLE articles(
    article_id bigint,    -- identifier of article
    text       text       -- all text in the article
);

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


CREATE TABLE concept_mentions(
  sentence_id text,
  start_position int,
  length int,
  text text,
  mention_id text  -- unique identifier for concept_mentions
  );


CREATE TABLE region_mentions(
  sentence_id text,
  start_position int,
  length int,
  text text,
  mention_id text  -- unique identifier for region_mentions
);

CREATE TABLE has_cognitive_concept(
  region_id text,
  concept_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for has_cognitive_concept
  id bigint   -- reserved for DeepDive
);

CREATE TABLE has_cognitive_concept_features(
  relation_id text,
  feature text);
);

CREATE TABLE has_related_concept(
  concept1_id text,
  concept2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, 
  id bigint   -- reserved for DeepDive
);


CREATE TABLE has_related_concept_features(
  relation_id text,
  feature text);
);
