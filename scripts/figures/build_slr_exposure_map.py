"""Folium rebuild of the SLR exposure maps: settlements plotted red (at/below
1m), yellow (above 1m) or grey (no usable elevation), from the per-settlement
CSVs written by scripts/analysis/slr_exposure_analysis.py.

Updated 2026-10-10 (Forensic Review): settlements whose DEM reading is NoData,
outside the DEM extent, or on a water pixel with no land nearby are no longer
shown as "at risk" (previously Seychelles popups read "Elevation: -32767.0 m").
They are drawn grey with the reason, and the legend reports coverage.
Boundaries now come from the validated data/boundaries_v2 files.
"""
import os
import pandas as pd
import geopandas as gpd
import folium

DATA_DIR = "data/settlement_elevations_full"
BOUNDARY_DIR = "data/boundaries_v2"
OUT_DIR = "dashboard/static"

SLR_THRESHOLD_M = 1.0
RISK_COLOR = "#e63232"
SAFE_COLOR = "#f4d03f"

ISLANDS = ["maldives", "lakshadweep", "seychelles", "fiji", "canary"]
ISLAND_LABEL = {
    "maldives": "Maldives", "lakshadweep": "Lakshadweep", "seychelles": "Seychelles",
    "fiji": "Fiji", "canary": "Canary Islands",
}
BOUNDARY_FILE = {
    "maldives": "maldives_islands_v2.gpkg", "lakshadweep": "lakshadweep_islands_v2.gpkg",
    "seychelles": "seychelles_islands_v2.gpkg", "fiji": "fiji_islands_v2.gpkg",
    "canary": "canary_islands_v2.gpkg",
}
NO_DATA_COLOR = "#9e9e9e"
KEPT_STATUSES = {"valid", "snapped_to_land", "above_10m"}  # same as scripts/common/dem_sampling.py
STATUS_LABEL = {
    "deltadtm_nodata": "bare-earth model has no value here (below 10 m on the surface model)",
    "nodata": "DEM has no data here",
    "out_of_extent": "outside the DEM extent",
    "water_no_land_nearby": "point falls on water, no land pixel within ~60 m",
}


def build_island_map(island):
    csv_path = os.path.join(DATA_DIR, f"{island}.csv")
    if not os.path.exists(csv_path):
        print(f"  SKIPPED {island}: {csv_path} not found — run scripts/analysis/slr_exposure_analysis.py first.")
        return

    df = pd.read_csv(csv_path)
    boundary = gpd.read_file(os.path.join(BOUNDARY_DIR, BOUNDARY_FILE[island]))

    minx, miny, maxx, maxy = boundary.total_bounds
    center = [(miny + maxy) / 2, (minx + maxx) / 2]

    m = folium.Map(location=center, tiles="CartoDB positron")
    m.fit_bounds([[miny, minx], [maxy, maxx]])

    folium.GeoJson(
        boundary.__geo_interface__,
        name="Island Boundary",
        style_function=lambda f: {"color": "#2d7a3e", "weight": 1.2, "fillOpacity": 0.03},
    ).add_to(m)

    safe_group = folium.FeatureGroup(name="Above 1m elevation")
    risk_group = folium.FeatureGroup(name="At/below 1m elevation (SLR risk)")
    nodata_group = folium.FeatureGroup(name="No usable elevation (excluded)")

    if "status" not in df.columns:  # older CSV format
        df["status"] = "valid"
    df["kept"] = df["status"].isin(KEPT_STATUSES)

    for _, row in df.iterrows():
        if row["kept"]:
            note = " (water pixel; median of adjacent land pixels)" if row["status"] == "snapped_to_land" else ""
            popup_html = (
                f"<b>{row['name']}</b><br>"
                f"Elevation: {row['elevation_m']:.1f} m{note}<br>"
                f"{'At/below 1m — SLR risk' if row['at_risk'] else 'Above 1m'}"
            )
            color = RISK_COLOR if row["at_risk"] else SAFE_COLOR
            group = risk_group if row["at_risk"] else safe_group
        else:
            popup_html = (f"<b>{row['name']}</b><br>No usable elevation: "
                          f"{STATUS_LABEL.get(row['status'], row['status'])}<br>Excluded from the percentage")
            color, group = NO_DATA_COLOR, nodata_group
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=4,
            color="#000000",
            weight=0.4,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(group)

    nodata_group.add_to(m)
    safe_group.add_to(m)
    risk_group.add_to(m)

    n_all = len(df)
    n_total = int(df["kept"].sum())
    n_risk = int((df["kept"] & df["at_risk"].astype(bool)).sum())
    pct_risk = (n_risk / n_total * 100) if n_total else 0

    legend_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: white; padding: 12px 16px; border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3); font-family: sans-serif; font-size: 13px; max-width: 300px;">
      <b>{ISLAND_LABEL[island]} — Sea-Level-Rise Exposure</b><br>
      {pct_risk:.1f}% of {n_total} named places with a usable elevation are at or below 1m<br>
      ({n_all - n_total} of {n_all} named places have no usable elevation and are shown grey)<br>
      <span style="font-size:11px;color:#555;">Elevation: {"DeltaDTM (bare earth)" if str(df.get("elevation_source", pd.Series(["copernicus"])).iloc[0]) == "deltadtm" else "Copernicus GLO-30 (surface)"}; heights above EGM2008</span><br><br>
      <span style="color:{RISK_COLOR};">●</span> At/below 1m &nbsp;
      <span style="color:{SAFE_COLOR};">●</span> Above 1m &nbsp;
      <span style="color:{NO_DATA_COLOR};">●</span> No usable elevation
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=False).add_to(m)

    island_dir = os.path.join(OUT_DIR, f"{island}_slr_exposure_webmap")
    os.makedirs(island_dir, exist_ok=True)
    out_path = os.path.join(island_dir, "index.html")
    m.save(out_path)
    print(f"  Saved: {out_path}  ({n_total} settlements, {n_risk} at risk, {pct_risk:.1f}%)")
    return {"island": island, "total": n_total, "at_risk": n_risk, "pct_at_risk": round(pct_risk, 1)}


def main():
    print("Building SLR exposure maps...\n")
    results = []
    for island in ISLANDS:
        print(f"{island.upper()}:")
        r = build_island_map(island)
        if r:
            results.append(r)
        print()
    print("Done.")
    if results:
        for r in results:
            print(f"  {r['island']:<12} {r['pct_at_risk']}% at risk ({r['at_risk']}/{r['total']})")


if __name__ == "__main__":
    main()
