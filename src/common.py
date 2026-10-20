"""Shared helpers: readable titles and the paper table with up-to-date schedule and links."""
import csv, html, json, re
from urllib.parse import quote_plus
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, P = ROOT / "data/raw", ROOT / "data/processed"

GREEK = {name: chr(cp) for name, cp in [
    ("alpha", 0x3B1), ("beta", 0x3B2), ("gamma", 0x3B3), ("delta", 0x3B4), ("epsilon", 0x3B5), ("varepsilon", 0x3B5),
    ("zeta", 0x3B6), ("eta", 0x3B7), ("theta", 0x3B8), ("kappa", 0x3BA), ("lambda", 0x3BB), ("mu", 0x3BC),
    ("nu", 0x3BD), ("xi", 0x3BE), ("pi", 0x3C0), ("rho", 0x3C1), ("sigma", 0x3C3), ("tau", 0x3C4), ("phi", 0x3C6),
    ("varphi", 0x3C6), ("chi", 0x3C7), ("psi", 0x3C8), ("omega", 0x3C9), ("Gamma", 0x393), ("Delta", 0x394),
    ("Theta", 0x398), ("Lambda", 0x39B), ("Pi", 0x3A0), ("Sigma", 0x3A3), ("Phi", 0x3A6), ("Psi", 0x3A8), ("Omega", 0x3A9)]}
SYMBOLS = {"ell": "ℓ", "infty": "∞", "times": "×", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "to": "→",
           "rightarrow": "→", "sqrt": "√", "cdot": "·", "approx": "≈", "sim": "~", "pm": "±", "star": "*",
           "partial": "∂", "nabla": "∇", "log": "log", "mathcal": "", "mathbf": "", "mathrm": "", "boldsymbol": "",
           "text": "", "textbf": "", "textit": "", "mathbb": "", "emph": "", "operatorname": "", "texttt": ""}


def tex_to_text(s):
    """Turn inline LaTeX in titles into readable text: '$\\gamma$-weakly' -> 'γ-weakly'."""
    s = html.unescape(s or "")

    def inner(m):
        t = m.group(1)
        t = re.sub(r"\\([A-Za-z]+)", lambda c: GREEK.get(c.group(1), SYMBOLS.get(c.group(1), c.group(1))), t)
        return re.sub(r"[{}$]|\\,|\\ |\\!", "", t).replace("^", "").replace("_", "")
    s = re.sub(r"\$([^$]*)\$", inner, s)
    s = re.sub(r"\\([A-Za-z]+)", lambda c: GREEK.get(c.group(1), SYMBOLS.get(c.group(1), c.group(1))), s)
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "")).strip()


def openreview_pdf(forum):
    return forum.replace("/forum?id=", "/pdf?id=") if forum else ""


OPENREVIEW_NOTE = ("NeurIPS has not made the 2026 papers public on OpenReview yet (checked 20 October 2026). "
                   "Those links will work once they do.")


def arxiv_search(title):
    """arXiv title search: finds the preprint today, while OpenReview is still closed."""
    return "https://arxiv.org/search/?query=" + quote_plus(re.sub(r"[^\w\s-]", " ", title)) + "&searchtype=title"


def display_titles():
    """uid -> readable title, from the raw exports (same uid scheme as 01_prepare)."""
    out = {}
    for year in (2026, 2025):
        rows = list(csv.DictReader(open(RAW / f"neurips{year}_papers_abstracts.csv", encoding="utf-8")))
        seen = {}
        for r in rows:
            vid = r["virtualsite_url"].rstrip("/").split("/")[-1]
            k = seen.get(vid, 0); seen[vid] = k + 1
            out[f"{year}_{vid}_{k}"] = tex_to_text(r["name"])
    return out


def load_papers():
    """papers_clustered.parquet with schedule, links and titles refreshed from papers.parquet."""
    df = pd.read_parquet(P / "papers_clustered.parquet")
    base = pd.read_parquet(P / "papers.parquet").set_index("uid")
    for c in ["site", "session", "room", "start", "end", "openreview", "scheduled", "decision"]:
        if c in base.columns:
            df[c] = df["uid"].map(base[c])
    titles = display_titles()
    df["title_display"] = df["uid"].map(titles).fillna(df["title"])
    df["pdf"] = df["openreview"].map(openreview_pdf)
    df["arxiv"] = df["title_display"].map(arxiv_search)
    return df
