"""Generate report/APPENDIX.md: every area and subtopic with counts, shares and the orals."""
import json, re
from pathlib import Path
import pandas as pd
from common import load_papers, OPENREVIEW_NOTE

ROOT = Path(__file__).resolve().parents[1]
P, OUT = ROOT / "data/processed", ROOT / "outputs"
(ROOT / "report").mkdir(exist_ok=True)
df = load_papers()
L = json.load(open(ROOT / "data/labels/labels.json"))
fine = {int(k): v for k, v in L["fine"].items()}
broad = {int(k): v for k, v in L["broad"].items()}
d26, d25 = df[df.year == 2026], df[df.year == 2025]
n26, n25 = d26.fine.value_counts(), d25.fine.value_counts()
b26, b25 = d26.broad.value_counts(), d25.broad.value_counts()


def slug(name):
    """Anchor for an area heading, so the list at the top can link to it."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


order = sorted(broad, key=lambda b: -b26.get(b, 0))
lines = ["# All NeurIPS 2026 areas and topics", "",
         f"All 20 areas and 150 topics of NeurIPS 2026 ({len(d26):,} papers). For each topic you see what the papers do, "
         f"how many papers it has, and its share of all papers in 2025 and 2026. ★ counts its orals and spotlights.", "",
         OPENREVIEW_NOTE, "",
         "**Areas:** " + " · ".join(f"[{broad[b]['name']}](#{slug(broad[b]['name'])})" for b in order), ""]
for b in order:
    s26, s25 = 100 * b26.get(b, 0) / len(d26), 100 * b25.get(b, 0) / len(d25)
    lines += [f'<a id="{slug(broad[b]["name"])}"></a>', "",
              f"## {broad[b]['name']}: {b26.get(b, 0):,} papers ({s26:.1f}% of all, 2025: {s25:.1f}%)", "",
              broad[b]["one_line"], "", "| Topic | What the papers do | Papers | Share 2025 → 2026 | ★ |", "|---|---|---|---|---|"]
    fs = sorted([f for f in fine if (d26.fine == f).any() and d26.loc[d26.fine == f, "broad"].iloc[0] == b],
                key=lambda f: -n26.get(f, 0))
    for f in fs:
        g = d26[d26.fine == f]
        star = int(g.decision.isin(["oral", "spotlight"]).sum())
        lines.append(f"| {fine[f]['name']} | {fine[f]['one_line']} | {len(g)} | "
                     f"{100 * n25.get(f, 0) / len(d25):.2f}% → {100 * len(g) / len(d26):.2f}% | {star} |")
    orals = d26[(d26.broad == b) & (d26.decision == "oral")]
    orals = orals.iloc[orals.title_display.str.replace(r"^[^0-9A-Za-z]+", "", regex=True).str.lower().argsort(kind="stable")]
    if len(orals):
        lines += ["", f"### Orals ({len(orals)})", ""]
        for o in orals.itertuples():
            extra = f" · [OpenReview]({o.or_link}) · [PDF]({o.pdf_link})" if o.or_link else ""
            lines.append(f'- {o.title_display} · <span class="links">[NeurIPS page]({o.url}) · [Search arXiv]({o.arxiv}){extra}</span>')
    lines.append("")
S = "https://mohammadi.cv/neurips/2026/"
lines += ["## Explore", "", f"[The map]({S}atlas.html) · [All papers with poster times]({S}papers.html) · "
          f"[All topics]({S}charts/treemap.html) · [The 2026 story]({S}index.html) · [Code and data](https://github.com/mohammadi-hadi/neurips)", ""]
(ROOT / "report/APPENDIX.md").write_text("\n".join(lines))
print("wrote report/APPENDIX.md")
