"""Page template that matches mohammadi.cv: its fonts, its stylesheet (/assets/css/site.css),
its header and a footer without personal contact details."""

SITE_ROOT = "https://mohammadi.cv"
ATLAS_ROOT = "https://mohammadi.cv/neurips/"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;'
         '0,8..60,700;1,8..60,400;1,8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500'
         '&display=swap" rel="stylesheet">'
         '<link rel="stylesheet" href="/assets/css/site.css">')

# small additions for this project, written with the site's own tokens
EXTRA_CSS = """
html,body{overflow-x:hidden}
.atlas-nav{border-bottom:1px solid var(--rule);background:var(--surface)}
.atlas-nav .container{display:flex;gap:6px 18px;flex-wrap:wrap;align-items:center;padding-top:10px;padding-bottom:10px;
  font-family:var(--mono);font-size:.78rem;letter-spacing:.02em}
.atlas-nav a{color:var(--ink-2);text-decoration:none}.atlas-nav a:hover{color:var(--accent)}
.atlas-nav .name{font-weight:500;color:var(--ink)}
.atlas-nav a.map{background:var(--accent);color:#fff;padding:4px 10px;border-radius:6px}
.atlas-nav a.map:hover{background:var(--accent-hover);color:#fff}
.atlas-hero{margin:8px auto 36px}
.atlas-hero iframe{width:100%;height:min(78vh,760px);border:1px solid var(--rule);border-radius:10px;background:#fff;display:block;
  box-shadow:0 2px 18px rgba(30,58,95,.08)}
.map-frame{position:relative}
.map-preview{width:100%;height:min(78vh,760px);object-fit:contain;background:#fff;border:1px solid var(--rule);border-radius:10px;display:block}
@media (max-width:720px){.map-preview{height:auto}}
.map-cover{position:absolute;inset:0;border:0;background:transparent;cursor:pointer;display:flex;align-items:flex-end;justify-content:center;padding-bottom:18px}
.map-cover span{font-family:var(--sans);font-size:.9rem;font-weight:500;background:var(--accent);color:#fff;padding:8px 14px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.15)}
.map-cover:hover span{background:var(--accent-hover)}
.atlas-hero .actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:14px}
.post-body figure{margin:32px 0 32px 50%;width:min(1000px,calc(100vw - 32px));transform:translateX(-50%)}
.post-body figure img{display:block;width:auto;max-width:100%;height:auto;max-height:min(85vh,860px);margin:0 auto;border:1px solid var(--rule);border-radius:8px;background:#fff}
.post-body figcaption{text-align:center}
.post-body iframe.chart{width:min(1000px,calc(100vw - 32px))!important;margin-left:50%!important;transform:translateX(-50%)}
.post-body figcaption{font-size:var(--step--1);color:var(--ink-3);margin-top:6px}
.post-body iframe.chart{width:100%;border:1px solid var(--rule);border-radius:8px;background:#fff;margin:0 0 28px}
.post-body table{width:100%;border-collapse:collapse;font-size:var(--step--1)}
.post-body th,.post-body td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;vertical-align:top}
.post-body .note{font-size:var(--step--1);color:var(--ink-3)}
.wide{max-width:1080px}
"""

HEADER = """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container">
<a class="wordmark" href="/">Hadi Mohammadi</a>
<nav class="site-nav" aria-label="Main"><ul>
<li><a href="/research/">Research</a></li><li><a href="/publications/">Publications</a></li>
<li><a href="/software/">Software</a></li><li><a href="/blog/">Blog</a></li>
<li><a href="/neurips/">NeurIPS Atlas</a></li><li><a href="/emnlp/">EMNLP Atlas</a></li><li><a href="/assets/docs/HadiMohammadiCV.pdf">CV</a></li></ul></nav>
<details class="nav-toggle"><summary>Menu</summary><nav class="site-nav" aria-label="Mobile"><ul>
<li><a href="/research/">Research</a></li><li><a href="/publications/">Publications</a></li>
<li><a href="/software/">Software</a></li><li><a href="/blog/">Blog</a></li>
<li><a href="/neurips/">NeurIPS Atlas</a></li><li><a href="/emnlp/">EMNLP Atlas</a></li><li><a href="/assets/docs/HadiMohammadiCV.pdf">CV</a></li></ul></nav></details>
</div></header>"""


def atlas_nav(prefix=""):
    """Project menu shown under the site header. prefix='' inside /neurips/2026/, '2026/' on the landing page."""
    return (f'<nav class="atlas-nav" aria-label="NeurIPS Atlas"><div class="container">'
            f'<a class="name" href="{"../" if not prefix else ""}">NeurIPS Atlas</a>'
            f'<a class="map" href="{prefix}atlas.html">Open the map</a>'
            f'<a href="{prefix}index.html">2026 story</a><a href="{prefix}papers.html">All papers</a>'
            f'<a href="{prefix}charts/treemap.html">All topics</a><a href="{prefix}appendix.html">Appendix</a>'
            f'<a href="https://github.com/mohammadi-hadi/neurips">Code &amp; data</a>'
            f'<a href="/emnlp/2026/">EMNLP 2026 map</a></div></nav>')


FOOTER = """<footer class="site-footer"><div class="container">
<p>&copy; 2026 Hadi Mohammadi &middot; Data: public paper lists from neurips.cc</p>
<p><a href="/">mohammadi.cv</a> <span class="nobreak">&middot; <a href="https://github.com/mohammadi-hadi/neurips">Code and data on GitHub</a></span></p>
</div></footer>"""


def page(title, description, url, body, image=None, extra_head=""):
    img = image or f"{ATLAS_ROOT}2026/figures/atlas_static.png"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="color-scheme" content="light">
<title>{title} — Hadi Mohammadi</title><meta name="description" content="{description}">
<link rel="canonical" href="{url}"><meta name="author" content="Hadi Mohammadi">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:url" content="{url}"><meta property="og:type" content="article"><meta property="og:site_name" content="Hadi Mohammadi">
<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
{FONTS}<style>{EXTRA_CSS}</style>{extra_head}</head><body>
{HEADER}
{body}
{FOOTER}
</body></html>"""
