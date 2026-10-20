"""Merge the subtopic and area names (data/labels/labels_raw.json) into labels.json.

labels_raw.json = {"fine": [{fine_id, name, one_line, keywords, coherence}],
                   "cons": {"broad": [{broad_id, name, one_line}], "fine_renames": [{fine_id, name, reason}]}}
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
raw = json.load(open(ROOT / "data/labels/labels_raw.json"))
fine = {f["fine_id"]: f for f in raw["fine"]}
for r in raw["cons"]["fine_renames"]:
    if r["fine_id"] in fine:
        fine[r["fine_id"]]["name"] = r["name"]
names = [f["name"] for f in fine.values()]
dupes = {n for n in names if names.count(n) > 1}
for f in fine.values():  # last-resort disambiguation
    if f["name"] in dupes:
        f["name"] = f'{f["name"]} ({f["keywords"][0]})'
assert len(fine) == 150, f"expected 150 subtopics, got {len(fine)}"
broad = {b["broad_id"]: {"name": b["name"], "one_line": b["one_line"]} for b in raw["cons"]["broad"]}
assert len(broad) == 20
labels = {"fine": {str(k): {kk: v[kk] for kk in ("name", "one_line", "keywords", "coherence")} for k, v in sorted(fine.items())},
          "broad": {str(k): v for k, v in sorted(broad.items())}}
json.dump(labels, open(ROOT / "data/labels/labels.json", "w"), indent=1)
print("labels:", len(labels["fine"]), "subtopics,", len(labels["broad"]), "areas")
