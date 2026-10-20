"""Fill in city, time, room and OpenReview link for 2026 papers that are missing from the bulk
schedule file, by reading each paper's public page on neurips.cc (polite: 3 workers, small delay).

Writes data/raw/neurips2026_schedule_fill.json  {virtualsite id: {site, start_utc, end_utc, room, openreview}}.
Re-running only fetches ids that are not in the file yet.
"""
import csv, html, json, re, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

RAW = Path(__file__).resolve().parents[1] / "data/raw"
OUT = RAW / "neurips2026_schedule_fill.json"
UA = {"User-Agent": "Mozilla/5.0 (research script; NeurIPS paper overview; about 1 request/s)"}
AEDT = timezone(timedelta(hours=11))  # the virtual site prints poster times in Sydney summer time

rows = list(csv.DictReader(open(RAW / "neurips2026_papers_abstracts.csv", encoding="utf-8")))
sched = json.load(open(RAW / "neurips2026_orals_posters_meta.json"))["results"]
have_or = {x["virtualsite_url"].rstrip("/").split("/")[-1] for x in sched
           if x.get("eventtype") == "Poster" and str(x.get("paper_url", "")).startswith("https://openreview.net")}
todo = sorted({r["virtualsite_url"].rstrip("/").split("/")[-1] for r in rows} - have_or)
done = json.load(open(OUT)) if OUT.exists() else {}
todo = [v for v in todo if v not in done or ("start_utc" not in done[v] and "error" not in done[v])]
print(f"{len(todo)} pages to fetch")

TIME = re.compile(r"(\w{3}, \w{3} \d{1,2}, \d{4}) • (\d{1,2}:\d{2} [AP]M) – (\d{1,2}:\d{2} [AP]M) AEDT")


def fetch(vid):
    time.sleep(0.5)
    try:
        r = requests.get(f"https://neurips.cc/virtual/2026/poster/{vid}", headers=UA, timeout=40)
    except requests.RequestException as e:
        return vid, {"error": str(e)[:100]}
    if r.status_code != 200:
        return vid, {"error": f"HTTP {r.status_code}"}
    site = re.search(r"/virtual/2026/loc/(\w+)/", r.url)
    orv = re.search(r"https://openreview\.net/forum\?id=([A-Za-z0-9_-]+)", r.text)
    txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))).replace("\xa0", " ")
    t = TIME.search(txt)
    room = re.search(r"AEDT (Paris Poster Hall|Hall \S+)", txt)
    out = {"site": site.group(1).capitalize() if site else "",
           "openreview": f"https://openreview.net/forum?id={orv.group(1)}" if orv else "",
           "room": room.group(1) if room else ""}
    if t:
        day = datetime.strptime(t.group(1), "%a, %b %d, %Y")
        s = datetime.strptime(f"{day:%Y-%m-%d} {t.group(2)}", "%Y-%m-%d %I:%M %p").replace(tzinfo=AEDT)
        e = datetime.strptime(f"{day:%Y-%m-%d} {t.group(3)}", "%Y-%m-%d %I:%M %p").replace(tzinfo=AEDT)
        if e <= s:
            e += timedelta(days=1)
        out["start_utc"], out["end_utc"] = s.astimezone(timezone.utc).isoformat(), e.astimezone(timezone.utc).isoformat()
    return vid, out


with ThreadPoolExecutor(3) as ex:
    for i, (vid, res) in enumerate(ex.map(fetch, todo), 1):
        done[vid] = res
        if i % 200 == 0:
            json.dump(done, open(OUT, "w"))
            print(i, "fetched")
json.dump(done, open(OUT, "w"), indent=0)
ok = sum(1 for v in done.values() if v.get("openreview"))
print(f"done: {len(done)} pages, {ok} with an OpenReview link, "
      f"{sum(1 for v in done.values() if 'error' in v)} errors")
