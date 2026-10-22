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
        '<div class="map-frame"><img class="map-preview" src="figures/atlas_clusters.png" '
        'alt="Map of all NeurIPS 2026 papers, coloured by research area">'
        '<button class="map-cover" type="button" onclick="openMap(this)"><span>Explore the map</span></button></div>'
        '<div class="actions"><a class="btn" href="atlas.html">Open the map full screen</a>'
        '<a class="btn btn-ghost" href="papers.html">Search all papers</a></div></section>'
        # the live map only loads on click; on small screens it opens full screen instead
        '<script>function openMap(b){if(window.innerWidth<900){location.href="atlas.html";return;}'
        'b.parentNode.innerHTML=\'<iframe src="atlas.html" title="Map of all NeurIPS 2026 papers"></iframe>\';}</script>'
        '<div class="post-wrap">')


PHONE_LABELS = {"★": "Orals and spotlights"}  # the share column reads "Share 2025 → 2026: 1.18% → 1.12%" otherwise


def label_cells(body):
    """Gives each number cell of a table its column name, so on a phone a row can be shown as a card."""
    def table(m):
        heads = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", m.group(0), re.S)]
        def row(r):
            cells = iter(range(10**6))
            return re.sub(r"<td>", lambda _: (lambda i: f'<td data-label="{html.escape(PHONE_LABELS.get(heads[i], "Share" if heads[i].startswith("Share") else heads[i]))}">'
                                                         if 2 <= i < len(heads) else "<td>")(next(cells)), r.group(0))
        return re.sub(r"<tr>.*?</tr>", row, m.group(0), flags=re.S)
    return re.sub(r"<table>.*?</table>", table, body, flags=re.S)

def img_size(src):
    """width and height of a figure, so the page does not jump while the images load."""
    from PIL import Image
    f = DOCS / src
    if not f.exists():
        return ""
    w, h = Image.open(f).size
    return f'width="{w}" height="{h}" '

def md_to_html(md_path):
    body = subprocess.run(["pandoc", str(md_path), "-f", "gfm", "-t", "html5", "--wrap=none"], capture_output=True,
                          text=True, check=True).stdout
    body = body.replace("../outputs/figures/", "figures/").replace(SITE, "")
    title = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    # images become figures with a caption from their alt text
    body = re.sub(r'<p>(<a href="[^"]*">)?<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/?>(</a>)?</p>',
                  lambda m: f'<figure>{m.group(1) or '<a href="' + m.group(2) + '">'}<img src="{m.group(2)}" alt="{m.group(3)}" '
                            f'{img_size(m.group(2))}loading="lazy">{m.group(4) or "</a>"}'
                            f'<figcaption>{m.group(3)}<span class="tap"> · Tap to enlarge.</span></figcaption></figure>', body)
    body = re.sub(r"<!--\s*atlas-hero\s*-->\s*<p><strong><a [^>]*>[^<]*</a></strong></p>", HERO, body)
    body = re.sub(r"<!--\s*interactive:\s*([a-z_]+)\s*-->",
                  lambda m: f'<iframe class="chart" style="height:{HEIGHTS.get(m.group(1), 680)}px" '
                            f'src="charts/{m.group(1)}.html" loading="lazy" title="interactive chart"></iframe>', body)
    return (html.unescape(re.sub(r"<[^>]+>", "", title.group(1))) if title else ""), body


def article(md_path, crumbs, dek, byline, current=""):
    title, body = md_to_html(md_path)
    return title, f"""{atlas_nav("", current)}<main id="main"><article class="post">
<header class="post-head"><div class="post-wrap">
<p class="post-crumbs">{crumbs}</p><h1>{title}</h1><p class="post-dek">{dek}</p>
<p class="post-byline"><span>{byline}</span></p></div></header>
<div class="post-body"><div class="post-wrap">{body}</div></div></article></main>"""


CRUMBS = '<a href="/blog/">Blog</a><span class="sep">/</span><a href="../">NeurIPS Atlas</a>'
words = len(re.sub(r"[#*\[\]()!<>-]", " ", (ROOT / "report/BLOG.md").read_text()).split())
title, body = article(ROOT / "report/BLOG.md", CRUMBS,
                      "Every NeurIPS 2026 paper on one map, and what changed since 2025.",
                      f"{round(words / 220)} min read · 20 October 2026", "index.html")
(DOCS / "index.html").write_text(page(title, "Every NeurIPS 2026 paper on one map, and what changed since 2025.",
                                      SITE, body))
print("wrote", DOCS / "index.html")

title, body = article(ROOT / "report/APPENDIX.md", CRUMBS + '<span class="sep">/</span><a href="index.html">2026</a>',
                      "Every NeurIPS 2026 area and topic with its numbers, and every oral.", "Data as of 20 October 2026",
                      "appendix.html")
body = label_cells(body.replace('<div class="post-wrap">', '<div class="post-wrap wide">'))
(DOCS / "appendix.html").write_text(page(title, "Every NeurIPS 2026 area and topic with its numbers, and every oral.",
                                         SITE + "appendix.html", body))
print("wrote", DOCS / "appendix.html")

(ROOT / "docs/.nojekyll").write_text("")
LANDING = f"""{atlas_nav("2026/")}<main id="main"><section class="hero"><div class="container">
<span class="kicker">Project</span><h1>NeurIPS Atlas</h1>
<p class="section-lede">What NeurIPS papers are about, and how that changes each year. Made from the public paper lists on neurips.cc.</p>
</div></section>
<section class="section"><div class="container">
<a href="2026/atlas.html"><img src="2026/figures/atlas_clusters.png" alt="Map of all NeurIPS 2026 papers"
 class="landing-map"></a>
<div class="landing-actions"><a class="btn" href="2026/atlas.html">Open the NeurIPS 2026 map</a>
<a class="btn btn-ghost" href="2026/papers.html">Search all papers</a></div>
<div class="prose" style="margin-top:28px">
<h2>Editions</h2>
<p><a href="2026/"><strong>NeurIPS 2026: the story.</strong></a> All 9,110 papers on one map, and what changed since 2025.</p>
<p><strong>NeurIPS through the years.</strong> Coming soon: how topics, submissions and countries changed since 2014.</p>
<h2>Also see</h2>
<p>The <a href="/emnlp/"><strong>EMNLP Atlas</strong></a>: all 5,534 EMNLP 2026 papers on one map, made the same way.</p>
</div></div></section></main>"""
(ROOT / "docs/index.html").write_text(page("NeurIPS Atlas", "Maps and numbers on what NeurIPS papers are about.",
                                           "https://mohammadi.cv/neurips/", LANDING, kind="website"))
print("wrote", ROOT / "docs/index.html")
