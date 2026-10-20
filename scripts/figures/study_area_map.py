"""Study-area figure built from the project's own data (added 2026-10-10).

Replaces outputs/plots/fig1_study_area_map.png, which was not produced by any
script in this repository and has wrong graticules (e.g. the Canary panel's
longitude labels run backwards; Lakshadweep islands are mispositioned by up
to ~1 degree). Every element here is drawn from repository data:
  land        data/boundaries_v2/<island>_islands_v2.gpkg (validated vs official land areas)
  coral reef  data/ecosystem_buffers/<island>_coral_clean.gpkg
  mangroves   data/mangroves/gmw_2020_by_island/<island>_mangroves_2020.gpkg
  settlements data/settlements/<island>_settlements_clean.gpkg
Output: outputs/plots/study_area_map.png
Needs geopandas, matplotlib, numpy.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

OUT = "outputs/plots/study_area_map.png"
ISLANDS = [("maldives", "Maldives", "Indian Ocean"), ("lakshadweep", "Lakshadweep (India)", "Arabian Sea"),
           ("seychelles", "Seychelles", "Western Indian Ocean"), ("fiji", "Fiji", "South Pacific"),
           ("canary", "Canary Islands (Spain)", "Eastern Atlantic")]
LAYERS = {
    "land": "data/boundaries_v2/{}_islands_v2.gpkg",
    "coral": "data/ecosystem_buffers/{}_coral_clean.gpkg",
    "mangrove": "data/mangroves/gmw_2020_by_island/{}_mangroves_2020.gpkg",
}
STYLE = {"land": dict(facecolor="#e8e2d0", edgecolor="#333333", linewidth=0.6),
         "coral": dict(facecolor="#f08080", edgecolor="none", alpha=0.8),
         "mangrove": dict(facecolor="#2e8b57", edgecolor="none")}


def load_rings(path):
    """List of polygons, each a list of (N, 2) lon/lat arrays (exterior first)."""
    import geopandas as gpd
    if not os.path.exists(path):
        return []
    gdf = gpd.read_file(path).to_crs(epsg=4326)
    out = []
    for geom in gdf.geometry:
        if geom is None or geom.is_empty:
            continue
        for poly in getattr(geom, "geoms", [geom]):
            if poly.geom_type != "Polygon":
                continue
            out.append([np.asarray(poly.exterior.coords)[:, :2]] + [np.asarray(i.coords)[:, :2] for i in poly.interiors])
    return out


def load_points(path):
    import geopandas as gpd
    gdf = gpd.read_file(path).to_crs(epsg=4326)
    pts = np.array([(g.centroid.x, g.centroid.y) for g in gdf.geometry if g is not None])
    if "fiji" in path:  # 6 points stored at ~0 deg longitude; see dem_sampling.fix_antimeridian_lon
        bad = np.abs(pts[:, 0]) < 10
        pts[bad, 0] = np.where(pts[bad, 0] + 180 > 180, pts[bad, 0] - 180, pts[bad, 0] + 180)
    return pts


def wrap(arr, island):
    if island == "fiji":
        arr = arr.copy()
        arr[:, 0] = np.where(arr[:, 0] < 0, arr[:, 0] + 360, arr[:, 0])
    return arr


def nice_step(span, max_ticks=5):
    for s in [0.1, 0.25, 0.5, 1, 2, 2.5, 5]:
        if span / s <= max_ticks:
            return s
    return 10


def lon_label(v):
    v = ((v + 180) % 360) - 180
    if abs(abs(v) - 180) < 1e-9:
        return "180°"
    return f"{abs(v):g}°{'E' if v >= 0 else 'W'}"


def lat_label(v):
    return f"{abs(v):g}°{'N' if v >= 0 else 'S'}"


def draw_panel(ax, island, title, basin, loaders):
    rings_by_layer = {k: [[wrap(r, island) for r in poly] for poly in loaders["rings"](p.format(island))]
                      for k, p in LAYERS.items()}
    for k in ["land", "mangrove", "coral"]:
        patches = [MplPolygon(poly[0], closed=True) for poly in rings_by_layer[k]]
        if patches:
            ax.add_collection(PatchCollection(patches, **STYLE[k]))
    pts = wrap(loaders["points"](f"data/settlements/{island}_settlements_clean.gpkg"), island)
    ax.scatter(pts[:, 0], pts[:, 1], s=1.2, color="#1f3b73", alpha=0.6, zorder=3, linewidths=0)

    # Extent from the settlement points (land files can contain large clipping
    # polygons, e.g. OSM land polygons around the antimeridian for Fiji).
    (x0, y0), (x1, y1) = pts.min(0), pts.max(0)
    padx, pady = (x1 - x0) * 0.06 + 0.05, (y1 - y0) * 0.06 + 0.05
    ax.set_xlim(x0 - padx, x1 + padx)
    ax.set_ylim(y0 - pady, y1 + pady)
    lat_mid = (y0 + y1) / 2
    ax.set_aspect(1 / np.cos(np.radians(lat_mid)))
    ax.set_facecolor("#d9eaf5")

    xs, ys = nice_step(x1 - x0 + 2 * padx, 2), nice_step(y1 - y0 + 2 * pady, 6)
    xt = np.arange(np.ceil((x0 - padx) / xs) * xs, x1 + padx, xs)
    yt = np.arange(np.ceil((y0 - pady) / ys) * ys, y1 + pady, ys)
    ax.set_xticks(xt)
    ax.set_xticklabels([lon_label(v) for v in xt], fontsize=7)
    ax.set_yticks(yt)
    ax.set_yticklabels([lat_label(v) for v in yt], fontsize=7)
    ax.grid(color="white", linewidth=0.5)

    # scale bar (km), placed bottom-left
    km_per_deg = 111.32 * np.cos(np.radians(lat_mid))
    span_km = (x1 - x0 + 2 * padx) * km_per_deg
    bar_km = [v for v in [5, 10, 20, 25, 50, 100, 200, 250, 500] if v <= span_km / 4][-1]
    bx, by = x0 - padx * 0.4, y0 - pady * 0.55
    ax.plot([bx, bx + bar_km / km_per_deg], [by, by], color="black", linewidth=2.5)
    ax.text(bx + bar_km / km_per_deg / 2, by + pady * 0.15, f"{bar_km} km", ha="center", fontsize=7)
    ax.annotate("N", xy=(0.95, 0.93), xytext=(0.95, 0.80), xycoords="axes fraction",
                ha="center", fontsize=9, fontweight="bold", arrowprops=dict(arrowstyle="-|>", color="black"))
    ax.set_title(f"{title}\n{basin} · {len(pts)} OSM settlement points", fontsize=9.5)


def make_figure(loaders):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, (island, title, basin) in zip(axes.flat, ISLANDS):
        draw_panel(ax, island, title, basin, loaders)
    leg = axes.flat[-1]
    leg.axis("off")
    for label, key in [("Land (OSM coastline, validated)", "land"), ("Coral reef (mapped)", "coral"),
                       ("Mangrove (GMW 2020)", "mangrove")]:
        leg.add_patch(plt.Rectangle((0, 0), 0, 0, label=label, **{k: v for k, v in STYLE[key].items() if k != "linewidth"}))
    leg.scatter([], [], s=12, color="#1f3b73", label="Settlement point (OpenStreetMap)")
    leg.legend(loc="center", fontsize=10, frameon=False, title="Study areas, WGS84", title_fontsize=11)
    fig.suptitle("DOUBLE JEOPARDY study areas: five island groups in three ocean basins", fontsize=14, fontweight="bold")
    fig.text(0.5, 0.01, "Sources: OpenStreetMap contributors (ODbL); Global Mangrove Watch v3 (Bunting et al. 2022); "
             "coral layers as listed in DATA_SOURCES_AND_LICENSES.md", ha="center", fontsize=8, color="gray")
    plt.tight_layout(rect=(0, 0.02, 1, 0.96))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, dpi=200)
    plt.close(fig)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    make_figure({"rings": load_rings, "points": load_points})
