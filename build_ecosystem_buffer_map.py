"""build_ecosystem_buffer_map.py — folium rebuild of the ecosystem buffer
overview maps, replacing the old QGIS2Web exports. One map per island,
layering whichever of mangroves / coral / WDPA-protected-areas / island
boundary actually exist for that island — same layer set the dashboard
already documents per island (Lakshadweep: coral + boundary only; Canary:
WDPA + boundary only — mangroves and coral are genuinely absent for both,
not a data gap, see dashboard/pages/7_Interactive_Maps.py's per-island notes).

Each layer is a single combined GeoJson call (not one per feature) with a
hover tooltip — the WDPA source polygons in particular carry far more
vertices than a browser needs at this zoom level (Canary's alone is ~1.8M
raw points), so geometries are simplified before rendering. This is a
display-only simplification (shape only, at a tolerance well below anything
visible on screen) — it doesn't touch feature counts, attributes, or any
analysis result, all of which come from the original unsimplified files.

Run from the DOUBLE_JEOPARDY folder:
    python build_ecosystem_buffer_map.py

Produces dashboard/static/{island}_ecosystem_buffer_webmap/index.html for
all five islands — same output path every other interactive map in this
project already uses, so the dashboard and GitHub Pages links don't change.
"""
import os
import geopandas as gpd
import folium

DATA_DIR = "data/ecosystem_buffers"
BOUNDARY_DIR = "data/boundaries"
OUT_DIR = "dashboard/static"

MANGROVE_COLOR = "#e91e8c"   # pink
CORAL_COLOR = "#f5e400"      # bright yellow
WDPA_COLOR = "#38b6e6"       # sky blue outline
BOUNDARY_COLOR = "#2d8a3e"   # green outline

# Simplify tolerance in degrees, per layer — WDPA source polygons are far
# more detailed than anything visible at island scale, mangrove/coral less
# so. See module docstring: display-only, doesn't touch the underlying data.
SIMPLIFY_TOLERANCE = {"mangroves": 0.0001, "coral": 0.0001, "wdpa": 0.0005, "boundary": 0.0003}

# island -> which layers it genuinely has (matches the dashboard's own
# per-island legend already in dashboard/pages/7_Interactive_Maps.py)
ISLAND_LAYERS = {
    "maldives": ["mangroves", "coral", "wdpa"],
    "fiji": ["mangroves", "coral", "wdpa"],
    "seychelles": ["mangroves", "coral", "wdpa"],
    "lakshadweep": ["coral"],
    "canary": ["wdpa"],
}
ISLAND_LABEL = {
    "maldives": "Maldives", "fiji": "Fiji", "seychelles": "Seychelles",
    "lakshadweep": "Lakshadweep", "canary": "Canary Islands",
}
LEGEND_TEXT = {
    "mangroves": (MANGROVE_COLOR, "Mangrove Forests (2020)"),
    "coral": (CORAL_COLOR, "Coral Reefs"),
    "wdpa": (WDPA_COLOR, "Protected Areas (WDPA)"),
}


def name_field(gdf):
    """Whichever name-like column this layer actually has."""
    for col in ("name", "NAME"):
        if col in gdf.columns:
            return col
    return None


def add_layer(m, gdf, color, layer_name, tolerance, fill=True):
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(tolerance, preserve_topology=True)
    gdf = gdf[~gdf.geometry.is_empty]

    tooltip = None
    col = name_field(gdf)
    if col:
        gdf["_label"] = gdf[col].fillna(layer_name)
        tooltip = folium.GeoJsonTooltip(fields=["_label"], aliases=[""])

    folium.GeoJson(
        gdf.__geo_interface__,
        name=f"{layer_name} (n={len(gdf)})",
        style_function=lambda f, c=color, fl=fill: {
            "color": c, "weight": 1.5, "fillColor": c,
            "fillOpacity": 0.45 if fl else 0.0,
        },
        tooltip=tooltip,
    ).add_to(m)


def build_island_map(island):
    layers = ISLAND_LAYERS[island]
    boundary = gpd.read_file(os.path.join(BOUNDARY_DIR, f"{island}_islands.gpkg"))
    minx, miny, maxx, maxy = boundary.total_bounds
    center = [(miny + maxy) / 2, (minx + maxx) / 2]

    m = folium.Map(location=center, tiles="CartoDB positron")
    m.fit_bounds([[miny, minx], [maxy, maxx]])

    add_layer(m, boundary, BOUNDARY_COLOR, "Island Boundary", SIMPLIFY_TOLERANCE["boundary"], fill=False)

    counts = {}
    if "mangroves" in layers:
        gdf = gpd.read_file(os.path.join(DATA_DIR, f"{island}_mangroves_clean.gpkg"))
        add_layer(m, gdf, MANGROVE_COLOR, "Mangrove Forests", SIMPLIFY_TOLERANCE["mangroves"])
        counts["mangroves"] = len(gdf)
    if "coral" in layers:
        gdf = gpd.read_file(os.path.join(DATA_DIR, f"{island}_coral_clean.gpkg"))
        add_layer(m, gdf, CORAL_COLOR, "Coral Reefs", SIMPLIFY_TOLERANCE["coral"])
        counts["coral"] = len(gdf)
    if "wdpa" in layers:
        gdf = gpd.read_file(os.path.join(DATA_DIR, f"{island}_wdpa.gpkg"))
        add_layer(m, gdf, WDPA_COLOR, "Protected Areas (WDPA)", SIMPLIFY_TOLERANCE["wdpa"], fill=False)
        counts["wdpa"] = len(gdf)

    legend_rows = "".join(
        f'<span style="color:{LEGEND_TEXT[l][0]};">■</span> {LEGEND_TEXT[l][1]} ({counts[l]})<br>'
        for l in layers
    )
    legend_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: white; padding: 12px 16px; border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3); font-family: sans-serif; font-size: 13px; max-width: 300px;">
      <b>{ISLAND_LABEL[island]} — Ecosystem Buffer Overview</b><br><br>
      <span style="color:{BOUNDARY_COLOR};">■</span> Island Boundary<br>
      {legend_rows}
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=False).add_to(m)

    island_dir = os.path.join(OUT_DIR, f"{island}_ecosystem_buffer_webmap")
    os.makedirs(island_dir, exist_ok=True)
    out_path = os.path.join(island_dir, "index.html")
    m.save(out_path)
    size_mb = os.path.getsize(out_path) / 1_000_000
    print(f"  Saved: {out_path}  ({counts}, {size_mb:.1f} MB)")
    return {"island": island, **counts}


def main():
    print("Building ecosystem buffer maps...\n")
    results = []
    for island in ISLAND_LAYERS:
        print(f"{island.upper()}:")
        r = build_island_map(island)
        results.append(r)
        print()
    print("Done.")
    for r in results:
        print(f"  {r}")


if __name__ == "__main__":
    main()
