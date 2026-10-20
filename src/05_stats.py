"""Numbers and charts for the report: topics 2026 vs 2025, orals/spotlights, sites,
institutions, countries, sectors and keyword trends."""
import json, re
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
P, OUT = ROOT / "data/processed", ROOT / "outputs"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.bbox": "tight"})
INK, A26, A25 = "#1f2a44", "#d9480f", "#8aa1b1"

df = pd.read_pickle(P / "papers_clustered.pkl")
labels = json.load(open(ROOT / "data/labels/labels.json"))
fine_name = {int(k): v["name"] for k, v in labels["fine"].items()}
broad_name = {int(k): v["name"] for k, v in labels["broad"].items()}
df["broad_name"] = df["broad"].map(broad_name)
df["fine_name"] = df["fine"].map(fine_name)
d26, d25 = df[df.year == 2026], df[df.year == 2025]
S = {"n_2026": len(d26), "n_2025": len(d25)}

# ---------- topics: share 2026 vs 2025 ----------
def shares(col):
    a = d26[col].value_counts(normalize=True) * 100
    b = d25[col].value_counts(normalize=True) * 100
    t = pd.DataFrame({"share_2026": a, "share_2025": b}).fillna(0)
    t["n_2026"] = d26[col].value_counts()
    t["n_2025"] = d25[col].value_counts()
    t = t.fillna(0)
    t["delta_pp"] = t["share_2026"] - t["share_2025"]
    return t.sort_values("share_2026", ascending=False)

broad = shares("broad_name")
fine = shares("fine_name")
fine["growth_x"] = (fine["share_2026"] + 0.05) / (fine["share_2025"] + 0.05)
broad.round(2).to_csv(OUT / "topics_broad.csv")
fine.round(2).to_csv(OUT / "topics_fine.csv")
S["broad"] = broad.round(2).reset_index(names="topic").to_dict("records")
big = fine[(fine.n_2026 >= 40)]
S["fine_growers"] = big.sort_values("delta_pp", ascending=False).head(12).round(2).reset_index(names="topic").to_dict("records")
S["fine_shrinkers"] = fine[fine.n_2025 >= 30].sort_values("delta_pp").head(12).round(2).reset_index(names="topic").to_dict("records")
S["fine_largest"] = fine.head(15).round(2).reset_index(names="topic").to_dict("records")

fig, ax = plt.subplots(figsize=(8, 7))
b = broad.iloc[::-1]
y = np.arange(len(b))
ax.barh(y + 0.2, b["share_2026"], 0.4, color=A26, label="2026")
ax.barh(y - 0.2, b["share_2025"], 0.4, color=A25, label="2025")
ax.set_yticks(y, b.index)
ax.set_xlabel("% of accepted papers")
ax.set_title("Research areas at NeurIPS, 2026 vs 2025", loc="left", color=INK, fontweight="bold")
ax.legend(frameon=False, loc="lower right")
fig.savefig(FIG / "areas_2026_vs_2025.png"); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 6))
g = pd.concat([big.sort_values("delta_pp", ascending=False).head(10),
               fine[fine.n_2025 >= 30].sort_values("delta_pp").head(10)]).drop_duplicates().sort_values("delta_pp")
ax.barh(g.index, g["delta_pp"], color=[A26 if v > 0 else A25 for v in g["delta_pp"]])
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlabel("change in share of papers (percentage points)")
ax.set_title("Fastest-growing and shrinking subtopics", loc="left", color=INK, fontweight="bold")
fig.savefig(FIG / "subtopic_movers.png"); plt.close(fig)

# ---------- orals and spotlights ----------
known = d26[d26.decision != "unknown"]
hi = known.assign(high=known.decision.isin(["oral", "spotlight"]))
rate = hi.groupby("broad_name").agg(papers=("high", "size"), orals=("decision", lambda s: (s == "oral").sum()),
                                     spotlights=("decision", lambda s: (s == "spotlight").sum()), rate=("high", "mean"))
rate["rate_pct"] = rate["rate"] * 100
rate = rate.sort_values("rate_pct", ascending=False)
S["decision_counts"] = d26.decision.value_counts().to_dict()
S["highlight_rate_overall_pct"] = round(hi.high.mean() * 100, 2)
S["highlight_rate_by_area"] = rate.round(2).reset_index().to_dict("records")
S["orals"] = d26[d26.decision == "oral"][["title", "fine_name", "broad_name", "url"]].to_dict("records")

