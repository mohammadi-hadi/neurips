"""Interactive and static maps of the NeurIPS 2026 papers (DataMapPlot)."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import datamapplot

ROOT = Path(__file__).resolve().parents[1]
P, OUT, DOCS = ROOT / "data/processed", ROOT / "outputs", ROOT / "docs"
(OUT / "figures").mkdir(parents=True, exist_ok=True)
DOCS.mkdir(exist_ok=True)

df = pd.read_parquet(P / "papers_clustered.parquet")
labels = json.load(open(ROOT / "data/labels/labels.json"))
fine_name = {int(k): v["name"] for k, v in labels["fine"].items()}
broad_name = {int(k): v["name"] for k, v in labels["broad"].items()}

d = df[df["year"] == 2026].reset_index(drop=True)
coords = d[["x", "y"]].to_numpy()
broad_lab = d["broad"].map(broad_name).to_numpy()
fine_lab = d["fine"].map(fine_name).to_numpy()

status = d["decision"].replace({"unknown": "poster"}).str.capitalize()
site = d["site"].replace({"unscheduled": "not yet scheduled", "": "not yet scheduled"})
hover = (d["title"] + " — " + status + " · " + site).to_numpy()
extra = pd.DataFrame({
    "title": d["title"], "authors": d["authors"].str.slice(0, 160),
    "status": status, "site": site, "topic": d["fine"].map(fine_name),
    "url": d["url"], "abstract": d["abstract"].str.slice(0, 400) + "…",
})
marker = np.where(d["decision"].isin(["oral", "spotlight"]), 6, 2)

plot = datamapplot.create_interactive_plot(
    coords, fine_lab, broad_lab,  # finest layer first
    hover_text=hover,
    extra_point_data=extra,
    hover_text_html_template="""<div style="max-width:420px">
<b>{title}</b><br><span style="opacity:.75">{authors}</span><br>
<span>{status} · {site}</span><br><i>{topic}</i><hr style="margin:4px 0">{abstract}</div>""",
    on_click="window.open(`{url}`)",
    marker_size_array=marker,
    title="NeurIPS 2026 · paper atlas",
    sub_title=f"{len(d):,} accepted papers, clustered by abstract. Bigger dots = orals and spotlights. Click a dot to open the paper.",
    enable_search=True,
    darkmode=False,
    font_family="Inter",
    cluster_boundary_polygons=True,
    initial_zoom_fraction=0.95,
)
plot.save(str(DOCS / "atlas.html"))
# pin the CDN libraries the page loads, so a future "latest" release cannot break it
page = (DOCS / "atlas.html").read_text().replace("apache-arrow@latest", "apache-arrow@21.2.0")
(DOCS / "atlas.html").write_text(page)

fig, ax = datamapplot.create_plot(
    coords, broad_lab, title="NeurIPS 2026 paper atlas",
    sub_title=f"{len(d):,} papers · 20 research areas · clustered by abstract",
    label_font_size=9, label_wrap_width=16, use_medoids=True,
    figsize=(14, 14), dpi=150, darkmode=False,
)
fig.savefig(OUT / "figures/atlas_static.png", bbox_inches="tight", dpi=150)
print("saved", DOCS / "atlas.html")
