"""Robustness check: do the area-level shifts depend on fitting the clusters on 2026 papers?

Refit the 150 subtopics two other ways (on 2025 papers only, and on both years pooled), map each new
subtopic to the research area most of its papers had in the main fit, and recompute the area shares.
Writes outputs/robustness_areas.csv.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parents[1]
P, OUT = ROOT / "data/processed", ROOT / "outputs"
df = pd.read_parquet(P / "papers_clustered.parquet")
X = np.load(P / "embeddings.npy")
broad_name = {int(k): v["name"] for k, v in json.load(open(ROOT / "data/labels/labels.json"))["broad"].items()}
is25, is26 = (df.year == 2025).to_numpy(), (df.year == 2026).to_numpy()


def area_shares(area):
    s = {}
    for yr, m in (("2025", is25), ("2026", is26)):
        s[yr] = pd.Series(area[m]).map(broad_name).value_counts(normalize=True) * 100
    return pd.DataFrame(s)


rows = {"fit on 2026 (main)": area_shares(df.broad.to_numpy())}
for name, mask in (("fit on 2025", is25), ("fit on both years", is25 | is26)):
    km = KMeans(150, n_init=4, random_state=42).fit(X[mask])
    C = km.cluster_centers_ / np.linalg.norm(km.cluster_centers_, axis=1, keepdims=True)
    lab = np.argmax(X @ C.T, axis=1)
    to_area = pd.Series(df.broad.to_numpy()).groupby(lab).agg(lambda s: s.value_counts().idxmax())
    rows[name] = area_shares(to_area.reindex(lab).to_numpy())

out = pd.concat(rows, axis=1).round(2)
out.columns = [f"{fit} · {yr}" for fit, yr in out.columns]
for fit in rows:
    out[f"{fit} · change"] = (out[f"{fit} · 2026"] - out[f"{fit} · 2025"]).round(2)
out = out.sort_values("fit on 2026 (main) · change", ascending=False)
out.to_csv(OUT / "robustness_areas.csv")
print(out[[c for c in out.columns if "change" in c]].to_string())
