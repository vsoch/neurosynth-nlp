psql $DBNAME -c "
COPY (
 SELECT hsi.relation_id
      , s.sentence_id
      , description
      , is_true
      , expectation
      , s.words
      , c1.start_position AS c1_start
      , c1.length AS c1_length
      , c2.start_position AS c2_start
      , c2.length AS c2_length
      , c2.length AS c2_length
      -- also include all relevant features with weights
      , features[1:6] -- top 6 features with weights
      , weights[1:6]
   FROM has_related_concept_is_true_inference hsi
      , sentences s
      , concept_mentions c1
      , concept_mentions c2
      , ( -- find features relevant TO the relation
         SELECT relation_id
              , ARRAY_AGG(feature ORDER BY abs(weight) DESC) AS features
              , ARRAY_AGG(weight  ORDER BY abs(weight) DESC) AS weights
           FROM has_spouse_features f
              , dd_inference_result_variables_mapped_weights wm
          WHERE wm.description = ('f_has_related_concept_features-' || f.feature)
          GROUP BY relation_id
        ) f
  WHERE s.sentence_id  = hsi.sentence_id
    AND c1.mention_id  = hsi.concept1_id
    AND c2.mention_id  = hsi.concept2_id
    AND f.relation_id  = hsi.relation_id
    AND expectation    > 0.9
  ORDER BY random() LIMIT 100
) TO STDOUT WITH CSV HEADER;
" > inference/has_related_concept.csv
