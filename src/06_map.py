"""Interactive "atlas of change" and a static overview map of the NeurIPS 2026 papers (DataMapPlot).

The interactive map can be recoloured by research area, change since 2025, city, status,
industry involvement and team size, filtered by presentation day, and browsed with a topic tree."""
import re
import json
from pathlib import Path
import numpy as np
import pandas as pd
from common import load_papers, paper_orgs
import datamapplot

ROOT = Path(__file__).resolve().parents[1]
P, OUT, DOCS = ROOT / "data/processed", ROOT / "outputs", ROOT / "docs/2026"
(OUT / "figures").mkdir(parents=True, exist_ok=True)
DOCS.mkdir(exist_ok=True)

df = load_papers()
labels = json.load(open(ROOT / "data/labels/labels.json"))
fine_name = {int(k): v["name"] for k, v in labels["fine"].items()}
broad_name = {int(k): v["name"] for k, v in labels["broad"].items()}
imap = {r["raw"]: r for r in json.load(open(ROOT / "data/labels/institutions_map.json"))}

d26, d25 = df[df.year == 2026], df[df.year == 2025]
sh26 = d26.fine.value_counts(normalize=True)
sh25 = d25.fine.value_counts(normalize=True).reindex(sh26.index, fill_value=0)
growth = np.log2((sh26 + 0.0005) / (sh25 + 0.0005))  # per subtopic, 2026 vs 2025 share

d = d26.reset_index(drop=True)
coords = d[["x", "y"]].to_numpy()
fine_lab = d["fine"].map(fine_name).to_numpy()
broad_lab = d["broad"].map(broad_name).to_numpy()

status = d["decision"].map({"oral": "Oral", "spotlight": "Spotlight", "poster": "Poster"}).fillna("Decision not yet public")
city = d["site"].replace({"unscheduled": "City not listed", "": "City not listed"})


def sector(s):
    secs = {o[2] for o in paper_orgs(s)}
    if "industry" in secs and "academia" in secs:
        return "Academia + industry"
    if "industry" in secs:
        return "Industry only"
    if secs - {"unknown"}:
        return "Academia / public research"
    return "Unknown"


who = d["institutions"].map(sector)
g = d["fine"].map(growth).clip(-1.5, 1.5).to_numpy()  # symmetric scale: 1.5 = 2.8x more or less share
change_txt = [f"{fine_name[f]}: {100 * sh25[f]:.2f}% → {100 * sh26[f]:.2f}% of papers since 2025" for f in d["fine"]]

start = pd.to_datetime(d["start"], errors="coerce", utc=True)
local_tz = {"Sydney": "Australia/Sydney", "Atlanta": "America/New_York", "Paris": "Europe/Paris"}
day = []
for s, c in zip(start, city):
    if pd.isna(s) or c not in local_tz:
        day.append("Unscheduled")
    else:
        # one word per label ("08-Tue"): the histogram shows only the first word. Colour by city tells the cities apart
        day.append(s.tz_convert(local_tz[c]).strftime("%d-%a"))

title = d["title_display"]
hover = (title + " — " + status + " · " + city).to_numpy()
safe = title.str.replace(r"[`$\\]", "", regex=True)
GONE = set(json.load(open(ROOT / "data/labels/gone_from_program.json")))  # papers whose NeurIPS page is gone
extra = pd.DataFrame({
    "title": title, "safe_title": safe, "openreview": d["or_link"], "pdf": d["pdf_link"], "arxiv": d["arxiv"],
    "authors": d["authors"].str.slice(0, 160), "status": status, "city": city,
    "topic": d["fine"].map(fine_name), "area": d["broad"].map(broad_name), "change": change_txt,
    "where": [f"{c} · {s.tz_convert(local_tz[c]).strftime('%a %-d %b %H:%M')}, local time" if (c in local_tz and not pd.isna(s))
              else "" for s, c in zip(start, city)],
    "url": d["url"].where(~d["url"].str.rsplit("/", n=1).str[-1].isin(GONE), ""), "abstract": d["abstract"].str.slice(0, 420) + "…",
})
marker = np.where(d["decision"].isin(["oral", "spotlight"]), 7, 2.5)

cmap_raw = [g, city.to_numpy(), status.to_numpy(), who.to_numpy(), np.log2(d["n_authors"].clip(1, 40)).to_numpy()]
cmap_meta = [
    {"field": "growth", "description": "Change since 2025 (red grew, blue shrank)", "cmap": "RdBu_r", "kind": "continuous"},
    {"field": "city", "description": "City", "kind": "categorical",
     "color_mapping": {"Sydney": "#0b7285", "Atlanta": "#862e9c", "Paris": "#e8a20c", "City not listed": "#ced4da"}},
    {"field": "status", "description": "Oral, spotlight or poster", "kind": "categorical",
     "color_mapping": {"Oral": "#c92a2a", "Spotlight": "#f08c00", "Poster": "#adb5bd", "Decision not yet public": "#e9ecef"}},
    {"field": "sector", "description": "Academia or industry", "kind": "categorical",
     "color_mapping": {"Academia / public research": "#4c6ef5", "Academia + industry": "#ae3ec9",
                       "Industry only": "#e8590c", "Unknown": "#ced4da"}},
    {"field": "team", "description": "Number of authors", "cmap": "viridis", "kind": "continuous"},
]

