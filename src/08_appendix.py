"""Generate report/APPENDIX.md: every area and subtopic with counts, shares and the orals."""
import json
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

lines = ["# All areas and topics", "",
         f"All 20 areas and 150 topics of NeurIPS 2026 ({len(d26):,} papers). For each topic you see what the papers do, "
         f"how many there are, and its share of all papers in 2025 and 2026. ★ is the number of orals and spotlights.", "",
         OPENREVIEW_NOTE, ""]
for b in sorted(broad, key=lambda b: -b26.get(b, 0)):
    s26, s25 = 100 * b26.get(b, 0) / len(d26), 100 * b25.get(b, 0) / len(d25)
    lines += [f"## {broad[b]['name']}: {b26.get(b, 0):,} papers ({s26:.1f}% of all, 2025: {s25:.1f}%)", "",
              broad[b]["one_line"], "", "| Subtopic | What the papers do | 2026 | share 2025 → 2026 | ★ |", "|---|---|---|---|---|"]
    fs = sorted([f for f in fine if (d26.fine == f).any() and d26.loc[d26.fine == f, "broad"].iloc[0] == b],
                key=lambda f: -n26.get(f, 0))
    for f in fs:
        g = d26[d26.fine == f]
        star = int(g.decision.isin(["oral", "spotlight"]).sum())
        lines.append(f"| {fine[f]['name']} | {fine[f]['one_line']} | {len(g)} | "
                     f"{100 * n25.get(f, 0) / len(d25):.2f}% → {100 * len(g) / len(d26):.2f}% | {star} |")
    orals = d26[(d26.broad == b) & (d26.decision == "oral")]
    if len(orals):
        lines += ["", "**Orals**", ""]
        for o in orals.itertuples():
            extra = f" · [OpenReview]({o.or_link}) · [PDF]({o.pdf_link})" if o.or_link else ""
            lines.append(f"- {o.title_display}: [NeurIPS page]({o.url}) · [arXiv]({o.arxiv}){extra}")
    lines.append("")
(ROOT / "report/APPENDIX.md").write_text("\n".join(lines))
print("wrote report/APPENDIX.md")
