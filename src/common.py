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


# NeurIPS 2026 papers were still closed on OpenReview on 20 October 2026 ("You don't have permission to
# read this forum"). Keep the OpenReview and PDF buttons hidden until they open, then set this to True
# and rebuild (src/06_map.py, src/08_appendix.py, src/12_paper_index.py, src/09_build_site.py).
OPENREVIEW_PUBLIC = False
OPENREVIEW_NOTE = ("OpenReview and PDF links will appear here once NeurIPS makes the 2026 papers public on OpenReview. "
                   "Until then, each paper's NeurIPS page has the link." if not OPENREVIEW_PUBLIC else "")


def arxiv_search(title):
    """arXiv title search: finds the preprint today, while OpenReview is still closed."""
    # keep apostrophes: arXiv finds "Don't" but not "Don t"
    q = re.sub(r"[^\w\s'-]", " ", re.sub(r"[’‘]", "'", title))
    return "https://arxiv.org/search/?query=" + quote_plus(q) + "&searchtype=title"


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


_ORGS = None


def _org_lookup():
    global _ORGS
    if _ORGS is None:
        rows = json.load(open(ROOT / "data/labels/institutions_map.json"))
        by_raw = {r["raw"].strip(): (r["canonical"], r["country"], r["sector"]) for r in rows
                  if r["canonical"].strip().lower() not in ("", "unknown")}
        by_name = {}
        for c, ct, se in by_raw.values():
            by_name.setdefault(c.lower(), (c, ct, se))
        _ORGS = (by_raw, by_name)
    return _ORGS


def orgs_of(raw):
    """All organisations named in one affiliation string, e.g. 'MIT/Google' -> {MIT, Google}."""
    by_raw, by_name = _org_lookup()
    raw = raw.strip()
    found = set()
    hit = by_raw.get(raw) or by_name.get(raw.lower())
    if hit:
        found.add(hit)
    # strings that join several organisations
    for part in re.split(r"\s*(?:/|;|&|\band\b|\+)\s*", raw):
        part = part.strip(" ,()")
        h = by_raw.get(part) or by_name.get(part.lower())
        if h:
            found.add(h)
    if not found:  # 'Department of X, Some University': try each comma part
        for part in [p.strip() for p in raw.split(",")]:
            h = by_raw.get(part) or by_name.get(part.lower())
            if h:
                found.add(h)
    return found


def paper_orgs(institutions):
    """Organisations on a paper (institutions = ' | '-joined affiliation strings)."""
    out = set()
    for raw in str(institutions or "").split(" | "):
        if raw.strip():
            out |= orgs_of(raw)
    return out


def load_papers(drop_duplicates=True):
    """papers_clustered.parquet with schedule, links and titles refreshed from papers.parquet."""
    df = pd.read_parquet(P / "papers_clustered.parquet")
    labels = json.load(open(ROOT / "data/labels/labels.json"))
    moves = {int(k): int(v) for k, v in labels.get("broad_moves", {}).items()}
    df["broad"] = [moves.get(int(f), int(b)) for f, b in zip(df["fine"], df["broad"])]
    base = pd.read_parquet(P / "papers.parquet").set_index("uid")
    for c in ["site", "session", "room", "start", "end", "openreview", "scheduled", "decision", "dup"]:
        if c in base.columns:
            df[c] = df["uid"].map(base[c])
    titles = display_titles()
    df["title_display"] = df["uid"].map(titles).fillna(df["title"])
    df["pdf"] = df["openreview"].map(openreview_pdf)
    if drop_duplicates and "dup" in df.columns:
        df = df[~df["dup"].astype(bool)]  # keeps the original row index, so it still lines up with embeddings.npy
    df["arxiv"] = df["title_display"].map(arxiv_search)
    df["or_link"] = df["openreview"].fillna("") if OPENREVIEW_PUBLIC else ""
    df["pdf_link"] = df["pdf"].fillna("") if OPENREVIEW_PUBLIC else ""
    return df