CSS = """
#title-container{background:rgba(255,255,255,.94)!important;border-radius:10px;box-shadow:0 2px 12px rgba(31,42,68,.08);
  padding:14px 18px 13px!important;max-width:min(600px,calc(100vw - 48px));line-height:1.2!important}
#title-container br{display:none}
#main-title{display:block;font-family:"Source Serif 4",Georgia,serif!important;font-weight:600!important;font-size:30px!important;
  line-height:1.15!important;letter-spacing:-.01em;color:#1a1a1a!important;margin:0 0 6px;text-wrap:balance}
#title-container>span:not(#main-title){display:block;font-family:Inter,system-ui,sans-serif!important;font-size:14.5px!important;
  line-height:1.45!important;color:#444!important;text-wrap:pretty}
#paper-links{display:none;position:absolute;right:14px;bottom:60px;z-index:20;width:340px;background:#fff;
  border-radius:10px;box-shadow:0 6px 24px rgba(31,42,68,.18);padding:14px 16px;font:13px/1.4 Inter,system-ui,sans-serif;color:#1f2a44}
#paper-links .t{font-weight:700;margin:0 22px 10px 0}
#paper-links a{display:inline-block;margin:0 6px 6px 0;padding:6px 10px;border-radius:7px;background:#f1f3f5;color:#1f2a44;text-decoration:none;font-weight:600}
#paper-links a.main{background:#1e3a5f;color:#fff}
#paper-links .n{font-size:12px;color:#6b7489;margin:0 0 8px}
#paper-links .n:empty{display:none}
#paper-links .x{position:absolute;top:8px;right:10px;cursor:pointer;font-size:16px;color:#6b7489;border:0;background:none}
.embedded #topic-tree,.embedded #d3histogram-container,.embedded .atlas-back{display:none!important}
.embedded #title-container{display:none!important}
.atlas-back{position:absolute;bottom:14px;right:14px;z-index:10;font:600 13px Inter,system-ui,sans-serif;
  background:#1e3a5f;color:#fff;padding:8px 12px;border-radius:8px;text-decoration:none}
/* the loading box is wider than a phone */
#progress-container{max-width:calc(100vw - 24px)!important;box-sizing:border-box}
/* short windows: the topic tree scrolls instead of running under the colour menu */
#topic-tree{max-height:calc(100vh - 330px)!important;overflow:auto!important}
/* phones: placed last so these rules win over the ones above */
@media (max-width:768px){
  #main-title{font-size:21px!important;margin-bottom:4px}
  #title-container{padding:10px 12px!important}
  #title-container>span:not(#main-title){font-size:12.5px!important;line-height:1.4!important}
  .stack.top-left{max-height:44vh!important}
  #topic-tree{display:none!important}
  .stack.bottom-left{display:flex!important}  /* keep the colour menu on phones */
  #d3histogram-container{display:none!important}
  #colormap-selector-container{max-width:calc(100vw - 32px)!important;box-sizing:border-box}
  #colormap-selector-container .color-map-dropdown,#colormap-selector-container .color-map-selected{max-width:100%!important}
  .atlas-back{bottom:88px;right:12px;padding:7px 11px;font-size:12px}
  body:has(.color-map-options[style*="block"]) .atlas-back{visibility:hidden}  /* out of the way of the open menu */
  #paper-links{left:12px;right:12px;width:auto;bottom:132px}
}
"""

# the map page is linked from the posts: give it the same head as the other pages (viewport for phones,
# description, preview card, icon), and the site name in the tab title
def finish_head(page, title, desc, url, image):
    head = (f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="description" content="{desc}"><link rel="canonical" href="{url}">\n'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">\n'
            f'<meta property="og:url" content="{url}"><meta property="og:type" content="website">'
            f'<meta property="og:site_name" content="Hadi Mohammadi">\n'
            f'<meta property="og:image" content="{image}"><meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" href="/assets/img/favicon.png"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">\n')
    assert page.count("<head>") == 1 and "name=\"viewport\"" not in page
    page = page.replace("<head>", "<head>\n" + head)
    old = re.search(r"<title>(.*?)</title>", page, re.S)
    return page.replace(old.group(0), f"<title>{title} — Hadi Mohammadi</title>") if old else page.replace("</head>", f"<title>{title} — Hadi Mohammadi</title></head>")

