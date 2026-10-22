"""docs/papers.html: a searchable list of every NeurIPS 2026 paper with its links
(NeurIPS page, OpenReview, PDF), area, subtopic, status, city and local poster time.
Also writes outputs/papers_index.csv."""
import json
from pathlib import Path
import pandas as pd
from common import load_papers, OPENREVIEW_NOTE
from site_template import page as site_page, atlas_nav

ROOT = Path(__file__).resolve().parents[1]
OUT, DOCS = ROOT / "outputs", ROOT / "docs/2026"
L = json.load(open(ROOT / "data/labels/labels.json"))
fine_name = {int(k): v["name"] for k, v in L["fine"].items()}
broad_name = {int(k): v["name"] for k, v in L["broad"].items()}


def short_authors(a, n=180):
    """Cuts a long author list at a name, not in the middle of one."""
    names = [x.strip() for x in str(a).replace(";", ",").split(",") if x.strip()]
    out = []
    for x in names:
        if len(", ".join(out + [x])) > n: return ", ".join(out) + f" and {len(names) - len(out)} more"
        out.append(x)
    return ", ".join(out)

d = load_papers()
d = d[d.year == 2026].copy()
tz = {"Sydney": "Australia/Sydney", "Atlanta": "America/New_York", "Paris": "Europe/Paris"}
start = pd.to_datetime(d["start"], errors="coerce", utc=True)
d["when"] = [s.tz_convert(tz[c]).strftime("%a %-d %b %H:%M") if (c in tz and not pd.isna(s)) else ""
             for s, c in zip(start, d["site"])]
d["area"] = d["broad"].map(broad_name)
d["subtopic"] = d["fine"].map(fine_name)
d["status"] = d["decision"].map({"oral": "Oral", "spotlight": "Spotlight", "poster": "Poster"}).fillna("Decision not yet public")
d["city"] = d["site"].where(d["site"].isin(list(tz)), "")
cols = ["title_display", "authors", "area", "subtopic", "status", "city", "when", "url", "arxiv", "openreview", "pdf", "or_link"]
idx = d[cols].rename(columns={"title_display": "title"}).fillna("")
idx = idx.iloc[idx["title"].str.replace(r"^[^0-9A-Za-z]+", "", regex=True).str.lower().argsort(kind="stable")]  # "(How)..." sorts under H
csv = idx.drop(columns=["openreview", "pdf"]).rename(columns={"or_link": "openreview"})
csv["pdf"] = csv["openreview"].str.replace("/forum?id=", "/pdf?id=", regex=False)
csv.to_csv(OUT / "papers_index.csv", index=False)  # OpenReview columns stay empty until the papers are public

GONE = set(json.load(open(ROOT / "data/labels/gone_from_program.json")))  # papers whose NeurIPS page is gone
rows = [[r.title, short_authors(r.authors), r.area, r.subtopic, r.status, r.city, r.when,
         "" if r.url.rsplit("/", 1)[-1] in GONE else r.url.rsplit("/", 1)[-1],
         r.or_link.rsplit("=", 1)[-1] if r.or_link else ""] for r in idx.itertuples()]
areas = sorted(idx["area"].unique())

