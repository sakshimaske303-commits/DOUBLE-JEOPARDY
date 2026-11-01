"""Coastal policy density and intensity for the five jurisdictions, compared with how many
low-lying buildings each setback reaches, plus a timeline of rule changes.

Run from the repository root:
    python scripts/analysis/coastal_policy_coding.py
Reads data/policy_coding/*.csv, data/setback_calibration_summary.csv and, if present,
data/regime/vdem_electoral_democracy.csv (scripts/acquisition/download_vdem_owid.py).
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "data"
PLOTS = os.path.join("outputs", "plots")
ORDER = ["canary", "lakshadweep", "seychelles", "fiji", "maldives"]
LABEL = {"maldives": "Maldives", "lakshadweep": "Lakshadweep", "seychelles": "Seychelles",
         "fiji": "Fiji", "canary": "Canary Islands"}
COLOR = {"maldives": "#2c7fb8", "seychelles": "#e34a33", "fiji": "#31a354",
         "canary": "#756bb1", "lakshadweep": "#fd8d3c"}
SUMMARY_NAME = {"Canary Islands": "canary", "Lakshadweep": "lakshadweep", "Seychelles": "seychelles",
                "Maldives": "maldives", "Fiji": "fiji"}

code = pd.read_csv(os.path.join(D, "policy_coding", "coastal_policy_coding.csv"))
code["value"] = pd.to_numeric(code["value"])
dens = code[code["item"].str.startswith("D")].pivot(index="jurisdiction", columns="item", values="value")
inten = code[code["item"].str.startswith("I")].pivot(index="jurisdiction", columns="item", values="value")

out = pd.DataFrame(index=ORDER)
out["density"] = dens.sum(axis=1)
out["density_max"] = dens.shape[1]
out["setback_inhabited_m"] = inten["I1_setback_inhabited_m"]
out["setback_general_m"] = inten["I2_setback_general_m"]
out["intensity"] = ((inten["I1_setback_inhabited_m"] + inten["I2_setback_general_m"]) / 2 / 100).round(3)
out["items_not_primary"] = code[code["verification"] != "primary"].groupby("jurisdiction").size()
out["items_not_primary"] = out["items_not_primary"].fillna(0).astype(int)

sb = pd.read_csv(os.path.join(D, "setback_calibration_summary.csv"))
sb = sb[sb["variant"] == "all"].copy()
sb["jurisdiction"] = sb["island"].map(SUMMARY_NAME)
sb = sb.set_index("jurisdiction").reindex(ORDER)
has_rule = out["setback_general_m"] > 0
out["low_buildings"] = sb["low_buildings"]
out["low_reached_by_setback_pct"] = (100 - sb["low_outside_every_setback_pct"]).round(1).where(has_rule, 0.0)
out["setback_for_75pct_low_m"] = sb["setback_covering_75pct_low_m"]

tl = pd.read_csv(os.path.join(D, "policy_coding", "coastal_policy_timeline.csv"))
tl["year"] = tl["date"].astype(str).str[:4].astype(int)
counts = tl.pivot_table(index="jurisdiction", columns="direction", values="instrument", aggfunc="count").reindex(ORDER).fillna(0).astype(int)
for c in ["expansion", "dismantling", "reallocation"]:
    out[f"changes_{c}"] = counts[c] if c in counts else 0

vdem_path = os.path.join(D, "regime", "vdem_electoral_democracy.csv")
vdem = None
if os.path.exists(vdem_path):
    vdem = pd.read_csv(vdem_path)
    last = vdem.sort_values("year").groupby("jurisdiction").tail(1).set_index("jurisdiction")
    out["vdem_year"] = last["year"]
    out["electoral_democracy_vdem"] = last["electoral_democracy_vdem"].round(3)

    def at(j, y):
        s = vdem[(vdem["jurisdiction"] == j) & (vdem["year"] <= y)]
        return round(float(s.iloc[-1]["electoral_democracy_vdem"]), 3) if len(s) else np.nan
    tl["electoral_democracy_at_change"] = [at(j, y) for j, y in zip(tl["jurisdiction"], tl["year"])]
    tl.to_csv(os.path.join(D, "coastal_policy_timeline_with_regime.csv"), index=False)
else:
    print("V-Dem file not found; run scripts/acquisition/download_vdem_owid.py to add regime scores.")

out.index.name = "jurisdiction"
out.insert(0, "label", [LABEL[j] for j in out.index])
out.to_csv(os.path.join(D, "coastal_policy_scores.csv"))
print(out.to_string())

# ---------- Figure 11: density, intensity, reach ----------
os.makedirs(PLOTS, exist_ok=True)
panels = [("density", "Policy density\n(instrument types in force, of 6)", 6, "{:.0f}"),
          ("intensity", "Setback intensity\n(mean width / 100 m)", 1, "{:.2f}"),
          ("low_reached_by_setback_pct", "Low-lying buildings reached\nby the setback (%)", 100, "{:.1f}")]
fig, axes = plt.subplots(1, 3, figsize=(11, 3.9), sharey=True)
y = np.arange(len(ORDER))[::-1]
for ax, (col, title, xmax, fmt) in zip(axes, panels):
    vals = out.loc[ORDER, col].values
    ax.barh(y, vals, color=[COLOR[j] for j in ORDER], height=0.62)
    for yi, v in zip(y, vals):
        ax.text(v + xmax * 0.02, yi, fmt.format(v), va="center", fontsize=9)
    ax.set_xlim(0, xmax * 1.18); ax.set_title(title, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_yticks(y); axes[0].set_yticklabels([LABEL[j] for j in ORDER])
plt.figtext(0.5, 0.01, "Coding: data/policy_coding (rules in force, October 2026). Reach: share of buildings at or below 1 m "
            "that stand within the statutory setback (Section 4.8).", ha="center", fontsize=7, color="gray")
plt.tight_layout(rect=(0, 0.05, 1, 1))
plt.savefig(os.path.join(PLOTS, "fig11_policy_density_intensity.png"), dpi=200); plt.close()

# ---------- Figure 12: timeline ----------
MARK = {"expansion": ("^", "#2b8cbe"), "dismantling": ("v", "#d7301f"), "reallocation": ("D", "#6a51a3"),
        "reform": ("o", "#969696"), "implementation": ("o", "#d9d9d9")}
fig, ax = plt.subplots(figsize=(11, 4.4))
rows = {j: i for i, j in enumerate(ORDER[::-1])}
for _, r in tl.iterrows():
    m, c = MARK[r["direction"]]
    ax.scatter(r["year"], rows[r["jurisdiction"]], marker=m, s=90, color=c, edgecolor="white", zorder=3)
for j, i in rows.items():
    ax.axhline(i, color="#eeeeee", lw=1, zorder=1)
    if vdem is not None:
        s = vdem[vdem["jurisdiction"] == j]
        ax.plot(s["year"], i - 0.35 + 0.7 * s["electoral_democracy_vdem"], color="#bdbdbd", lw=1.2, zorder=2)
ax.set_yticks(list(rows.values())); ax.set_yticklabels([LABEL[j] for j in rows])
ax.set_xlim(1986, 2027); ax.set_ylim(-0.6, len(ORDER) - 0.4)
for k in ["expansion", "dismantling", "reallocation", "reform"]:
    m, c = MARK[k]; ax.scatter([], [], marker=m, color=c, s=70, label=k)
if vdem is not None:
    ax.plot([], [], color="#bdbdbd", lw=1.2, label="V-Dem electoral democracy (row band = 0 to 1)")
ax.legend(loc="upper left", fontsize=8, frameon=False, ncol=5, bbox_to_anchor=(0, 1.12))
ax.spines[["top", "right", "left"]].set_visible(False)
plt.figtext(0.5, 0.01, "Source: data/policy_coding/coastal_policy_timeline.csv. Direction coded as in the codebook.",
            ha="center", fontsize=7, color="gray")
plt.tight_layout(rect=(0, 0.04, 1, 1))
plt.savefig(os.path.join(PLOTS, "fig12_coastal_policy_timeline.png"), dpi=200); plt.close()
print("Saved fig11_policy_density_intensity.png and fig12_coastal_policy_timeline.png")