nb = lambda a: np.char.replace(a.astype(str), "-", "\u2011")  # non-breaking hyphen: the topic tree wrapped 'Post-Training' as 'Post- Training'
plot = datamapplot.create_interactive_plot(
    coords, nb(fine_lab), nb(broad_lab),  # finest layer first
    hover_text=hover,
    extra_point_data=extra,
    hover_text_html_template="""<div style="max-width:440px;font-family:Inter,system-ui,sans-serif">
<div style="font-weight:700;font-size:14px;line-height:1.3">{title}</div>
<div style="opacity:.7;font-size:12px;margin:2px 0 6px">{authors}</div>
<div style="font-size:12px"><b>{status}</b> · {city} · <i>{area}</i></div>
<div style="font-size:12px;color:#d9480f;margin:2px 0 6px">{change}</div>
<div style="font-size:12px;opacity:.85">{abstract}</div>
<div style="font-size:11px;margin-top:6px;color:#1f2a44"><b>Click</b> for links to the paper.</div></div>""",
    on_click="showLinks(`{url}`, `{arxiv}`, `{openreview}`, `{pdf}`, `{safe_title}`, `{where}`)",
    marker_size_array=marker,
    title="NeurIPS 2026: every paper on one map",
    sub_title=f"Each dot is one of the {len(d):,} papers. Similar papers sit close together. Big dots are orals and "
              f"spotlights. Use the menu at the bottom left to colour by change since 2025, city or status.",
    enable_search=True,
    enable_topic_tree=True,
    colormap_rawdata=cmap_raw,
    colormap_metadata=cmap_meta,
    histogram_data=pd.Series(day),
    histogram_n_bins=40,
    histogram_settings={"histogram_title": "Poster day in December, local time. Click a bar to filter.",
                        "histogram_bin_unselected_fill_color": "#d0d7e2",
                        "histogram_bin_selected_fill_color": "#d9480f",
                        "histogram_width": 420, "histogram_height": 90},
    custom_css=CSS,
    custom_html='<a class="atlas-back" href="index.html">← Back to the story</a>'
                '<div id="paper-links"><button class="x" onclick="this.parentNode.style.display=\'none\'" '
                'aria-label="close">×</button><div class="t"></div><div class="n"></div><div class="l"></div></div>',
    custom_js="""
// When the map is embedded in the story page, keep it clean: only the map, search and the colour menu.
if (window.self !== window.top) {
  document.documentElement.classList.add('embedded');
}
function showLinks(page, arxiv, forum, pdf, title, where) {
  const box = document.getElementById('paper-links');
  box.querySelector('.t').textContent = title;
  box.querySelector('.n').textContent = where;
  let h = (page ? '<a class="main" href="' + page + '" target="_blank" rel="noopener">NeurIPS page</a>' : '') +
          '<a href="' + arxiv + '" target="_blank" rel="noopener">Find on arXiv</a>';
  if (forum) h += '<a href="' + forum + '" target="_blank" rel="noopener">OpenReview</a>' +
                  '<a href="' + pdf + '" target="_blank" rel="noopener">PDF</a>';
  box.querySelector('.l').innerHTML = h;
  box.style.display = 'block';
}
""",
    darkmode=False,
    font_family="Inter",
    cluster_boundary_polygons=True,
    initial_zoom_fraction=0.95,
)
plot.save(str(DOCS / "atlas.html"))
# pin the CDN libraries the page loads, so a future "latest" release cannot break it
page = (DOCS / "atlas.html").read_text().replace("apache-arrow@latest", "apache-arrow@21.2.0").replace("d3@latest", "d3@7")
# load the site's title font; without it the title falls back to Georgia Bold.
# Inter is left to DataMapPlot, which embeds its own copy and waits for it before drawing labels.
FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600&display=swap" rel="stylesheet" />'
anchor = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />'
assert page.count(anchor) == 1
page = page.replace(anchor, anchor + "\n" + FONT_LINK)
page = finish_head(page, "NeurIPS 2026: every paper on one map", f"All {len(d):,} NeurIPS 2026 papers on one interactive map. Search, zoom in and click any paper.",
                   "https://mohammadi.cv/neurips/2026/atlas.html", "https://mohammadi.cv/neurips/2026/figures/atlas_static.png")
(DOCS / "atlas.html").write_text(page)

BG, INK, MUTED = "#fbfaf7", "#1f2a44", "#6b7489"
for name, title in [("atlas_static.png", "NeurIPS 2026 paper atlas"), ("atlas_card.png", None)]:
    kw = dict(title=title, sub_title=f"{len(d):,} papers · 20 research areas · placed by what their abstracts say",
              title_keywords={"color": INK, "fontweight": "bold", "fontsize": 26},
              sub_title_keywords={"color": MUTED, "fontsize": 14}) if title else {}
    fig, ax = datamapplot.create_plot(
        coords, broad_lab, label_font_size=12 if title else 15, label_wrap_width=14, use_medoids=True,
        font_family="Helvetica Neue", label_over_points=True, dynamic_label_size=True,
        figsize=(14, 14), dpi=150, darkmode=False, **kw)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_visible(False)
    if title:
        fig.text(0.01, 0.01, "Data: NeurIPS 2026 accepted papers (neurips.cc) · Analysis: Hadi Mohammadi · "
                 "github.com/mohammadi-hadi/neurips", fontsize=10, color=MUTED)
    fig.savefig(OUT / "figures" / name, bbox_inches="tight", dpi=150, facecolor=BG)
print("saved", DOCS / "atlas.html")
