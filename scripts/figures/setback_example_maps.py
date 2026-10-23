"""Close-up maps for the coastal setback analysis (paper Figure 10)."""
import os
import sys
import runpy
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
D = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs", "plots", "fig10_setback_close_ups.png")
sc = runpy.run_path(os.path.join(ROOT, "scripts", "analysis", "setback_calibration.py"), run_name="setback_lib")
polygons, SETBACK, LABEL = sc["polygons"], sc["SETBACK"], sc["LABEL"]
ISLANDS = ["maldives", "lakshadweep", "seychelles", "fiji", "canary"]
HALF = 0.035  # degrees
RED, BLUE, GREY = "#d7301f", "#2c7fb8", "#bdbdbd"


def window(b):
    low = b[(b.elev_m <= 1) & (b.elev_m >= 0) & (b.on_land | (b.dist_coast_m >= -50))]
    key = low.assign(lo=(low.lon / 0.05).round() * 0.05, la=(low.lat / 0.05).round() * 0.05)
    la, lo = key.groupby(["la", "lo"]).size().idxmax()
    sub = low[(abs(low.lat - la) < 0.05) & (abs(low.lon - lo) < 0.05)]
    return sub.lon.median(), sub.lat.median()


files = {i: os.path.join(D, f"buildings/{i}_buildings_setback.csv.gz") for i in ISLANDS}
if not all(os.path.exists(f) for f in files.values()):
    print("Skipped: run scripts/analysis/setback_calibration.py first")
    sys.exit(0)

fig, axes = plt.subplots(2, 3, figsize=(13, 9))
for ax, isl in zip(axes.flat, ISLANDS):
    b = pd.read_csv(files[isl])
    cx, cy = window(b)
    k = np.cos(np.radians(cy))
    hx = HALF / k
    in_win = (abs(b.lon - cx) < hx) & (abs(b.lat - cy) < HALF)
    w = b[in_win]
    near = w.on_land | (w.dist_coast_m >= -50)
    low = w[near & (w.elev_m <= 1) & (w.elev_m >= 0)]
    sb = max(SETBACK[isl]) if SETBACK[isl] else 0
    inside = low[low.dist_coast_m <= sb]
    outside = low[low.dist_coast_m > sb]
    for rings in polygons(os.path.join(D, f"boundaries_v2/{isl}_islands_v2.gpkg")):
        ext = rings[0]
        if ext[:, 0].max() < cx - hx or ext[:, 0].min() > cx + hx or ext[:, 1].max() < cy - HALF or ext[:, 1].min() > cy + HALF:
            continue
        ax.fill(ext[:, 0], ext[:, 1], color="#f3efe6", ec="#8c8c8c", lw=0.6, zorder=0)
    ax.scatter(w.lon, w.lat, s=1.2, c=GREY, lw=0, zorder=1)
    ax.scatter(inside.lon, inside.lat, s=5, c=BLUE, lw=0, zorder=3)
    ax.scatter(outside.lon, outside.lat, s=5, c=RED, lw=0, zorder=2)
    ax.set_xlim(cx - hx, cx + hx); ax.set_ylim(cy - HALF, cy + HALF); ax.set_aspect(1 / k)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor("#e8f1f8")
    rule = f"{'/'.join(map(str, SETBACK[isl]))} m setback" if SETBACK[isl] else "no national setback"
    ns = "N" if cy >= 0 else "S"; ew = "E" if cx >= 0 else "W"
    ax.set_title(f"{LABEL[isl]} ({rule})\n{abs(cy):.2f}° {ns}, {abs(cx):.2f}° {ew}", fontsize=10, loc="left")
    ax.text(0.02, 0.02, f"low buildings in view: {len(low):,}\nlandward of setback: {len(outside):,}",
            transform=ax.transAxes, fontsize=8, va="bottom", bbox=dict(fc="white", ec="none", alpha=0.85))
    # 1 km scale bar
    x0 = cx + hx * 0.45; y0 = cy - HALF * 0.88; dx = 1000 / (111320 * k)
    ax.plot([x0, x0 + dx], [y0, y0], color="black", lw=2); ax.text(x0 + dx / 2, y0 + HALF * 0.03, "1 km", ha="center", fontsize=8)

leg = axes.flat[5]; leg.axis("off")
for c, s, t in [(GREY, 20, "building above 1 m"), (BLUE, 40, "building at or below 1 m, inside the statutory setback"),
                (RED, 40, "building at or below 1 m, landward of the setback\n(or where there is none)")]:
    leg.scatter([], [], c=c, s=s, label=t)
leg.legend(loc="center left", frameon=False, fontsize=9.5, title="Buildings (Overture Maps 2026-08-19.0)", title_fontsize=9.5)
leg.text(0, 0.12, "Window: ~7 km around the densest cluster of low buildings.\nElevation: DeltaDTM v1.1 (bare earth), EGM2008; cells below 0 m left out.\n"
         "Canary Islands: the 20 m urban rule would leave more red.", transform=leg.transAxes, fontsize=8, color="gray")
fig.suptitle("Where the low-lying buildings are, and where the setback line is", x=0.01, ha="left", fontsize=13)
plt.tight_layout(h_pad=3.0, rect=(0, 0, 1, 0.97))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=200); plt.close()
print("Saved:", OUT)
