"""docs/papers.html: a searchable list of every NeurIPS 2026 paper with its links
(NeurIPS page, OpenReview, PDF), area, subtopic, status, city and local poster time.
Also writes outputs/papers_index.csv."""
import json
from pathlib import Path
import pandas as pd
from common import load_papers, OPENREVIEW_NOTE

ROOT = Path(__file__).resolve().parents[1]
OUT, DOCS = ROOT / "outputs", ROOT / "docs/2026"
L = json.load(open(ROOT / "data/labels/labels.json"))
fine_name = {int(k): v["name"] for k, v in L["fine"].items()}
broad_name = {int(k): v["name"] for k, v in L["broad"].items()}

d = load_papers()
d = d[d.year == 2026].copy()
tz = {"Sydney": "Australia/Sydney", "Atlanta": "America/New_York", "Paris": "Europe/Paris"}
start = pd.to_datetime(d["start"], errors="coerce", utc=True)
d["when"] = [s.tz_convert(tz[c]).strftime("%a %d %b %H:%M") if (c in tz and not pd.isna(s)) else ""
             for s, c in zip(start, d["site"])]
d["area"] = d["broad"].map(broad_name)
d["subtopic"] = d["fine"].map(fine_name)
d["status"] = d["decision"].map({"oral": "Oral", "spotlight": "Spotlight", "poster": "Poster"}).fillna("Decision not yet public")
d["city"] = d["site"].where(d["site"].isin(list(tz)), "")
cols = ["title_display", "authors", "area", "subtopic", "status", "city", "when", "url", "arxiv", "openreview", "pdf"]
idx = d[cols].rename(columns={"title_display": "title"}).sort_values("title").fillna("")
idx.to_csv(OUT / "papers_index.csv", index=False)

rows = [[r.title, r.authors[:180], r.area, r.subtopic, r.status, r.city, r.when, r.url.rsplit("/", 1)[-1],
         r.openreview.rsplit("=", 1)[-1] if r.openreview else ""] for r in idx.itertuples()]
areas = sorted(idx["area"].unique())

page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NeurIPS 2026 paper index</title>
<meta name="description" content="Search all 9,110 NeurIPS 2026 papers with links to the NeurIPS page, OpenReview and the PDF.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#1f2a44;--muted:#5c677d;--accent:#d9480f;--bg:#ffffff;--card:#f6f7f9;--line:#e3e6ea}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#e8ebf1;--muted:#a3acbd;--accent:#ff8a4c;--bg:#12151c;--card:#1b2029;--line:#2a313d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}
nav{border-bottom:1px solid var(--line)}nav div{max-width:1100px;margin:0 auto;padding:10px 16px;display:flex;gap:18px;flex-wrap:wrap;font-size:15px}
nav a{color:var(--muted);text-decoration:none}nav a:hover{color:var(--accent)}
main{max-width:1100px;margin:0 auto;padding:20px 16px 60px}h1{font-size:1.8rem;margin:.3em 0}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
input,select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
input{flex:1;min-width:220px}
.p{border-bottom:1px solid var(--line);padding:10px 0}.p .t{font-weight:600}
.p .m{color:var(--muted);font-size:13px}.p .a{font-size:13px;margin-top:3px}
.p a{color:var(--accent);margin-right:12px;text-decoration:none;font-weight:600}.p a:hover{text-decoration:underline}
.tag{display:inline-block;font-size:12px;padding:1px 7px;border-radius:10px;background:var(--card);margin-right:6px}
.tag.o{background:#c92a2a;color:#fff}.tag.s{background:#f08c00;color:#fff}
#more{margin-top:14px;padding:8px 14px;border:0;border-radius:8px;background:var(--accent);color:#fff;font:inherit;cursor:pointer}
</style></head><body>
<nav><div><a href="../"><b>NeurIPS Atlas</b></a><a href="index.html">2026</a><a href="atlas.html">Interactive map</a>
<a href="papers.html">All papers</a><a href="charts/treemap.html">All subtopics</a><a href="appendix.html">Appendix</a>
<a href="https://github.com/mohammadi-hadi/neurips">Code &amp; data</a></div></nav>
<main><h1>All NeurIPS 2026 papers</h1>
<p>__N__ papers with links to the NeurIPS page, an arXiv search, OpenReview and the PDF. Search titles and authors, or filter by area, city and status.
Poster times are local to the city.</p><p class="m">* __NOTE__</p>
<div class="controls"><input id="q" type="search" placeholder="Search title or author…" aria-label="search">
<select id="area" aria-label="area"><option value="">All areas</option>__AREAS__</select>
<select id="city" aria-label="city"><option value="">All cities</option><option>Sydney</option><option>Atlanta</option><option>Paris</option></select>
<select id="status" aria-label="status"><option value="">Any status</option><option>Oral</option><option>Spotlight</option><option>Poster</option><option>Decision not yet public</option></select></div>
<div id="count" class="m"></div><div id="list"></div><button id="more">Show more</button></main>
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
    const links = `<a href="https://neurips.cc/virtual/2026/poster/${r[7]}" target="_blank" rel="noopener">NeurIPS page</a>` +
      `<a href="${ax}" target="_blank" rel="noopener">Find on arXiv</a>` +
      (r[8] ? `<a href="https://openreview.net/forum?id=${r[8]}" target="_blank" rel="noopener">OpenReview*</a><a href="https://openreview.net/pdf?id=${r[8]}" target="_blank" rel="noopener">PDF*</a>` : '');
    return `<div class="p"><div class="t">${tag}${esc(r[0])}</div><div class="m">${esc(r[1])}</div>` +
      `<div class="a"><span class="tag">${esc(r[2])}</span><span class="tag">${esc(r[3])}</span>${esc(where)}</div><div class="a">${links}</div></div>`;
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
</script></body></html>"""
page = (page.replace("__N__", f"{len(rows):,}").replace("__NOTE__", OPENREVIEW_NOTE)
        .replace("__AREAS__", "".join(f"<option>{a}</option>" for a in areas))
        .replace("__DATA__", json.dumps(rows, ensure_ascii=False, separators=(",", ":"))))
(DOCS / "papers.html").write_text(page)
print("wrote docs/papers.html,", len(rows), "papers,", sum(1 for r in rows if r[8]), "with OpenReview links")
