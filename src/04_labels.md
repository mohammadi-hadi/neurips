# Naming the topics

The clusters from `03_cluster.py` are numbers. To turn them into readable names:

1. For each of the 150 subtopics, `clusters_fine.json` lists its most distinctive terms (class-based
   TF-IDF), the 20 titles closest to the cluster centre, 3 representative abstracts and 10 random titles.
2. A language model reads these in batches of 30 and proposes a short name, a one-sentence
   description, keywords and a coherence rating (do the random titles fit the name?).
3. An editing pass reads all 150 names together, names the 20 research areas from the subtopics
   they contain, and renames subtopics whose names overlap.
4. `04_apply_labels.py` merges the result into `labels.json`.

The names are a reading aid. The cluster assignments themselves come only from the embeddings.
