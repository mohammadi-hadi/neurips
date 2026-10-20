# NeurIPS 2026 Paper Atlas

A data-driven tour of the accepted papers at NeurIPS 2026: what the field is working on, what grew
and shrank since 2025, where the orals and spotlights went, who wrote the papers, and how the
research is split across the three conference sites (Sydney, Atlanta, Paris).

- **Blog post:** [`report/BLOG.md`](report/BLOG.md) (web version: `docs/index.html`)
- **Appendix:** [`report/APPENDIX.md`](report/APPENDIX.md), every area and subtopic with counts, shares and orals
- **Interactive map:** `docs/atlas.html` (open in a browser; search, hover, click a dot to open the paper)
- **Interactive charts:** `docs/charts/` (treemap of all subtopics, area shifts, cities, vocabulary, countries)
- **Tables:** `outputs/*.csv`, figures in `outputs/figures/`

## Data

All data comes from the public NeurIPS website:

| File | Source | Content |
|---|---|---|
| `neurips2026_papers_abstracts.csv` | "Download Data" export on [neurips.cc/Downloads/2026](https://neurips.cc/Downloads/2026) | 9,110 papers: title, authors with affiliations, abstract, link |
| `neurips2025_papers_abstracts.csv` | same export for [2025](https://neurips.cc/Downloads/2025) | 5,859 papers, used for the year-over-year comparison |
| `neurips2026_orals_posters_meta.json` | schedule data behind the virtual site | decision (oral / spotlight / poster), site, session, room, time |

Pulled on 20 October 2026. About 1,900 of the 2026 papers were not yet in the schedule data at that
time; they are included in the topic analysis and marked "not yet scheduled" in the site analysis.
The raw files are not stored in this repository; `src/00_fetch_data.py` downloads them again.

## Method

1. **Prepare** (`src/01_prepare.py`): join the abstract export with the schedule data on the
   paper id, normalise decisions, clean LaTeX and HTML from titles and abstracts.
2. **Embed** (`src/02_embed.py`): title + abstract of every 2025 and 2026 paper with
   [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B), run locally.
3. **Cluster** (`src/03_cluster.py`): 150 subtopics with k-means on the 2026 embeddings, grouped
   into 20 research areas. The taxonomy is fitted on 2026 only; each 2025 paper is assigned to its
   nearest 2026 subtopic, so the year-over-year shares compare like with like. UMAP gives the 2D map.
4. **Label** (`src/04_labels.md`): each subtopic is named from its most typical titles, abstracts and
   distinctive terms, then the full list is checked for overlaps and consistent naming.
5. **Statistics** (`src/05_stats.py`): topic shares, oral/spotlight rates, site mix, organisations
   and countries (top 1,200 affiliation strings merged into canonical names), team size, vocabulary trends.
6. **Map and charts** (`src/06_map.py`, `src/07_dashboard.py`): interactive and static maps with [DataMapPlot](https://github.com/TutteInstitute/datamapplot), interactive charts with Plotly.
7. **Site** (`src/08_appendix.py`, `src/09_build_site.py`): appendix tables and the web pages in `docs/`.

## Reproduce

```bash
uv venv -p 3.12 .venv && uv pip install -r requirements.txt
source .venv/bin/activate
python src/00_fetch_data.py
python src/01_prepare.py && python src/02_embed.py && python src/03_cluster.py
# labels: see src/04_labels.md, then
python src/04_apply_labels.py
python src/05_stats.py && python src/06_map.py && python src/07_dashboard.py
python src/08_appendix.py && python src/09_build_site.py   # needs pandoc
```

## Caveats

- Clusters are a lens, not ground truth: many papers sit between topics.
- Country and sector counts use the authors' listed affiliations; a paper counts once for every
  country or organisation that appears on it. The 1,200 most frequent affiliation strings are merged
  into canonical names with a country and sector; this covers 97% of 2025 and 94% of 2026 papers.
  Country and industry shares are computed over the papers with at least one mapped affiliation.
- The 2025 export and the 2026 export may differ slightly in which tracks they include.

Inspired by Jay Alammar's [Illustrated NeurIPS 2025](https://newsletter.languagemodels.co/p/the-illustrated-neurips-2025-a-visual).

Author: Hadi Mohammadi · [mohammadi.cv](https://mohammadi.cv)
