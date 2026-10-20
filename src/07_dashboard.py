"""Interactive charts (Plotly) for the web version: topic treemap coloured by growth since 2025,
area shares 2025 -> 2026, site mix, vocabulary trends, countries. Writes standalone HTML snippets
into docs/ and a combined dashboard page."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
P, OUT, DOCS = ROOT / "data/processed", ROOT / "outputs", ROOT / "docs"
(DOCS / "charts").mkdir(parents=True, exist_ok=True)
INK, A26, A25 = "#1f2a44", "#d9480f", "#8aa1b1"
FONT = dict(family="Inter, system-ui, sans-serif", size=13, color=INK)

df = pd.read_pickle(P / "papers_clustered.pkl")
labels = json.load(open(ROOT / "data/labels/labels.json"))
S = json.load(open(OUT / "stats.json"))
fine_name = {int(k): v["name"] for k, v in labels["fine"].items()}
fine_line = {int(k): v["one_line"] for k, v in labels["fine"].items()}
broad_name = {int(k): v["name"] for k, v in labels["broad"].items()}
d26, d25 = df[df.year == 2026], df[df.year == 2025]


def save(fig, name, height=600):
    fig.update_layout(font=FONT, height=height, margin=dict(l=10, r=10, t=60, b=10),
                      paper_bgcolor="white", plot_bgcolor="white")
    fig.write_html(DOCS / "charts" / f"{name}.html", include_plotlyjs="cdn", full_html=True,
                   config={"displaylogo": False, "responsive": True})
    return fig


# 1. treemap: area -> subtopic, size = 2026 papers, colour = change in share vs 2025
n26 = d26.groupby("fine").size()
n25 = d25.groupby("fine").size().reindex(n26.index, fill_value=0)
sh26, sh25 = 100 * n26 / n26.sum(), 100 * n25 / max(n25.sum(), 1)
t = pd.DataFrame({"fine": n26.index, "papers": n26.values, "share_2026": sh26.values, "share_2025": sh25.values})
t["growth"] = np.log2((t.share_2026 + 0.05) / (t.share_2025 + 0.05))
t["area"] = t.fine.map(lambda f: broad_name[int(df.loc[df.fine == f, "broad"].iloc[0])])
t["subtopic"] = t.fine.map(fine_name)
t["about"] = t.fine.map(fine_line)
hi = d26[d26.decision.isin(["oral", "spotlight"])].groupby("fine").size()
t["highlights"] = t.fine.map(hi).fillna(0).astype(int)
fig = px.treemap(t, path=[px.Constant("NeurIPS 2026"), "area", "subtopic"], values="papers", color="growth",
                 color_continuous_scale=["#3b5bdb", "#f1f3f5", "#d9480f"], range_color=(-1.5, 1.5),
                 custom_data=["share_2025", "share_2026", "highlights", "about"])
fig.update_traces(hovertemplate="<b>%{label}</b><br>%{value} papers in 2026<br>share 2025 → 2026: "
                  "%{customdata[0]:.2f}% → %{customdata[1]:.2f}%<br>orals + spotlights: %{customdata[2]}"
                  "<br><i>%{customdata[3]}</i><extra></extra>", root_color="white", textinfo="label+value")
fig.update_layout(title="All 9,110 papers by area and subtopic (colour: grew vs shrank since 2025)",
                  coloraxis_colorbar=dict(title="log₂ share<br>2026/2025", tickvals=[-1.5, 0, 1.5],
                                          ticktext=["shrank", "same", "grew"]))
save(fig, "treemap", 760)

# 2. dumbbell: area share 2025 -> 2026
b = pd.DataFrame(S["broad"]).sort_values("share_2026")
fig = go.Figure()
for _, r in b.iterrows():
    fig.add_trace(go.Scatter(x=[r.share_2025, r.share_2026], y=[r.topic, r.topic], mode="lines",
                             line=dict(color="#ced4da", width=3), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=b.share_2025, y=b.topic, mode="markers", name="2025", marker=dict(size=11, color=A25),
                         hovertemplate="%{y}: %{x:.1f}% in 2025<extra></extra>"))
fig.add_trace(go.Scatter(x=b.share_2026, y=b.topic, mode="markers", name="2026", marker=dict(size=13, color=A26),
                         hovertemplate="%{y}: %{x:.1f}% in 2026<extra></extra>"))
fig.update_layout(title="Share of papers per research area, 2025 → 2026", xaxis_title="% of accepted papers",
                  legend=dict(orientation="h", y=1.05, x=0))
save(fig, "areas_dumbbell", 650)

# 3. site mix
m = pd.DataFrame(S["site_mix_by_area"]).set_index("broad_name").sort_values("Sydney")
fig = go.Figure()
for site, col in [("Sydney", A26), ("Atlanta", "#5c7cfa"), ("Paris", "#94d82d")]:
    fig.add_trace(go.Bar(y=m.index, x=m[site], name=site, orientation="h", marker_color=col,
                         hovertemplate="%{y}<br>" + site + ": %{x:.1f}%<extra></extra>"))
fig.update_layout(barmode="stack", title="Which city presents which research (scheduled posters)",
                  xaxis=dict(title="% of the area's scheduled posters", range=[0, 100]),
                  legend=dict(orientation="h", y=1.05, x=0))
save(fig, "site_mix", 650)

# 4. vocabulary
v = pd.DataFrame(S["vocabulary"]).sort_values("delta_pp")
fig = go.Figure(go.Bar(y=v.term, x=v.delta_pp, orientation="h",
                       marker_color=[A26 if x > 0 else A25 for x in v.delta_pp],
                       customdata=np.stack([v.pct_2025, v.pct_2026], axis=1),
                       hovertemplate="<b>%{y}</b><br>%{customdata[0]:.1f}% → %{customdata[1]:.1f}% of abstracts<extra></extra>"))
fig.update_layout(title="What abstracts mention more (and less) than in 2025",
                  xaxis_title="change in % of abstracts (percentage points)")
save(fig, "vocabulary", 700)

# 5. countries
c26 = {c: p for c, _, p in S["countries_2026"]}
c25 = {c: p for c, _, p in S["countries_2025"]}
cs = [c for c, _, _ in S["countries_2026"][:15]][::-1]
fig = go.Figure([go.Bar(y=cs, x=[c25.get(c, 0) for c in cs], name="2025", orientation="h", marker_color=A25),
                 go.Bar(y=cs, x=[c26.get(c, 0) for c in cs], name="2026", orientation="h", marker_color=A26)])
fig.update_layout(barmode="group", title="Countries behind the papers",
                  xaxis_title="% of papers (with a mapped affiliation) with an author there",
                  legend=dict(orientation="h", y=1.05, x=0))
save(fig, "countries", 650)

t.sort_values("papers", ascending=False).to_csv(OUT / "subtopics_treemap_data.csv", index=False)
print("charts written to", DOCS / "charts")
