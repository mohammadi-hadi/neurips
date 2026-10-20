"""Embed title + abstract of 2025 and 2026 papers with one open model, so both years share a space."""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data/processed"
LOCAL = ROOT / "models/Qwen3-Embedding-0.6B"  # same weights, fetched once with curl
MODEL = sys.argv[1] if len(sys.argv) > 1 else (str(LOCAL) if LOCAL.exists() else "Qwen/Qwen3-Embedding-0.6B")

df = pd.read_parquet(P / "papers.parquet")
texts = (df["title"] + ". " + df["abstract"]).tolist()
device = "mps" if torch.backends.mps.is_available() else "cpu"
model = SentenceTransformer(MODEL, device=device)
model.max_seq_length = 384

# longest first keeps padding small inside each batch
order = np.argsort([-len(t) for t in texts])
t0 = time.time()
emb = model.encode([texts[i] for i in order], batch_size=32, normalize_embeddings=True,
                   show_progress_bar=True, convert_to_numpy=True)
out = np.empty_like(emb)
out[order] = emb
np.save(P / "embeddings.npy", out.astype(np.float32))
(P / "embeddings_model.txt").write_text(Path(MODEL).name)
print(f"{len(texts)} texts, dim {out.shape[1]}, {time.time() - t0:.0f}s, {MODEL} on {device}")
