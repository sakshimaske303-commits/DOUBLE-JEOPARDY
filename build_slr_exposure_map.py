"""Folium rebuild of the SLR exposure maps: settlements plotted red (at/below
1m) or yellow (safe), from export_settlement_elevations_full.py's CSVs.
"""
import os
import pandas as pd
import geopandas as gpd
import folium

DATA_DIR = "data/settlement_elevations_full"
BOUNDARY_DIR = "data/boundaries"
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
    "maldives": "maldives_islands.gpkg", "lakshadweep": "lakshadweep_islands.gpkg",
    "seychelles": "seychelles_islands.gpkg", "fiji": "fiji_islands.gpkg",
    "canary": "canary_islands.gpkg",
}


def build_island_map(island):
    csv_path = os.path.join(DATA_DIR, f"{island}.csv")
    if not os.path.exists(csv_path):
        print(f"  SKIPPED {island}: {csv_path} not found — run export_settlement_elevations_full.py first.")
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

    safe_group = folium.FeatureGroup(name="Above 1m elevation (safe)")
    risk_group = folium.FeatureGroup(name="At/below 1m elevation (SLR risk)")

    for _, row in df.iterrows():
        popup_html = (
            f"<b>{row['name']}</b><br>"
            f"Elevation: {row['elevation_m']:.1f} m<br>"
            f"{'At/below 1m — SLR risk' if row['at_risk'] else '✓ Above 1m — safe'}"
        )
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=4,
            color="#000000",
            weight=0.4,
            fill=True,
            fill_color=RISK_COLOR if row["at_risk"] else SAFE_COLOR,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(risk_group if row["at_risk"] else safe_group)

    safe_group.add_to(m)
    risk_group.add_to(m)

    n_total = len(df)
    n_risk = int(df["at_risk"].sum())
    pct_risk = (n_risk / n_total * 100) if n_total else 0

    legend_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: white; padding: 12px 16px; border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3); font-family: sans-serif; font-size: 13px; max-width: 300px;">
      <b>{ISLAND_LABEL[island]} — Sea-Level-Rise Exposure</b><br>
      {pct_risk:.1f}% of {n_total} settlements at or below 1m elevation<br><br>
      <span style="color:{RISK_COLOR};">●</span> At/below 1m elevation (SLR risk) &nbsp;
      <span style="color:{SAFE_COLOR};">●</span> Above 1m elevation (safe)
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
