"""Page template that matches mohammadi.cv: its fonts, its stylesheet (/assets/css/site.css),
its header and a footer without personal contact details."""

SITE_ROOT = "https://mohammadi.cv"
ATLAS_ROOT = "https://mohammadi.cv/neurips/"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;'
         '0,8..60,700;1,8..60,400;1,8..60,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500'
         '&display=swap" rel="stylesheet">'
         '<link rel="stylesheet" href="/assets/css/site.css">'
         '<link rel="icon" href="/assets/img/favicon.png"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">')

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
.atlas-nav a[aria-current]{color:var(--ink);text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1.5px}
.post-body .btn,.atlas-hero .btn{text-decoration:none}
.map-preview{padding-bottom:58px;box-sizing:border-box}
@media (max-width:720px){.map-preview{padding-bottom:0}.map-cover span{display:none}}
.landing-actions{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:16px}
.post-body figcaption .tap{display:none}
@media (max-width:640px){.post-body figcaption .tap{display:inline}}
.post-body .links{white-space:nowrap}
.post-body table + h3{margin-top:28px}
.landing-map{width:100%;height:min(70vh,680px);object-fit:contain;border:1px solid var(--rule);border-radius:10px;background:#fff;display:block}
@media (max-width:720px){.landing-map{height:auto}}
@media (max-width:640px){.post-wrap.wide table,.post-wrap.wide tbody,.post-wrap.wide tr,.post-wrap.wide td{display:block;width:auto;min-width:0}
.post-wrap.wide thead{display:none}.post-wrap.wide tr{padding:12px 0;border-bottom:1px solid var(--rule)}
.post-wrap.wide td{border:0;padding:2px 0}.post-wrap.wide td:first-child{font-weight:600}
.post-wrap.wide td[data-label]{display:inline-block;margin:4px 14px 0 0;font-family:var(--mono);font-size:.78rem;color:var(--ink-3)}
.post-wrap.wide td[data-label]::before{content:attr(data-label) ": "}}
/* desktop: the same column widths in every table, numbers on one line */
@media (min-width:641px){.post-wrap.wide table{table-layout:fixed}.post-wrap.wide th:nth-child(1){width:21%}.post-wrap.wide th:nth-child(3){width:4.5em}.post-wrap.wide th:nth-child(4){width:9.5em}.post-wrap.wide th:nth-child(5){width:3em}.post-wrap.wide td[data-label]{white-space:nowrap}}
"""

HEADER = """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container">
<a class="wordmark" href="/">Hadi Mohammadi</a>
<nav class="site-nav" aria-label="Main"><ul>
<li><a href="/research/">Research</a></li><li><a href="/publications/">Publications</a></li>
<li><a href="/software/">Software</a></li><li><a href="/experience/">Experience</a></li><li><a href="/teaching/">Teaching</a></li>
<li><a href="/blog/" aria-current="page">Blog</a></li><li><a href="/thesis/">Thesis</a></li><li><a href="/assets/docs/HadiMohammadiCV.pdf">CV</a></li></ul></nav>
<details class="nav-toggle"><summary>Menu</summary><nav class="site-nav" aria-label="Mobile"><ul>
<li><a href="/research/">Research</a></li><li><a href="/publications/">Publications</a></li>
<li><a href="/software/">Software</a></li><li><a href="/experience/">Experience</a></li><li><a href="/teaching/">Teaching</a></li>
<li><a href="/blog/" aria-current="page">Blog</a></li><li><a href="/thesis/">Thesis</a></li><li><a href="/assets/docs/HadiMohammadiCV.pdf">CV</a></li></ul></nav></details>
</div></header>"""


def atlas_nav(prefix="", current=""):
    """Project menu shown under the site header. prefix='' inside /neurips/2026/, '2026/' on the landing page."""
    nav = (f'<nav class="atlas-nav" aria-label="NeurIPS Atlas"><div class="container">'
            f'<a class="name" href="{"../" if not prefix else ""}">NeurIPS Atlas</a>'
            f'<a class="map" href="{prefix}atlas.html">Open the map</a>'
            f'<a href="{prefix}index.html">2026 story</a><a href="{prefix}papers.html">All papers</a>'
            f'<a href="{prefix}charts/treemap.html">All topics</a><a href="{prefix}appendix.html">Appendix</a>'
            f'<a href="https://github.com/mohammadi-hadi/neurips">Code and data</a>'
            f'<a href="/emnlp/2026/">EMNLP 2026</a><a href="/ai-conferences/2026/">NeurIPS vs EMNLP</a></div></nav>')
    # the page you are on is marked, like the Blog item in the site menu
    return nav.replace(f'href="{prefix}{current}">', f'href="{prefix}{current}" aria-current="page">', 1) if current else nav


FOOTER = """<footer class="site-footer"><div class="container">
<p>&copy; 2026 Hadi Mohammadi &middot; Data: public paper lists from neurips.cc</p>
<p><a href="/">mohammadi.cv</a> <span class="nobreak">&middot; <a href="https://github.com/mohammadi-hadi/neurips">Code and data on GitHub</a></span></p>
</div></footer>"""


def page(title, description, url, body, image=None, extra_head="", kind="article"):
    img = image or f"{ATLAS_ROOT}2026/figures/atlas_static.png"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="color-scheme" content="light">
<title>{title} — Hadi Mohammadi</title><meta name="description" content="{description}">
<link rel="canonical" href="{url}"><meta name="author" content="Hadi Mohammadi">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:url" content="{url}"><meta property="og:type" content="{kind}"><meta property="og:site_name" content="Hadi Mohammadi">
<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
{FONTS}<style>{EXTRA_CSS}</style>{extra_head}</head><body>
{HEADER}
{body}
{FOOTER}
</body></html>"""


TREEMAP_CSS = """<style>
#tm{height:min(80vh,820px)!important;min-height:520px;margin:4px 0 40px}
.scale{display:flex;align-items:center;flex-wrap:wrap;gap:8px;font-size:var(--step--1);color:var(--ink-3);margin:14px 0 4px}
.scale i{display:block;width:140px;height:10px;border-radius:5px;background:linear-gradient(90deg,#2166ac,#f7f7f7,#b2182b)}
.areas{list-style:none;padding:0;margin:8px 0 0;columns:2 340px;column-gap:28px}
.areas li{break-inside:avoid;border-bottom:1px solid var(--rule)}
.areas button{all:unset;box-sizing:border-box;cursor:pointer;display:flex;gap:10px;align-items:baseline;width:100%;padding:8px 2px}
.areas button:hover .n,.areas button:focus-visible .n{color:var(--accent);text-decoration:underline}
.areas .d{flex:none;width:11px;height:11px;border-radius:3px;border:1px solid rgba(0,0,0,.28);transform:translateY(1px)}
.areas .n{flex:1}.areas .v{font-family:var(--mono);font-size:.76rem;color:var(--ink-3);white-space:nowrap}
</style>"""


def _mix(g):
    """The chart's colour for a growth value, so the list below matches the boxes."""
    stops = [(-1.5, (33, 102, 172)), (0, (247, 247, 247)), (1.5, (178, 24, 43))]
    g = max(-1.5, min(1.5, g)); (a, ca), (b, cb) = (stops[0], stops[1]) if g <= 0 else (stops[1], stops[2])
    f = (g - a) / (b - a)
    return "#%02x%02x%02x" % tuple(round(x + f * (y - x)) for x, y in zip(ca, cb))


def area_list(t, prev, cur):
    """Areas as a plain list, largest growth first. A click opens the area in the chart."""
    import html, numpy as np
    a = t.groupby("area").agg(papers=("papers", "sum"), sc=("share_cur", "sum"), sp=("share_prev", "sum"))
    a["g"] = np.log2((a.sc + 0.05) / (a.sp + 0.05))  # colour, as in the chart
    a["pts"] = a.sc - a.sp  # order: change in share, in percentage points
    items = "".join(f'<li><button type="button" data-a="{html.escape(n)}"><span class="d" style="background:{_mix(r.g)}"></span>'
                    f'<span class="n">{html.escape(n)}</span><span class="v">{int(r.papers):,} · {r.sp:.1f}% → {r.sc:.1f}%</span></button></li>'
                    for n, r in a.sort_values("pts", ascending=False).iterrows())
    return (f'<h2>All areas</h2><p>From the area whose share of the papers grew most to the one whose share fell most: '
            f'papers in {cur}, then the share of all papers in {prev} and {cur}. Select a name to open it in the chart.</p><ol class="areas">{items}</ol>'
            "<script>document.querySelectorAll('.areas button').forEach(b => b.addEventListener('click', () => {"
            "Plotly.restyle('tm', {level: 'a/' + b.dataset.a}); document.getElementById('tm').scrollIntoView({behavior: 'smooth', block: 'center'});"
            "}));</script>")


def treemap_page(fig, conf, lede, url, below=""):
    """charts/treemap.html as a page of the site: header, project menu, a short explanation, then the chart.
    The chart opens on the areas, where the names are readable; a click on an area shows its topics."""
    div = fig.to_html(full_html=False, include_plotlyjs="cdn", div_id="tm",
                      config={"displaylogo": False, "responsive": True, "displayModeBar": False})
    nav = atlas_nav("../", "charts/treemap.html").replace('class="name" href=""', 'class="name" href="../../"')
    body = f"""{nav}<main id="main"><article class="post"><header class="post-head"><div class="post-wrap wide">
<p class="post-crumbs"><a href="/blog/">Blog</a><span class="sep">/</span><a href="../../">{conf} Atlas</a><span class="sep">/</span><a href="../index.html">2026</a></p>
<h1>All {conf} 2026 topics</h1>
<p>{lede}</p>
<p class="scale"><span>shrank</span><i></i><span>grew</span></p>
{div}
{below}
</div></header></article></main>"""
    return page(f"All {conf} 2026 topics", f"Every {conf} 2026 topic, sized by papers and coloured by its change since last year.",
                url, body, extra_head=TREEMAP_CSS)


def treemap_figure(t, root, cur, prev, area_info):
    """Treemap root -> area -> topic. t has one row per topic with area, label, papers, share_cur, share_prev
    and info (extra hover lines); area_info gives extra hover lines per area. Built by hand so the area boxes
    get real numbers on hover too (plotly express shows "(?)" for parents)."""
    import textwrap
    import numpy as np
    import plotly.graph_objects as go
    growth = lambda sc, sp: float(np.log2((sc + 0.05) / (sp + 0.05)))
    tip = lambda name, n, sc, sp, extra: (f"<b>{name}</b><br>{int(n):,} papers in {cur}<br>share of all papers: "
                                          f"{sp:.2f}% in {prev}, {sc:.2f}% in {cur}" + (f"<br>{extra}" if extra else ""))
    a = t.groupby("area").agg(papers=("papers", "sum"), share_cur=("share_cur", "sum"),
                              share_prev=("share_prev", "sum"), topics=("label", "size"))
    total = int(t.papers.sum())
    ids, labels, parents, values = ["root"], [root], [""], [total]
    colors, tips = [0.0], [f"<b>{root}</b><br>{total:,} papers. Click an area to see its topics."]
    for name, r in a.iterrows():
        ids.append(f"a/{name}"); labels.append(name); parents.append("root"); values.append(int(r.papers))
        colors.append(growth(r.share_cur, r.share_prev))
        tips.append(tip(name, r.papers, r.share_cur, r.share_prev, f"{int(r.topics)} topics" + (f"<br>{area_info[name]}" if area_info.get(name) else "")))
    for i, r in t.reset_index(drop=True).iterrows():
        ids.append(f"t/{i}"); labels.append(r.label); parents.append(f"a/{r.area}"); values.append(int(r.papers))
        colors.append(growth(r.share_cur, r.share_prev)); tips.append(tip(r.label, r.papers, r.share_cur, r.share_prev, r.info))
    return go.Figure(go.Treemap(
        ids=ids, labels=labels, parents=parents, values=values, branchvalues="total", maxdepth=2, sort=True,
        marker=dict(colors=colors, colorscale=[[0, "#2166ac"], [0.5, "#f7f7f7"], [1, "#b2182b"]], cmin=-1.5, cmax=1.5,
                    line=dict(color="white", width=1)),
        customdata=[[s] for s in tips], hovertemplate="%{customdata[0]}<extra></extra>",
        # long names on two or three lines, so Plotly does not shrink them to fit one
        text=[textwrap.fill(x, 22).replace("\n", "<br>") for x in labels], texttemplate="%{text}<br>%{value}", textfont_size=13, root_color="white", pathbar=dict(thickness=24)))
