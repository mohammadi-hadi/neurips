"""Story figures: every chart states its finding in the title.

Blog figures (outputs/figures/):
- field_moved.png        the 2026 map coloured by how much each subtopic's share changed since 2025
- agents_family.png      papers per agent subtopic, 2025 vs 2026
- areas_slope.png        area shares 2025 -> 2026
- movers_x.png           subtopics that gained and lost the most share
- cities_lean.png        which areas lean to Sydney, Atlanta or Paris
- vocabulary_trends.png, highlight_rate_by_area.png, top_institutions.png, countries.png
Social cards (outputs/carousel/, 1080x1350): drawn separately with large type, not shrunk blog figures.

Subtopics are fitted on 2026 papers; each 2025 paper is assigned to its nearest subtopic in the
embedding space. "Factor" always means the plain ratio of shares, share_2026 / share_2025.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from common import load_papers
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parents[1]
P, OUT = ROOT / "data/processed", ROOT / "outputs"
FIG, CAR = OUT / "figures", OUT / "carousel"
FIG.mkdir(parents=True, exist_ok=True)
CAR.mkdir(parents=True, exist_ok=True)

INK, MUTED, ACC, COOL, GREY, BG = "#1f2a44", "#6b7489", "#d9480f", "#3b5bdb", "#b8bfcc", "#fbfaf7"
CITY = {"Sydney": "#0b7285", "Atlanta": "#862e9c", "Paris": "#e8a20c"}  # distinct from grew/shrank colours
plt.rcParams.update({"font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#c9ced8",
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": INK,
                     "legend.labelcolor": INK, "figure.facecolor": BG, "axes.facecolor": BG,
                     "savefig.facecolor": BG, "savefig.bbox": "tight", "savefig.dpi": 200})
SOURCE = "Data: NeurIPS 2025 & 2026 accepted papers (neurips.cc) · Analysis: Hadi Mohammadi · github.com/mohammadi-hadi/neurips"
URL = "mohammadi.cv/neurips/2026"

df = load_papers()
L = json.load(open(ROOT / "data/labels/labels.json"))
S = json.load(open(OUT / "stats.json"))
fine_name = {int(k): v["name"] for k, v in L["fine"].items()}
broad_name = {int(k): v["name"] for k, v in L["broad"].items()}
d26, d25 = df[df.year == 2026], df[df.year == 2025]
growth_conf = len(d26) / len(d25)
fine = pd.read_csv(OUT / "topics_fine.csv", index_col=0)


def frame(fig, title, subtitle, y=0.995):
    fig.text(0.01, y, title, fontsize=19, fontweight="bold", color=INK, va="top")
    fig.text(0.01, y - 0.045, subtitle, fontsize=11.5, color=MUTED, va="top")
    fig.text(0.01, 0.005, SOURCE, fontsize=8, color=MUTED, va="bottom")


def outline(t, w=3):
    t.set_path_effects([pe.withStroke(linewidth=w, foreground=BG)])


def grid_x(ax):
    ax.grid(axis="x", color="#e6e8ee", lw=0.8)
    ax.set_axisbelow(True)


# ================= 1. where the field moved =================
# Colour = growth of the subtopic each 2026 paper belongs to (shares come from the embedding-space
# assignment, not from map positions), smoothed over the 2026 map and shown only where papers are.
sh26 = d26.fine.value_counts(normalize=True)
sh25 = d25.fine.value_counts(normalize=True).reindex(sh26.index, fill_value=0)
grow = np.log2((sh26 + 0.0005) / (sh25 + 0.0005)).clip(-1.5, 1.5)
xmin, xmax = d26.x.quantile([0.002, 0.998]); ymin, ymax = d26.y.quantile([0.002, 0.998])
ext = [xmin - 0.6, xmax + 0.6, ymin - 0.6, ymax + 0.6]
rng, bins, sig = [ext[:2], ext[2:]], 300, 3.5
cnt = gaussian_filter(np.histogram2d(d26.x, d26.y, bins=bins, range=rng)[0], sig)
wsum = gaussian_filter(np.histogram2d(d26.x, d26.y, bins=bins, range=rng, weights=d26.fine.map(grow))[0], sig)
field = np.ma.masked_where(cnt < 0.08, wsum / np.maximum(cnt, 1e-9))
med = d26.groupby("broad")[["x", "y"]].median()


def spread_labels(pos, dy=0.45, dx=2.2):
    pos = pos.copy()
    for _ in range(300):
        moved = False
        idx = list(pos.index)
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                ddx, ddy = pos.at[j, "x"] - pos.at[i, "x"], pos.at[j, "y"] - pos.at[i, "y"]
                if abs(ddy) < dy and abs(ddx) < dx:
                    step = 0.04 if ddy >= 0 else -0.04
                    pos.at[j, "y"] += step; pos.at[i, "y"] -= step; moved = True
        if not moved:
            break
    return pos


def draw_field(ax, keep=None, fs=10.5, scatter=True):
    ax.imshow(field.T, origin="lower", extent=ext, cmap="RdBu_r", vmin=-1.2, vmax=1.2, interpolation="bilinear")
    if scatter:
        ax.scatter(d26.x, d26.y, s=0.5, c=INK, alpha=0.15, linewidths=0)
    pos = med if keep is None else med.loc[[b for b in med.index if broad_name[b] in keep]]
    for b, r in spread_labels(pos, dx=2.2 * fs / 10.5, dy=0.45 * fs / 10.5).iterrows():
        outline(ax.text(r.x, r.y, broad_name[b], ha="center", va="center", fontsize=fs, color=INK,
                        fontweight="bold"), fs / 3)
    ax.set_xlim(ext[:2]); ax.set_ylim(ext[2:]); ax.axis("off")


def field_colorbar(fig, box, fs=9):
    cax = fig.add_axes(box)
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap="RdBu_r", norm=plt.Normalize(-1.2, 1.2)), cax=cax, orientation="horizontal")
    cb.set_ticks([-1, 0, 1]); cb.set_ticklabels(["half the share", "same", "double the share"])
    cb.outline.set_visible(False); cax.tick_params(labelsize=fs, colors=MUTED, length=0)


fig = plt.figure(figsize=(12, 12.6))
draw_field(fig.add_axes([0.0, 0.03, 1.0, 0.9]))
field_colorbar(fig, [0.68, 0.07, 0.28, 0.014])
frame(fig, "Where NeurIPS moved between 2025 and 2026",
      "Red topics grew their share of papers. Blue ones shrank.")
fig.savefig(FIG / "field_moved.png"); plt.close(fig)

# ================= 2. the agent family =================
agent_b = [k for k, n in broad_name.items() if "Agent" in n][0]
fam = sorted({int(f) for f in d26.loc[d26.broad == agent_b, "fine"]}, key=lambda f: -(d26.fine == f).sum())
c26 = np.array([(d26.fine == f).sum() for f in fam]); c25 = np.array([(d25.fine == f).sum() for f in fam])
n25, n26 = int((d25.broad == agent_b).sum()), int((d26.broad == agent_b).sum())
all_faster = bool((c26 / np.maximum(c25, 1)).min() > growth_conf)
agent_title = (f"Agent papers went from {n25} to {n26}"
               + (". Every agent topic grew faster than the conference." if all_faster else ""))


def draw_agents(ax, fs=10.5, lab_fs=9.5):
    yy = np.arange(len(fam))[::-1]
    ax.hlines(yy, c25, c26, color=ACC, lw=3, alpha=0.5)
    ax.scatter(c25, yy, s=60, color=GREY, zorder=3, label="2025")
    ax.scatter(c26, yy, s=80, color=ACC, zorder=4, label="2026")
    for y_, a_, b_ in zip(yy, c25, c26):
        ax.annotate(f"{a_} → {b_}", (b_, y_), xytext=(8, 0), textcoords="offset points", va="center",
                    fontsize=lab_fs, color=INK)
    ax.set_yticks(yy, [fine_name[f] for f in fam], fontsize=fs)
    ax.set_xlim(0, c26.max() * 1.22)
    ax.tick_params(axis="x", labelsize=fs - 1)
    ax.set_xlabel("papers", fontsize=fs - 1)
    grid_x(ax)
    ax.legend(frameon=False, loc="lower right", fontsize=fs - 1)


fig, ax = plt.subplots(figsize=(11, 7))
fig.subplots_adjust(top=0.86, bottom=0.14, left=0.36, right=0.95)
draw_agents(ax)
frame(fig, agent_title, f"Number of papers per agent topic. The whole conference grew {growth_conf:.1f}x. "
      f"Agent papers grew {n26 / n25:.1f}x.")
fig.savefig(FIG / "agents_family.png"); plt.close(fig)

# ================= 3. slope chart of areas =================
b = pd.DataFrame(S["broad"])


def spread(vals, gap):
    """Spread label positions symmetrically so neighbours are at least `gap` apart."""
    vals = np.asarray(vals, float)
    order = np.argsort(vals)
    pos = vals[order].copy()
    for _ in range(500):
        moved = False
        for k in range(1, len(pos)):
            d = pos[k] - pos[k - 1]
            if d < gap:
                push = (gap - d) / 2
                pos[k - 1] -= push; pos[k] += push; moved = True
        if not moved:
            break
    out = np.empty_like(pos); out[order] = pos
    return out


fig, ax = plt.subplots(figsize=(10, 13))
fig.subplots_adjust(top=0.88, left=0.03, right=0.97, bottom=0.05)
yl, yr = spread(b.share_2025, 0.2), spread(b.share_2026, 0.2)
for (_, row), a, c in zip(b.iterrows(), yl, yr):
    up, down = row.delta_pp > 0.5, row.delta_pp < -0.5
    col = ACC if up else (COOL if down else GREY)
    tcol = ACC if up else (COOL if down else MUTED)
    ax.plot([0, 1], [row.share_2025, row.share_2026], color=col, lw=2.6 if (up or down) else 1.2,
            solid_capstyle="round", zorder=3 if (up or down) else 1)
    ax.scatter([0, 1], [row.share_2025, row.share_2026], color=col, s=22, zorder=4)
    ax.plot([-0.06, -0.01], [a, row.share_2025], color="#c9ced8", lw=0.7)  # leader lines
    ax.plot([1.01, 1.06], [row.share_2026, c], color="#c9ced8", lw=0.7)
    ax.text(-0.07, a, f"{row.topic}  {row.share_2025:.1f}%", ha="right", va="center", fontsize=9.5, color=tcol)
    ax.text(1.07, c, f"{row.share_2026:.1f}%  {row.topic}", ha="left", va="center", fontsize=9.5, color=tcol,
            fontweight="bold" if abs(row.delta_pp) > 1 else "normal")
ax.set_xlim(-0.95, 1.95); ax.axis("off")
top_y = max(yl.max(), yr.max()) + 0.45
ax.text(0, top_y, "2025", ha="center", fontsize=12, fontweight="bold", color=INK)
ax.text(1, top_y, "2026", ha="center", fontsize=12, fontweight="bold", color=INK)
frame(fig, "LLM agents doubled their share. 3D vision and graph learning shrank.",
      "Share of all papers per area. Orange: up more than half a point. Blue: down more than half a point. Grey: smaller change.")
fig.savefig(FIG / "areas_slope.png"); plt.close(fig)

# ================= 4. subtopics that gained and lost the most share =================
up = fine[fine.n_2026 >= 40].sort_values("delta_pp", ascending=False).head(10)
dn = fine[fine.n_2025 >= 30].sort_values("delta_pp").head(8)
k_agents = int(sum("Agent" in n for n in up.index))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14.5, 7.8), gridspec_kw={"wspace": 0.95})
fig.subplots_adjust(top=0.82, bottom=0.13, left=0.23, right=0.97)
for ax, t, col, ttl in [(a1, up.iloc[::-1], ACC, "Gained most share"), (a2, dn.iloc[::-1], COOL, "Lost most share")]:
    yy = np.arange(len(t))
    ax.hlines(yy, t.share_2025, t.share_2026, color=col, lw=2.5, alpha=0.6)
    ax.scatter(t.share_2025, yy, color=GREY, s=40, zorder=3, label="2025")
    ax.scatter(t.share_2026, yy, color=col, s=55, zorder=4, label="2026")
    ax.set_yticks(yy, t.index, fontsize=10)
    for y_, (_, row) in zip(yy, t.iterrows()):
        lab = (f"{row.n_2025:.0f} → {row.n_2026:.0f} papers" if row.n_2025 < 15
               else (f"×{row.growth_x:.1f}" if row.growth_x >= 1 else f"×{row.growth_x:.2f}"))
        ax.annotate(lab, (max(row.share_2025, row.share_2026), y_), xytext=(7, 0), textcoords="offset points",
                    va="center", fontsize=9.5, color=col, fontweight="bold", annotation_clip=False)
    ax.set_xlim(0, max(t.share_2025.max(), t.share_2026.max()) * 1.32)
    ax.set_title(ttl, loc="left", fontsize=13, color=col, fontweight="bold")
    ax.set_xlabel("% of accepted papers")
    grid_x(ax)
a1.legend(frameon=False, loc="lower right", fontsize=9)
frame(fig, "Agent topics gained the most ground",
      "Grey dot: 2025. Coloured dot: 2026. The label shows how many times bigger or smaller the share got "
      "(paper counts for topics that were tiny in 2025).")
fig.savefig(FIG / "movers_x.png"); plt.close(fig)

# ================= 5. cities =================
m = pd.DataFrame(S["site_mix_by_area"]).set_index("broad_name")
avg = S["site_overall_pct"]
n_unsched = S["site_counts"].get("unscheduled", 0)
lean = m[["Sydney", "Atlanta", "Paris"]].sub(pd.Series(avg)[["Sydney", "Atlanta", "Paris"]], axis=1).sort_values("Sydney")
fig, ax = plt.subplots(figsize=(10, 9.4))
fig.subplots_adjust(top=0.83, bottom=0.12, left=0.3, right=0.97)
yy = np.arange(len(lean))
ax.axvline(0, color="#9aa3b5", lw=1)
for y_ in yy:
    ax.hlines(y_, lean.iloc[y_].min(), lean.iloc[y_].max(), color="#d5d9e2", lw=1.5, zorder=1)
for c in ["Sydney", "Atlanta", "Paris"]:
    ax.scatter(lean[c], yy, s=70, color=CITY[c], label=f"{c} (overall {avg[c]:.0f}%)", zorder=3,
               edgecolor=BG, linewidths=0.9)
ax.set_yticks(yy, lean.index)
ax.set_xlabel("points above or below the overall share")
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.4, 1.0), ncol=3, fontsize=10)
grid_x(ax)
frame(fig, "Vision and robotics went to Sydney. Theory leans to Paris.",
      f"How far each area is from the overall split: {avg['Sydney']:.0f}% Sydney, "
      f"{avg['Atlanta']:.0f}% Atlanta, {avg['Paris']:.0f}% Paris.")
fig.savefig(FIG / "cities_lean.png"); plt.close(fig)

# ================= 6. vocabulary, orals, organisations, countries =================
v = pd.DataFrame(S["vocabulary"]).sort_values("delta_pp")
fig, ax = plt.subplots(figsize=(10, 9.5))
fig.subplots_adjust(top=0.87, bottom=0.1, left=0.36, right=0.95)
ax.barh(v.term, v.delta_pp, color=[ACC if x > 0 else COOL for x in v.delta_pp], height=0.65)
for i, (p26, dlt) in enumerate(zip(v.pct_2026, v.delta_pp)):
    ax.text(dlt + 0.15 if dlt >= 0 else 0.15, i, f"{p26:.0f}%", va="center", fontsize=8.5, color=MUTED)
ax.axvline(0, color="#9aa3b5", lw=1)
ax.set_xlabel("change since 2025, in points")
grid_x(ax)
frame(fig, "More papers talk about benchmarks and agents. Fewer say 'efficient'.",
      "Change since 2025 in the share of papers that use each term. The label is the 2026 share.")
fig.savefig(FIG / "vocabulary_trends.png"); plt.close(fig)

r = pd.DataFrame(S["highlight_rate_by_area"]).sort_values("rate_pct")
avg_hi = S["highlight_rate_overall_pct"]
p0 = avg_hi / 100
sig_band = 200 * np.sqrt(p0 * (1 - p0) / r.papers)  # 2 standard errors, in percent
cols = [ACC if x - avg_hi > s else (COOL if avg_hi - x > s else GREY) for x, s in zip(r.rate_pct, sig_band)]
fig, ax = plt.subplots(figsize=(10, 8.5))
fig.subplots_adjust(top=0.86, bottom=0.1, left=0.3, right=0.95)
ax.hlines(r.broad_name, 0, r.rate_pct, color="#d5d9e2", lw=2)
ax.scatter(r.rate_pct, r.broad_name, s=70, color=cols, zorder=3)
ax.axvline(avg_hi, color=INK, ls="--", lw=1)
ax.text(avg_hi + 0.08, len(r) - 0.6, f"conference average {avg_hi:.1f}%", fontsize=9, color=INK)
ax.set_xlabel("% of the area's papers selected as oral or spotlight")
grid_x(ax)
leader = r.iloc[-1]
frame(fig, f"{leader.broad_name} papers get the most orals and spotlights",
      "Share of each area's papers with a decision that became an oral or spotlight. Grey means the gap could be chance.")
fig.savefig(FIG / "highlight_rate_by_area.png"); plt.close(fig)

top = S["institutions_2026"][:20][::-1]
fig, ax = plt.subplots(figsize=(9, 8))
fig.subplots_adjust(top=0.86, bottom=0.1, left=0.3, right=0.95)
ax.barh([t[0] for t in top], [t[1] for t in top], color=INK, height=0.65)
for i, t in enumerate(top):
    ax.text(t[1] + 4, i, str(t[1]), va="center", fontsize=9, color=MUTED)
ax.set_xlabel("papers with at least one author from the organisation")
grid_x(ax)
frame(fig, f"{top[-1][0]} is on the most papers: {top[-1][1]}",
      "The 20 organisations with the most NeurIPS 2026 papers.")
fig.savefig(FIG / "top_institutions.png"); plt.close(fig)

cc26 = {c: p_ for c, _, p_ in S["countries_2026"]}; cc25 = {c: p_ for c, _, p_ in S["countries_2025"]}
cs = [c for c, _, _ in S["countries_2026"][:12]][::-1]
fig, ax = plt.subplots(figsize=(9, 7))
fig.subplots_adjust(top=0.84, bottom=0.12, left=0.2, right=0.95)
yy = np.arange(len(cs))
ax.hlines(yy, [cc25.get(c, 0) for c in cs], [cc26.get(c, 0) for c in cs], color="#c9ced8", lw=2.5)
ax.scatter([cc25.get(c, 0) for c in cs], yy, s=50, color=GREY, label="2025", zorder=3)
ax.scatter([cc26.get(c, 0) for c in cs], yy, s=70, color=ACC, label="2026", zorder=4)
ax.set_yticks(yy, cs)
ax.set_xlabel("% of papers (with a mapped affiliation) that have an author from the country")
ax.legend(frameon=False, loc="lower right")
grid_x(ax)
frame(fig, f"The US is on {cc26['USA']:.0f}% of papers, China on {cc26['China']:.0f}%",
      f"Share of papers with at least one author from each country. China was at {cc25['China']:.0f}% in 2025.")
fig.savefig(FIG / "countries.png"); plt.close(fig)

# ================= 7. social cards, 1080 x 1350, large type =================
W, H = 5.4, 6.75  # inches at 200 dpi


def card(name, kicker, big, line, draw, box=(0.06, 0.1, 0.88, 0.52)):
    fig = plt.figure(figsize=(W, H), dpi=200)
    fig.patch.set_facecolor(BG)
    fig.text(0.07, 0.945, kicker, fontsize=11, color=ACC, fontweight="bold", va="top")
    t = fig.text(0.07, 0.895, big, fontsize=26, color=INK, fontweight="bold", va="top", linespacing=1.05)
    fig.canvas.draw()
    bottom = t.get_window_extent().transformed(fig.transFigure.inverted()).y0
    fig.text(0.07, bottom - 0.025, line, fontsize=12.5, color=INK, va="top", linespacing=1.3)
    draw(fig, box)
    fig.text(0.07, 0.035, URL, fontsize=9.5, color=MUTED)
    with plt.rc_context({"savefig.bbox": "standard"}):
        fig.savefig(CAR / name, dpi=200, facecolor=BG)
    plt.close(fig)


def draw_img(path):
    def f(fig, box):
        ax = fig.add_axes(box); ax.imshow(plt.imread(path)); ax.axis("off")
    return f


def draw_field_card(fig, box):
    ax = fig.add_axes(box)
    keep = {"LLM Agents", "LLM Post-Training", "Robotics & Embodied AI", "3D Vision & Perception", "Graph Learning",
            "Diffusion, Flows & Inference", "Image & 3D Generation"}
    draw_field(ax, keep=keep, fs=9.5, scatter=False)
    field_colorbar(fig, [box[0] + 0.12, box[1] - 0.025, box[2] - 0.24, 0.012], fs=8.5)


def draw_atlas_card(fig, box):
    ax = fig.add_axes(box)
    pal = plt.get_cmap("tab20")
    ax.scatter(d26.x, d26.y, s=1.2, c=[pal(int(b) % 20) for b in d26.broad], alpha=0.75, linewidths=0)
    keep = {"LLM Agents", "LLM Behavior & Safety", "Robotics & Embodied AI", "3D Vision & Perception",
            "Reinforcement Learning", "DL Theory & Neuroscience", "Biomolecules & Causal Discovery", "Image & 3D Generation"}
    pos = spread_labels(med.loc[[b for b in med.index if broad_name[b] in keep]], dx=2.6, dy=0.55)
    for b, r in pos.iterrows():
        outline(ax.text(r.x, r.y, broad_name[b], ha="center", va="center", fontsize=9, color=INK, fontweight="bold"), 3)
    ax.set_xlim(ext[:2]); ax.set_ylim(ext[2:]); ax.axis("off")


def draw_agents_card(fig, box):
    ax = fig.add_axes([box[0] + 0.47, box[1], box[2] - 0.5, box[3]])
    draw_agents(ax, fs=8, lab_fs=8)
    ax.get_legend().remove()


ag = next(x for x in S["broad"] if "Agent" in x["topic"])
card("1_cover.png", "NeurIPS 2026 · paper atlas", "9,110 papers,\none map",
     "Every accepted paper, placed by what its\nabstract says. What changed since 2025?",
     draw_atlas_card, (0.03, 0.07, 0.94, 0.58))
card("2_agents.png", "Biggest shift", f"LLM agents:\n{ag['share_2025']:.1f}% → {ag['share_2026']:.1f}%",
     f"{n25} → {n26} papers. {k_agents} of the 10 subtopics that\ngained the most share are about agents.",
     draw_agents_card, (0.05, 0.1, 0.9, 0.5))
card("3_moved.png", "Where the field moved", "Red grew,\nblue shrank",
     "The 2026 map, coloured by how each\nsubtopic's share changed since 2025.",
     draw_field_card, (0.02, 0.12, 0.96, 0.5))
card("4_explore.png", "Explore it yourself", "Search all\n9,110 papers",
     "Recolour by change, city or status,\nfilter by day, click any paper to open it.",
     draw_img(FIG / "atlas_screenshot.png") if (FIG / "atlas_screenshot.png").exists() else draw_img(FIG / "atlas_card.png"),
     (0.03, 0.08, 0.94, 0.56))
print("story figures and carousel written; agents in top-10 gainers:", k_agents)
