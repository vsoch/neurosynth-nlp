# Named Entity Recognition

For neuroimages

This is supplementary data from [cite](http://bioinformatics.oxfordjournals.org/content/31/10/1640.full)

The files `aba-syn.xml` and `bams2004swanson-syn.xml` are compiled into [one json file](brain_regions.json). In this file:

  - all parent regions were original defined under "canonical" attribute of <token>
  - children of parents were defined under "base" attribute of <variant>
  - unique children for each parent are combined into one data structure
  - the "variants" attribute includes the parent name, so when parsing, be careful to not include the parent twice. The parent just serves as a "representative" for all variations in the region group.
  - the "ref_id" from each parent of each file was extracted into a list, if existing.
