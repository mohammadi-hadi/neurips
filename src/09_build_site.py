"""Build the GitHub Pages site in docs/: blog (index.html), appendix, figures.
Needs pandoc on PATH."""
import re, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://mohammadi-hadi.github.io/NeurIPS2026_Analysis/"
(DOCS / "figures").mkdir(parents=True, exist_ok=True)
for f in (ROOT / "outputs/figures").glob("*.png"):
    shutil.copy(f, DOCS / "figures" / f.name)

CSS = """
:root{--ink:#1f2a44;--muted:#5c677d;--accent:#d9480f;--bg:#ffffff;--card:#f6f7f9;--line:#e3e6ea}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#e8ebf1;--muted:#a3acbd;--accent:#ff8a4c;--bg:#12151c;--card:#1b2029;--line:#2a313d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 Inter,system-ui,-apple-system,Segoe UI,sans-serif}
nav{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);z-index:5}
nav div{max-width:780px;margin:0 auto;padding:10px 16px;display:flex;gap:18px;flex-wrap:wrap;font-size:15px}
nav a{color:var(--muted);text-decoration:none}nav a:hover{color:var(--accent)}
main{max-width:780px;margin:0 auto;padding:24px 16px 80px}
h1{font-size:2.1rem;line-height:1.2;margin:.6em 0 .3em}h2{margin-top:2.2em;font-size:1.45rem}h3{font-size:1.15rem}
a{color:var(--accent)}img{max-width:100%;height:auto;border-radius:8px;background:#fff}
figure{margin:1.6em 0}figcaption{color:var(--muted);font-size:14px;margin-top:6px}
iframe.chart{width:100%;height:640px;border:1px solid var(--line);border-radius:10px;background:#fff;margin:.4em 0 1.6em}
table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
blockquote{margin:1em 0;padding:.6em 1em;background:var(--card);border-left:3px solid var(--accent);border-radius:4px}
code{background:var(--card);padding:1px 5px;border-radius:4px;font-size:.9em}
.cta{display:inline-block;background:var(--accent);color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600}
footer{color:var(--muted);font-size:14px;border-top:1px solid var(--line);margin-top:3em;padding-top:1em}
"""

NAV = ('<nav><div><a href="index.html"><b>NeurIPS 2026 Atlas</b></a><a href="atlas.html">Interactive map</a>'
       '<a href="papers.html">All papers</a><a href="charts/treemap.html">All subtopics</a><a href="appendix.html">Appendix</a>'
       '<a href="https://github.com/mohammadi-hadi/NeurIPS2026_Analysis">Code &amp; data</a></div></nav>')


HEIGHTS = {"treemap": 800, "vocabulary": 740}


def page(md_path, out_name, title, description):
    body = subprocess.run(["pandoc", str(md_path), "-f", "gfm", "-t", "html5"], capture_output=True,
                          text=True, check=True).stdout
    body = body.replace("../outputs/figures/", "figures/").replace("../docs/", "")
    body = re.sub(r'href="(?:\.\./)?docs/', 'href="', body)
    body = body.replace(SITE, "")  # keep links relative inside the site
    body = re.sub(r"<!--\s*interactive:\s*([a-z_]+)\s*-->",
                  lambda m: f'<iframe class="chart" style="height:{HEIGHTS.get(m.group(1), 680)}px" src="charts/{m.group(1)}.html" loading="lazy" '
                            f'title="interactive chart: {m.group(1)}"></iframe>', body)
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{description}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE}figures/atlas_static.png"><meta property="og:url" content="{SITE}{out_name}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{NAV}<main>{body}
<footer>Data: public NeurIPS 2025 and 2026 paper lists from neurips.cc, pulled 20 October 2026.
Code and method: <a href="https://github.com/mohammadi-hadi/NeurIPS2026_Analysis">github.com/mohammadi-hadi/NeurIPS2026_Analysis</a>.</footer>
</main></body></html>"""
    (DOCS / out_name).write_text(html)
    print("wrote", DOCS / out_name)


page(ROOT / "report/BLOG.md", "index.html", "The NeurIPS 2026 Atlas",
     "What 9,110 accepted NeurIPS 2026 papers say about where machine learning is going: topics, growth since 2025, orals, three cities and who wrote them.")
page(ROOT / "report/APPENDIX.md", "appendix.html", "NeurIPS 2026 Atlas: all areas and subtopics",
     "Every research area and subtopic of NeurIPS 2026 with paper counts, shares and orals.")
(DOCS / ".nojekyll").write_text("")