CSS = """<style>
.controls{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}
.controls input,.controls select{font:inherit;font-size:var(--step--1);padding:8px 10px;border:1px solid var(--rule);border-radius:8px;background:var(--surface);color:var(--ink)}
.controls input{flex:1;min-width:220px}
@media (max-width:560px){.controls input,.controls select{flex:1 1 100%;min-width:0}}
.when{white-space:nowrap}
.p{border-bottom:1px solid var(--rule);padding:12px 0}.p .t{font-weight:600;line-height:1.4}
.p .m,.meta{color:var(--ink-3);font-size:var(--step--1)}.p .a{font-size:var(--step--1);margin-top:4px}
.p .a a{margin-right:14px;font-weight:500}
.tag{display:inline-block;font-family:var(--mono);font-size:.7rem;padding:1px 7px;border-radius:10px;background:var(--paper-deep);margin-right:6px}
.tag.o{background:var(--accent);color:#fff}.tag.s{background:var(--accent-hover);color:#fff}
#more{margin-top:16px}
</style>"""
BODY = """__NAV__<main id="main"><article class="post"><header class="post-head"><div class="post-wrap wide">
<p class="post-crumbs"><a href="../">NeurIPS Atlas</a><span class="sep">/</span><a href="index.html">2026</a></p>
<h1>All __N__ NeurIPS 2026 papers</h1>
<p>Search by title or author, or filter by area, city and status. Each paper links to its NeurIPS page and an arXiv search. Times are local.</p>
<p class="meta">__NOTE__</p>
<div class="controls"><input id="q" type="search" placeholder="Search title or author…" aria-label="search">
<select id="area" aria-label="area"><option value="">All areas</option>__AREAS__</select>
<select id="city" aria-label="city"><option value="">All cities</option><option>Sydney</option><option>Atlanta</option><option>Paris</option></select>
<select id="status" aria-label="status"><option value="">Any status</option><option>Oral</option><option>Spotlight</option><option>Poster</option><option>Decision not yet public</option></select></div>
<div id="count" class="meta"></div><div id="list"></div><button id="more" class="btn">Show more</button>
</div></header></article></main>
<script>
const D = __DATA__;
const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let shown = 0, hits = [];
function filter() {
  const q = document.getElementById('q').value.toLowerCase(), a = document.getElementById('area').value,
        c = document.getElementById('city').value, s = document.getElementById('status').value;
  hits = D.filter(r => (!q || (r[0] + ' ' + r[1]).toLowerCase().includes(q)) && (!a || r[2] === a) && (!c || r[5] === c) && (!s || r[4] === s));
  shown = 0; document.getElementById('list').innerHTML = ''; more();
}
function more() {
  const html = hits.slice(shown, shown + 100).map(r => {
    const tag = r[4] === 'Oral' ? '<span class="tag o">Oral</span>' : r[4] === 'Spotlight' ? '<span class="tag s">Spotlight</span>' : '';
    const where = r[5] ? `${r[5]}${r[6] ? ' · ' + r[6] : ''}` : 'time not published';
    const ax = 'https://arxiv.org/search/?query=' + encodeURIComponent(r[0].replace(/[^\\w\\s-]/g, ' ')).replace(/%20/g, '+') + '&searchtype=title';
    const links = (r[7] ? `<a href="https://neurips.cc/virtual/2026/poster/${r[7]}" target="_blank" rel="noopener">NeurIPS page</a>` : '') +
      `<a href="${ax}" target="_blank" rel="noopener">Find on arXiv</a>` +
      (r[8] ? `<a href="https://openreview.net/forum?id=${r[8]}" target="_blank" rel="noopener">OpenReview</a><a href="https://openreview.net/pdf?id=${r[8]}" target="_blank" rel="noopener">PDF</a>` : '');
    return `<div class="p"><div class="t">${tag}${esc(r[0])}</div><div class="m">${esc(r[1])}</div>` +
      `<div class="a"><span class="tag">${esc(r[2])}</span><span class="tag">${esc(r[3])}</span><span class="when">${esc(where)}</span></div><div class="a">${links}</div></div>`;
  }).join('');
  document.getElementById('list').insertAdjacentHTML('beforeend', html);
  shown += 100;
  document.getElementById('count').textContent = `${hits.length.toLocaleString()} papers`;
  document.getElementById('more').style.display = shown < hits.length ? 'inline-block' : 'none';
}
['q', 'area', 'city', 'status'].forEach(id => document.getElementById(id).addEventListener('input', filter));
document.getElementById('more').addEventListener('click', more);
const params = new URLSearchParams(location.search); if (params.get('q')) document.getElementById('q').value = params.get('q');
filter();
</script>"""
body = (BODY.replace("__NAV__", atlas_nav()).replace("__N__", f"{len(rows):,}").replace("__NOTE__", OPENREVIEW_NOTE)
        .replace("__AREAS__", "".join(f"<option>{a}</option>" for a in areas))
        .replace("__DATA__", json.dumps(rows, ensure_ascii=False, separators=(",", ":"))))
(DOCS / "papers.html").write_text(site_page(
    "All NeurIPS 2026 papers", "Search all 9,110 NeurIPS 2026 papers and find their links.",
    "https://mohammadi.cv/neurips/2026/papers.html", body, extra_head=CSS))
print("wrote docs/papers.html,", len(rows), "papers,", sum(1 for r in rows if r[8]), "with OpenReview links")