fig, ax = plt.subplots(figsize=(8, 6))
r = rate.iloc[::-1]
ax.barh(r.index, r["rate_pct"], color=A26)
ax.axvline(hi.high.mean() * 100, color=INK, ls="--", lw=0.8)
ax.set_xlabel("% of papers selected as oral or spotlight")
ax.set_title("Where the orals and spotlights went", loc="left", color=INK, fontweight="bold")
fig.savefig(FIG / "highlight_rate_by_area.png"); plt.close(fig)

# ---------- sites ----------
sch = d26[d26.site.isin(["Sydney", "Atlanta", "Paris"])]
S["site_counts"] = d26.site.value_counts().to_dict()
mix = pd.crosstab(sch.broad_name, sch.site, normalize="index") * 100
overall = sch.site.value_counts(normalize=True) * 100
S["site_overall_pct"] = overall.round(2).to_dict()
mix = mix[["Sydney", "Atlanta", "Paris"]]
mix["sydney_vs_avg_pp"] = mix["Sydney"] - overall["Sydney"]
mix = mix.sort_values("Sydney", ascending=False)
mix.round(2).to_csv(OUT / "site_mix_by_area.csv")
S["site_mix_by_area"] = mix.round(2).reset_index().to_dict("records")

fig, ax = plt.subplots(figsize=(8, 7))
m = mix.iloc[::-1]
left = np.zeros(len(m))
for site_, col in [("Sydney", A26), ("Atlanta", "#5c7cfa"), ("Paris", "#94d82d")]:
    ax.barh(m.index, m[site_], left=left, color=col, label=site_)
    left += m[site_].to_numpy()
ax.set_xlim(0, 100)
ax.set_xlabel("% of the area's scheduled posters")
ax.set_title("Which site presents which research (scheduled posters)", loc="left", color=INK, fontweight="bold")
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.08))
fig.savefig(FIG / "site_mix_by_area.png"); plt.close(fig)

# ---------- institutions, countries, sectors ----------
imap = {}
if (ROOT / "data/labels/institutions_map.json").exists():
    imap = {r["raw"]: r for r in json.load(open(ROOT / "data/labels/institutions_map.json"))}


def canon(raw):
    raw = raw.strip()
    if raw in imap:
        return imap[raw]["canonical"], imap[raw]["country"], imap[raw]["sector"]
    parts = [p.strip() for p in raw.split(",")]
    base = parts[0] if parts else raw
    if base in imap:
        r = imap[base]
        return r["canonical"], r["country"], r["sector"]
    return base, "unmapped", "unknown"


def paper_orgs(s):
    return {canon(x) for x in s.split(" | ") if x.strip()}

for year, d in [(2026, d26), (2025, d25)]:
    orgs = d["institutions"].map(paper_orgs)
    inst = Counter(o[0] for os_ in orgs for o in {(c, k, s) for c, k, s in os_})
    ctry = Counter(c for os_ in orgs for c in {o[1] for o in os_})
    has_ind = orgs.map(lambda os_: any(o[2] == "industry" for o in os_))
    has_acad = orgs.map(lambda os_: any(o[2] == "academia" for o in os_))
    mapped = orgs.map(lambda os_: any(o[1] != "unmapped" for o in os_))
    S[f"institutions_{year}"] = inst.most_common(40)
    # share among papers with at least one mapped affiliation, so coverage differences between years cancel out
    n_mapped = int(mapped.sum()) if len(d) else 1
    S[f"countries_{year}"] = [(c, n, round(100 * n / n_mapped, 1)) for c, n in ctry.most_common(25) if c not in ("unmapped", "unknown")]
    S[f"industry_share_{year}"] = round(100 * has_ind[mapped].mean(), 1)
    S[f"industry_only_share_{year}"] = round(100 * (has_ind & ~has_acad)[mapped].mean(), 1)
    S[f"papers_with_mapped_org_{year}"] = round(100 * mapped.mean(), 1)

top = S["institutions_2026"][:25][::-1]
fig, ax = plt.subplots(figsize=(7, 7))
ax.barh([t[0] for t in top], [t[1] for t in top], color=A26)
ax.set_xlabel("papers with at least one author from the organisation")
ax.set_title("Most frequent organisations, NeurIPS 2026", loc="left", color=INK, fontweight="bold")
fig.savefig(FIG / "top_institutions.png"); plt.close(fig)

c26 = dict((c, p) for c, _, p in S["countries_2026"])
c25 = dict((c, p) for c, _, p in S["countries_2025"])
cs = [c for c, _, _ in S["countries_2026"][:12]][::-1]
fig, ax = plt.subplots(figsize=(7, 5))
yy = np.arange(len(cs))
ax.barh(yy + 0.2, [c26.get(c, 0) for c in cs], 0.4, color=A26, label="2026")
ax.barh(yy - 0.2, [c25.get(c, 0) for c in cs], 0.4, color=A25, label="2025")
ax.set_yticks(yy, cs)
ax.set_xlabel("% of papers (with a mapped affiliation) that have an author from the country")
ax.set_title("Countries behind the papers", loc="left", color=INK, fontweight="bold")
ax.legend(frameon=False, loc="lower right")
fig.savefig(FIG / "countries.png"); plt.close(fig)

