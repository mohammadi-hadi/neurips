"""Build the GitHub Pages site in docs/ in the style of mohammadi.cv:
docs/index.html (landing page), docs/2026/index.html (story), docs/2026/appendix.html, figures.
Needs pandoc on PATH."""
import html, re, shutil, subprocess
from pathlib import Path
from site_template import page, atlas_nav

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/2026"
SITE = "https://mohammadi.cv/neurips/2026/"
(DOCS / "figures").mkdir(parents=True, exist_ok=True)
for f in (ROOT / "outputs/figures").glob("*.png"):
    shutil.copy(f, DOCS / "figures" / f.name)

HEIGHTS = {"treemap": 820, "vocabulary": 740}
HERO = ('</div><section class="container atlas-hero" aria-label="map of all papers">'
        '<div class="map-frame"><iframe src="atlas.html" title="Map of all NeurIPS 2026 papers"></iframe>'
        '<button class="map-cover" type="button" onclick="this.remove()">'
        '<span>Click to explore the map</span></button></div>'
        '<div class="actions"><a class="btn" href="atlas.html">Open the map full screen</a>'
        '<a class="btn btn-ghost" href="papers.html">Search all papers</a></div></section><div class="post-wrap">')


def md_to_html(md_path):
    body = subprocess.run(["pandoc", str(md_path), "-f", "gfm", "-t", "html5"], capture_output=True,
                          text=True, check=True).stdout
    body = body.replace("../outputs/figures/", "figures/").replace(SITE, "")
    title = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    # images become figures with a caption from their alt text
    body = re.sub(r'<p>(<a href="[^"]*">)?<img src="([^"]+)" alt="([^"]*)"\s*/?>(</a>)?</p>',
                  lambda m: f'<figure>{m.group(1) or ""}<img src="{m.group(2)}" alt="{m.group(3)}" loading="lazy">'
                            f'{m.group(4) or ""}<figcaption>{m.group(3)}</figcaption></figure>', body)
    body = re.sub(r"<!--\s*atlas-hero\s*-->\s*<p><strong><a [^>]*>[^<]*</a></strong></p>", HERO, body)
    body = re.sub(r"<!--\s*interactive:\s*([a-z_]+)\s*-->",
                  lambda m: f'<iframe class="chart" style="height:{HEIGHTS.get(m.group(1), 680)}px" '
                            f'src="charts/{m.group(1)}.html" loading="lazy" title="interactive chart"></iframe>', body)
    return (html.unescape(re.sub(r"<[^>]+>", "", title.group(1))) if title else ""), body


def article(md_path, crumbs, dek, byline):
    title, body = md_to_html(md_path)
    return title, f"""{atlas_nav()}<main id="main"><article class="post">
<header class="post-head"><div class="post-wrap">
<p class="post-crumbs">{crumbs}</p><h1>{title}</h1><p class="post-dek">{dek}</p>
<p class="post-byline"><span>{byline}</span></p></div></header>
<div class="post-body"><div class="post-wrap">{body}</div></div></article></main>"""


CRUMBS = '<a href="/blog/">Blog</a><span class="sep">/</span><a href="../">NeurIPS Atlas</a>'
words = len(re.sub(r"[#*\[\]()!<>-]", " ", (ROOT / "report/BLOG.md").read_text()).split())
title, body = article(ROOT / "report/BLOG.md", CRUMBS,
                      "I put all 9,110 NeurIPS 2026 papers on one map and compared them with 2025. Agents are the big story.",
                      f"{round(words / 220)} min read · 20 October 2026")
(DOCS / "index.html").write_text(page(title, "All NeurIPS 2026 papers on one map, and what changed since 2025.",
                                      SITE, body))
print("wrote", DOCS / "index.html")

title, body = article(ROOT / "report/APPENDIX.md", CRUMBS + '<span class="sep">/</span><a href="index.html">2026</a>',
                      "Every NeurIPS 2026 area and topic with its numbers, and every oral.", "Reference")
body = body.replace('<div class="post-wrap">', '<div class="post-wrap wide">')
(DOCS / "appendix.html").write_text(page(title, "Every NeurIPS 2026 topic with its numbers, and every oral.",
                                         SITE + "appendix.html", body))
print("wrote", DOCS / "appendix.html")

(ROOT / "docs/.nojekyll").write_text("")
LANDING = f"""{atlas_nav("2026/")}<main id="main"><section class="hero"><div class="container">
<span class="kicker">Project</span><h1>NeurIPS Atlas</h1>
<p class="section-lede">What NeurIPS papers are about, and how that changes each year. Made from the public paper lists on neurips.cc.</p>
</div></section>
<section class="section"><div class="container">
<a href="2026/atlas.html"><img src="2026/figures/atlas_clusters.png" alt="Map of all NeurIPS 2026 papers"
 style="width:100%;border:1px solid var(--rule);border-radius:10px;background:#fff"></a>
<p style="text-align:center;margin-top:16px"><a class="btn" href="2026/atlas.html">Open the NeurIPS 2026 map</a>
<a class="btn btn-ghost" href="2026/papers.html">Search all papers</a></p>
<div class="prose" style="margin-top:28px">
<h2>Editions</h2>
<p><a href="2026/"><strong>NeurIPS 2026: the story.</strong></a> All 9,110 papers on one map, and what changed since 2025.</p>
<p><strong>NeurIPS through the years.</strong> Coming soon: how topics, submissions and countries changed since 2014.</p>
</div></div></section></main>"""
(ROOT / "docs/index.html").write_text(page("NeurIPS Atlas", "Maps and numbers on what NeurIPS papers are about.",
                                           "https://mohammadi.cv/neurips/", LANDING))
print("wrote", ROOT / "docs/index.html")
