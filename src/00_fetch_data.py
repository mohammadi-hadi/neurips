"""Download the public paper lists from neurips.cc into data/raw/.

- neurips{year}_papers_abstracts.csv : the "Download Data" export on https://neurips.cc/Downloads/{year}
  (posters, CSV: type, name, virtualsite_url, speakers/authors, abstract)
- neurips2026_orals_posters_meta.json : the schedule data used by the virtual site
  (decision, session, room, times)

The export is generated on the server and can take a few minutes.
"""
import re, sys
from pathlib import Path
import requests

RAW = Path(__file__).resolve().parents[1] / "data/raw"
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (research script; NeurIPS paper overview)"}


def export_csv(year):
    s = requests.Session()
    s.headers.update(UA)
    url = f"https://neurips.cc/Downloads/{year}"
    page = s.get(url, timeout=60).text
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page).group(1)
    r = s.post(url, headers={"Referer": url}, timeout=900, data={
        "csrfmiddlewaretoken": token, "format": "0", "posters": "on",
        "resource": "0", "submitaction": "Download Data"})
    r.raise_for_status()
    assert r.headers.get("Content-Type", "").startswith("text/csv"), "export did not return CSV"
    (RAW / f"neurips{year}_papers_abstracts.csv").write_bytes(r.content)
    print(year, len(r.content) // 1024, "KB")


def schedule_json():
    r = requests.get("https://neurips.cc/static/virtual/data/neurips-2026-orals-posters.json", headers=UA, timeout=300)
    r.raise_for_status()
    (RAW / "neurips2026_orals_posters_meta.json").write_bytes(r.content)
    print("schedule", len(r.content) // 1024, "KB")


if __name__ == "__main__":
    for y in (sys.argv[1:] or ["2026", "2025"]):
        export_csv(int(y))
    schedule_json()
