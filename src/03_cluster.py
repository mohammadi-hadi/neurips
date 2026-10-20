"""Two-level topic structure fitted on 2026 papers only; 2025 papers are assigned to the
nearest 2026 subtopic, so year-over-year shares are measured on the same taxonomy."""
import json, re
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
import umap

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data/processed"
N_FINE, N_BROAD, SEED = 150, 20, 42

df = pd.read_pickle(P / "papers.pkl")
X = np.load(P / "embeddings.npy")
is26 = (df["year"] == 2026).to_numpy()

# fine level: k-means on the unit-normalised embeddings (cosine geometry)
km = KMeans(N_FINE, n_init=10, random_state=SEED).fit(X[is26])
C = km.cluster_centers_ / np.linalg.norm(km.cluster_centers_, axis=1, keepdims=True)
fine = np.argmax(X @ C.T, axis=1)  # 2026 and 2025 alike
df["fine"] = fine
df["sim_to_centroid"] = (X * C[fine]).sum(1)

# broad level: group the fine centroids, weighted by cluster size
sizes = np.bincount(fine[is26], minlength=N_FINE)
kb = KMeans(N_BROAD, n_init=20, random_state=SEED).fit(C, sample_weight=sizes)
df["broad"] = kb.labels_[df["fine"]]

# 2D map for 2026 (and 2025 projected into the same map)
red = umap.UMAP(n_neighbors=30, min_dist=0.05, metric="cosine", random_state=SEED).fit(X[is26])
xy = np.zeros((len(df), 2), dtype=np.float32)
xy[is26] = red.embedding_
xy[~is26] = red.transform(X[~is26])
df["x"], df["y"] = xy[:, 0], xy[:, 1]

# distinctive terms per fine cluster (class-based tf-idf over 2026 docs)
stop = list(ENGLISH_STOP_WORDS | {"model", "models", "method", "methods", "propose", "proposed", "results",
                                   "paper", "approach", "show", "based", "learning", "data", "existing",
                                   "performance", "new", "novel", "task", "tasks", "using", "achieves",
                                   "framework", "state", "art", "experiments", "demonstrate", "work"})
d26 = df[is26]
docs = d26.groupby("fine").apply(lambda g: " ".join(g["title"] + " " + g["abstract"])).reindex(range(N_FINE), fill_value="")
tf = TfidfVectorizer(stop_words=stop, ngram_range=(1, 2), min_df=2, max_df=0.5, sublinear_tf=True,
                     token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9\-]{2,}\b")
M = tf.fit_transform(docs)
vocab = np.array(tf.get_feature_names_out())

clusters = []
for c in range(N_FINE):
    g = d26[d26["fine"] == c].sort_values("sim_to_centroid", ascending=False)
    row = M[c].toarray().ravel()
    terms = vocab[np.argsort(-row)[:15]].tolist()
    official = g["official_topic"][g["official_topic"] != ""].value_counts().head(3).to_dict()
    clusters.append({
        "fine_id": c, "broad_id": int(kb.labels_[c]), "n_2026": int(len(g)),
        "n_2025": int(((df["year"] == 2025) & (df["fine"] == c)).sum()),
        "top_terms": terms, "official_topics_sample": official,
        "representative_titles": g["title"].head(20).tolist(),
        "representative_abstracts": [a[:600] for a in g["abstract"].head(3)],
        "random_titles": g["title"].sample(min(10, len(g)), random_state=SEED).tolist(),
    })
json.dump(clusters, open(P / "clusters_fine.json", "w"), indent=1)

broad = []
for b in range(N_BROAD):
    fs = [c for c in clusters if c["broad_id"] == b]
    broad.append({"broad_id": b, "n_2026": sum(c["n_2026"] for c in fs), "fine_ids": [c["fine_id"] for c in fs]})
json.dump(broad, open(P / "clusters_broad.json", "w"), indent=1)
df.drop(columns=[]).to_pickle(P / "papers_clustered.pkl")
print("fine sizes 2026: min", sizes.min(), "median", int(np.median(sizes)), "max", sizes.max())
print("broad sizes:", sorted((b["n_2026"] for b in broad), reverse=True))