# ---------- team size ----------
S["authors_mean"] = {2026: round(d26.n_authors.mean(), 2), 2025: round(d25.n_authors.mean(), 2)}
S["authors_median"] = {2026: float(d26.n_authors.median()), 2025: float(d25.n_authors.median())}
S["single_author_pct"] = {2026: round(100 * (d26.n_authors == 1).mean(), 2), 2025: round(100 * (d25.n_authors == 1).mean(), 2)}
S["10plus_author_pct"] = {2026: round(100 * (d26.n_authors >= 10).mean(), 2), 2025: round(100 * (d25.n_authors >= 10).mean(), 2)}

# ---------- vocabulary trends (share of abstracts mentioning a term) ----------
TERMS = {
    "LLM / large language model": r"\bLLMs?\b|large language model",
    "agent / agentic": r"\bagent(s|ic)?\b",
    "reasoning": r"\breason(ing)?\b",
    "chain-of-thought": r"chain[- ]of[- ]thought|\bCoT\b",
    "test-time compute / scaling": r"test[- ]time",
    "reinforcement learning": r"reinforcement learning|\bRL\b",
    "RLVR / GRPO": r"\bGRPO\b|\bRLVR\b|verifiable reward",
    "diffusion": r"\bdiffusion\b",
    "flow matching": r"flow[- ]matching",
    "transformer": r"\btransformers?\b",
    "state-space / Mamba": r"state[- ]space model|\bmamba\b|\bSSMs?\b",
    "multimodal / VLM": r"multi-?modal|\bVLMs?\b|vision[- ]language",
    "world model": r"world models?",
    "robot": r"\brobot",
    "video": r"\bvideo",
    "3D / Gaussian splatting": r"\b3D\b|gaussian splatting",
    "benchmark": r"\bbenchmark",
    "safety / alignment": r"\bsafety\b|\balignment\b|jailbreak",
    "interpretability": r"interpretab|mechanistic|sparse autoencoder",
    "LLM-as-a-judge / evaluator": r"as[- ]a[- ]judge|LLM judges?|judge model|reward model",
    "federated learning": r"federated",
    "graph neural network": r"graph neural|\bGNNs?\b",
    "privacy / differential privacy": r"differential(ly)? priva|\bprivacy\b",
    "theory / regret / bounds": r"\bregret\b|generalization bound|sample complexity|convergence rate",
    "science (protein / molecule / materials)": r"protein|molecul|material|drug",
    "medical / clinical": r"medical|clinical|patient",
    "quantum": r"\bquantum\b",
    "efficient / efficiency": r"\befficien(t|cy)\b",
}
rows = []
for name, pat in TERMS.items():
    rx = re.compile(pat, re.I)
    a = (d26.title + " " + d26.abstract).map(lambda t: bool(rx.search(t))).mean() * 100
    b = (d25.title + " " + d25.abstract).map(lambda t: bool(rx.search(t))).mean() * 100
    rows.append({"term": name, "pct_2026": round(a, 1), "pct_2025": round(b, 1), "delta_pp": round(a - b, 1)})
vt = pd.DataFrame(rows).sort_values("delta_pp", ascending=False)
vt.to_csv(OUT / "vocabulary_trends.csv", index=False)
S["vocabulary"] = vt.to_dict("records")

fig, ax = plt.subplots(figsize=(8, 7))
v = vt.iloc[::-1]
ax.barh(v.term, v.delta_pp, color=[A26 if x > 0 else A25 for x in v.delta_pp])
for i, (p26, d) in enumerate(zip(v.pct_2026, v.delta_pp)):
    ax.text(d + (0.3 if d >= 0 else -0.3), i, f"{p26:.0f}%", va="center", ha="left" if d >= 0 else "right", fontsize=8, color=INK)
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlabel("change in % of abstracts mentioning the term, 2025 → 2026 (label = 2026 share)")
ax.set_title("What the abstracts talk about more (and less)", loc="left", color=INK, fontweight="bold")
fig.savefig(FIG / "vocabulary_trends.png"); plt.close(fig)

json.dump(S, open(OUT / "stats.json", "w"), indent=1, default=str)
print("broad areas:", len(broad), "| orals", S["decision_counts"].get("oral"), "| industry share 2026", S["industry_share_2026"])
