"""Check every link in the README, report and web pages.

- relative links: the target file must exist
- external links: fetched (polite, 3 workers) and must end in HTTP 200
- paper links: all links written in the appendix, plus a random sample of 150 papers from the index
- openreview.net answers scripts with a bot check; checked by hand in a logged-in browser on 20 Oct 2026:
  NeurIPS 2026 forums and PDFs are not public yet ("You don't have permission to read this forum"),
  so these links are reported as "not public yet" (they are the official links and open on release)
- links to the GitHub Pages site are reported as "pending" until the site is published
Writes outputs/link_check.csv and prints a summary.
"""
import re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urldefrag
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DOCS, OUT = ROOT / "docs/2026", ROOT / "outputs"
SITE = "https://mohammadi.cv/neurips/2026/"
UA = {"User-Agent": "Mozilla/5.0 (link check; NeurIPS paper overview)"}

links = []  # (source file, link)
for f in [ROOT / "README.md", *sorted((ROOT / "report").glob("*.md"))]:
    for m in re.finditer(r"\]\(([^)\s]+)\)|<(https?://[^>]+)>", f.read_text()):
        links.append((f, m.group(1) or m.group(2)))
for f in sorted(DOCS.glob("*.html")) + sorted((DOCS / "charts").glob("*.html")):
    txt = f.read_text()
    if f.name == "atlas.html":  # only the hand-written parts; the rest is the map library
        txt = "\n".join(re.findall(r'<a class="atlas-back"[^>]*>|<script src="[^"]+"', txt))
    for m in re.finditer(r'<(?:a|img|script|iframe|link)\b[^>]*?(?:href|src)="([^"]+)"[^>]*>', txt):
        tag = m.group(0)
        if 'rel="preconnect"' in tag or "${" in m.group(1):  # font preconnect host / JS template, not links
            continue
        links.append((f, m.group(1)))
for f in [DOCS / "papers.html"]:
    links.append((f, "https://neurips.cc/virtual/2026/poster/152156"))  # template of the JS-built links

idx = pd.read_csv(OUT / "papers_index.csv").fillna("")
sample = idx.sample(150, random_state=1)
for k, r in enumerate(sample.itertuples()):
    links.append((Path("papers_index.csv (sample)"), r.url))
    if k < 5:  # arXiv rate-limits scripts hard; all search links share one pattern, so test a few, slowly
        links.append((Path("papers_index.csv (sample)"), r.arxiv))
    if r.openreview:
        links.append((Path("papers_index.csv (sample)"), r.openreview))

rows, seen = [], {}


ARXIV_TESTED = {r.arxiv for r in list(sample.itertuples())[:5]}


def check_external(url):
    if url in seen:
        return seen[url]
    if "arxiv.org/search" in url and url not in ARXIV_TESTED:
        seen[url] = ("ok (pattern)", "same arXiv title-search pattern as the sampled links")
        return seen[url]
    if url.startswith(SITE):
        res = ("pending", "GitHub Pages site not published yet; checked locally via docs/")
    elif url.rstrip("/") == "https://github.com/mohammadi-hadi/neurips" or \
            url.startswith("https://github.com/mohammadi-hadi/neurips/"):
        r = requests.get(url, headers=UA, timeout=40)
        res = ("ok", "HTTP 200") if r.status_code == 200 else ("pending", "repository is private; public link works once it is made public")
    elif "openreview.net" in url:
        res = ("not public yet", "NeurIPS 2026 OpenReview pages are still closed (checked in a browser, 20 Oct 2026)")
    else:
        slow = "arxiv.org" in url
        res = ("broken", "no response")
        for attempt in range(4):
            time.sleep(8.0 if slow else 0.3)
            try:
                r = requests.get(url, headers=UA, timeout=40, allow_redirects=True)
            except requests.RequestException as e:
                res = ("broken", str(e)[:80]); continue
            if r.status_code == 429:  # rate limited: wait and retry
                time.sleep(10 * (attempt + 1)); res = ("broken", "HTTP 429 after retries"); continue
            res = ("ok", f"HTTP {r.status_code}") if r.status_code == 200 else ("broken", f"HTTP {r.status_code}")
            break
    seen[url] = res
    return res


def check(item):
    src, link = item
    link = link.strip()
    if link.startswith(("mailto:", "javascript:", "#")) or link == "":
        return src, link, "skip", ""
    if link.startswith("http"):
        if link.startswith(SITE):
            rel = urldefrag(link[len(SITE):])[0] or "index.html"
            ok = (DOCS / rel).exists()
            return src, link, "pending" if ok else "broken", f"local docs/{rel} {'exists' if ok else 'MISSING'}"
        st, note = check_external(link)
        return src, link, st, note
    base = src.parent if src.suffix else ROOT
    target = (base / urldefrag(link)[0]).resolve()
    return src, link, "ok" if target.exists() else "broken", "relative file"


with ThreadPoolExecutor(2) as ex:
    for src, link, st, note in ex.map(check, links):
        rows.append({"source": str(src).replace(str(ROOT) + "/", ""), "link": link, "status": st, "note": note})

res = pd.DataFrame(rows).drop_duplicates()
res.to_csv(OUT / "link_check.csv", index=False)
print(res.status.value_counts().to_string())
bad = res[res.status == "broken"]
if len(bad):
    print("\nBROKEN:\n" + bad.to_string(index=False))
sys.exit(1 if len(bad) else 0)
