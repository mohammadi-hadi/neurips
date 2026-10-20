"""Join the neurips.cc CSV export (titles, authors, abstracts) with the schedule JSON
(decision, site, session, time) and clean text for embedding."""
import csv, json, re, html
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data/raw", ROOT / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)


def clean(s):
    s = html.unescape(s or "")
    s = re.sub(r"\$([^$]*)\$", lambda m: re.sub(r"\\[a-zA-Z]+|[{}^_\\]", " ", m.group(1)), s)
    return re.sub(r"\s+", " ", s).strip()


def split_authors(s):
    """'Name (Inst), Name (Inst A, Inst B)' -> [(name, inst)]; parentheses can nest commas."""
    out, depth, cur = [], 0, ""
    for ch in html.unescape(s or ""):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    res = []
    for a in out:
        a = a.strip()
        m = re.match(r"^(.*?)\s*\((.*)\)$", a)
        res.append((m.group(1).strip(), m.group(2).strip()) if m else (a, ""))
    return [r for r in res if r[0]]


def load_year(year):
    rows = list(csv.DictReader(open(RAW / f"neurips{year}_papers_abstracts.csv", encoding="utf-8")))
    df = pd.DataFrame({
        "year": year,
        "vid": [r["virtualsite_url"].rstrip("/").split("/")[-1] for r in rows],
        "url": [r["virtualsite_url"] for r in rows],
        "title": [clean(r["name"]) for r in rows],
        "abstract": [clean(r["abstract"]) for r in rows],
        "authors_raw": [r["speakers/authors"] for r in rows],
    })
    au = df["authors_raw"].map(split_authors)
    df["authors"] = au.map(lambda x: "; ".join(n for n, _ in x))
    df["institutions"] = au.map(lambda x: " | ".join(sorted({i for _, i in x if i})))
    df["n_authors"] = au.map(len)
    # one virtualsite id groups the 16 reproducibility-track papers; keep them, make uid unique
    df["uid"] = df["year"].astype(str) + "_" + df["vid"] + "_" + df.groupby("vid").cumcount().astype(str)
    df["repro_track"] = df["vid"].map(df["vid"].value_counts()) > 1
    return df.drop(columns="authors_raw")


def decision_norm(d):
    d = (d or "").lower()
    if "oral" in d:
        return "oral"
    if "spotlight" in d:
        return "spotlight"
    return "poster"


d26 = load_year(2026)
J = json.load(open(RAW / "neurips2026_orals_posters_meta.json"))["results"]
def tkey(t):
    return re.sub(r"[^a-z0-9]", "", clean(t).lower())


sites_by_vid = {}
for x in J:
    vid = (x.get("virtualsite_url") or "").rstrip("/").split("/")[-1]
    site = (x.get("session") or "").split(" ")[0]
    if x.get("eventtype") == "Poster" and site in ("Sydney", "Atlanta", "Paris"):
        sites_by_vid.setdefault(vid, set()).add(site)
meta = {}
for x in J:
    vid = (x.get("virtualsite_url") or "").rstrip("/").split("/")[-1]
    if x.get("eventtype") != "Poster" or vid in meta:
        continue
    sess = x.get("session") or ""
    meta[vid] = {
        "decision": decision_norm(x.get("decision")),
        "decision_raw": x.get("decision") or "",
        "site": (sess.split()[0] if sess.split() and sess.split()[0] in ("Sydney", "Atlanta", "Paris") else ""),
        "session": sess,
        "room": x.get("room_name") or "",
        "start": x.get("starttime") or "",
        "end": x.get("endtime") or "",
        "official_topic": x.get("topic") or "",
        "openreview": x.get("paper_url") or "",
    }
m = d26["vid"].map(meta)
for k in ["decision", "decision_raw", "site", "session", "room", "start", "end", "official_topic", "openreview"]:
    d26[k] = m.map(lambda v: v[k] if isinstance(v, dict) else "")
d26["scheduled"] = m.notna().astype(bool)
# strongest decision seen for the paper anywhere in the schedule (oral events have their own ids)
rank = {"poster": 0, "spotlight": 1, "oral": 2}
best = {}
for x in J:
    t = tkey(x.get("name"))
    d = decision_norm(x.get("decision"))
    if x.get("decision") and rank[d] >= rank.get(best.get(t), 0):
        best[t] = d
d26["decision"] = [best.get(tkey(t)) or (d if sc else "unknown") for t, d, sc in zip(d26["title"], d26["decision"], d26["scheduled"])]
# papers missing from the bulk schedule file: use their own pages (src/01b_fill_schedule.py)
fill_path = RAW / "neurips2026_schedule_fill.json"
fill = json.load(open(fill_path)) if fill_path.exists() else {}
d26["schedule_source"] = np.where(d26["scheduled"], "bulk schedule file", "")
for i in d26.index[~d26["scheduled"] | (d26["openreview"] == "")]:
    f = fill.get(d26.at[i, "vid"], {})
    if f.get("openreview") and not d26.at[i, "openreview"]:
        d26.at[i, "openreview"] = f["openreview"]
    if not d26.at[i, "scheduled"] and f.get("site") in ("Sydney", "Atlanta", "Paris"):
        room = re.match(r"(Paris Poster Hall|Hall \S+)", f.get("room", ""))
        d26.at[i, "site"], d26.at[i, "room"] = f["site"], room.group(1) if room else ""
        d26.at[i, "start"], d26.at[i, "end"] = f.get("start_utc", ""), f.get("end_utc", "")
        d26.at[i, "session"] = f"{f['site']} poster"
        d26.at[i, "scheduled"] = True
        d26.at[i, "schedule_source"] = "paper page"
d26.loc[~d26["scheduled"], "site"] = "unscheduled"
for v, f in fill.items():
    if f.get("site") in ("Sydney", "Atlanta", "Paris"):
        sites_by_vid.setdefault(v, set()).add(f["site"])
d26["all_sites"] = d26["vid"].map(lambda v: ",".join(sorted(sites_by_vid.get(v, []))))
d26["n_sites"] = d26["all_sites"].map(lambda v: len(v.split(",")) if v else 0)

d25 = load_year(2025)
d25["scheduled"] = False
for c in d26.columns:
    if c not in d25.columns:
        d25[c] = ""

both = pd.concat([d26, d25], ignore_index=True)
both = both[both["abstract"].str.len() > 50].reset_index(drop=True)
both["scheduled"] = both["scheduled"].astype(bool)
both["n_sites"] = pd.to_numeric(both["n_sites"], errors="coerce").fillna(0).astype(int)
for c in both.columns:
    if both[c].dtype == object:
        both[c] = both[c].fillna("").astype(str)
both.to_parquet(OUT / "papers.parquet", index=False)

s26 = both[both.year == 2026]
report = {
    "2026_rows": int(len(s26)),
    "2026_scheduled": int(s26["scheduled"].astype(bool).sum()),
    "2026_unscheduled": int((~s26["scheduled"].astype(bool)).sum()),
    "2026_repro_track": int(s26["repro_track"].sum()),
    "2026_schedule_from_paper_pages": int((s26["schedule_source"] == "paper page").sum()),
    "2026_with_openreview_link": int(s26["openreview"].str.startswith("https://openreview.net").sum()),
    "2026_decision": s26["decision"].value_counts().to_dict(),
    "2026_site": s26["site"].value_counts().to_dict(),
    "2026_all_sites": s26["all_sites"].value_counts().to_dict(),
    "2025_rows": int((both.year == 2025).sum()),
}
json.dump(report, open(OUT / "prepare_report.json", "w"), indent=2)
print(json.dumps(report, indent=2))
