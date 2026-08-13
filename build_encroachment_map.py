"""
DOUBLE_JEOPARDY — Settlement Encroachment interactive map, step 2 of 2.

Takes the NDBI difference rasters produced by download_ndbi_encroachment_raster.py
and turns them into an interactive folium map per island: a continuous red/blue
overlay showing where the NDBI signal moved most between 2016 and 2024.

IMPORTANT — what this map does and doesn't claim: after cloud-masking, a full
year of averaging, and clipping to this project's own validated land boundary,
the remaining NDBI difference on all three islands still had no genuine
absolute scale to it — a fixed threshold like "+/-0.05 = built-up change"
flagged roughly HALF the land area on every island, split close to evenly
between "increase" and "decrease". That even split is the signature of
measurement noise, not real construction (real 8-year urbanization should
skew toward increase, not land 50/50). Rather than keep tuning a threshold
against noise until it produces a number that looks plausible, this map
switches to a percentile-based, relative visualization: it colors the
strongest ~15% of increase and ~15% of decrease pixels *within that island's
own distribution*, and does NOT report a "X km² new built-up" figure, because
that precision isn't supported by this dataset at this resolution. It's a
where-does-change-concentrate visual, not a quantified area estimate. The
validated, already-published built-up change number for this project remains
the bar chart on the Governance & Encroachment dashboard page (built from a
different, aggregate Statistical-API measurement, not this per-pixel one).

Run from the DOUBLE_JEOPARDY folder, after download_ndbi_encroachment_raster.py
has produced data/settlement_encroachment/{island}_ndbi_diff.tif for each island.
Needs: rasterio, geopandas, numpy, matplotlib, folium (pip install if not
already installed). Uses this project's own data/boundaries/*.gpkg island
outlines (already present) to mask the raster to land — see the note at the
top of download_ndbi_encroachment_raster.py for why.

Saves each map as index.html inside its own folder under dashboard/static/,
matching how every other interactive map in this project is already served
via GitHub Pages (see the "Interactive geospatial maps" links in README.md).

Produces:
  dashboard/static/maldives_settlement_encroachment_webmap/index.html
  dashboard/static/seychelles_settlement_encroachment_webmap/index.html
  dashboard/static/fiji_settlement_encroachment_webmap/index.html
"""
import os
import numpy as np
import rasterio
from rasterio.features import rasterize
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import folium

DATA_DIR = "data/settlement_encroachment"
BOUNDARY_DIR = "data/boundaries"
OUT_DIR = "dashboard/static"

# This project's own already-validated island boundary polygons — used here
# to mask the NDBI raster to actual land, the same fixed mask applied to both
# years, rather than a per-scene water/land guess that isn't even consistent
# between the two years being compared.
BOUNDARY_FILE = {
    "maldives": "maldives_islands.gpkg",
    "seychelles": "seychelles_islands.gpkg",
    "fiji": "fiji_islands.gpkg",
}


def load_land_mask(island, transform, shape):
    gdf = gpd.read_file(os.path.join(BOUNDARY_DIR, BOUNDARY_FILE[island]))
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    mask = rasterize(
        [(geom, 1) for geom in gdf.geometry if geom is not None and not geom.is_empty],
        out_shape=shape, transform=transform, fill=0, dtype="uint8",
    )
    return mask.astype(bool)

# Percentile cut used to call out the strongest change pixels, relative to
# that island's own distribution — see the module docstring for why this
# replaced a fixed absolute NDBI threshold.
HOTSPOT_PERCENTILE = 15

ISLANDS = ["maldives", "seychelles", "fiji"]
ISLAND_LABEL = {"maldives": "Maldives", "seychelles": "Seychelles", "fiji": "Fiji"}


def diff_to_rgba(diff, vmax):
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    cmap = plt.get_cmap("RdBu_r")
    rgba = cmap(norm(np.nan_to_num(diff, nan=0.0)))
    alpha = np.where(np.isnan(diff), 0.0, 0.75)
    rgba[..., 3] = alpha
    return rgba


def build_island_map(island):
    diff_path = os.path.join(DATA_DIR, f"{island}_ndbi_diff.tif")
    if not os.path.exists(diff_path):
        print(f"  SKIPPED {island}: {diff_path} not found — run download_ndbi_encroachment_raster.py first.")
        return

    with rasterio.open(diff_path) as src:
        diff = src.read(1)
        bounds = src.bounds
        transform = src.transform

    land_mask = load_land_mask(island, transform, diff.shape)
    diff = np.where(land_mask, diff, np.nan)

    lat_center = (bounds.bottom + bounds.top) / 2
    deg_to_km_lat = 111.0
    deg_to_km_lon = 111.0 * np.cos(np.radians(lat_center))
    px_height_deg = (bounds.top - bounds.bottom) / diff.shape[0]
    px_width_deg = (bounds.right - bounds.left) / diff.shape[1]
    pixel_area_km2 = (px_height_deg * deg_to_km_lat) * (px_width_deg * deg_to_km_lon)

    valid = ~np.isnan(diff)
    total_valid_km2 = valid.sum() * pixel_area_km2
    valid_values = diff[valid]

    if valid_values.size == 0:
        print(f"  SKIPPED {island}: no land pixels found inside the boundary polygon for this raster's extent.")
        return

    hi_cut = np.percentile(valid_values, 100 - HOTSPOT_PERCENTILE)
    lo_cut = np.percentile(valid_values, HOTSPOT_PERCENTILE)
    vmax = float(np.nanmax(np.abs(valid_values))) or 0.01

    # Only render the top/bottom HOTSPOT_PERCENTILE — the noisy middle band
    # is left fully transparent rather than shown in a pale, misleading color.
    display = np.where((diff >= hi_cut) | (diff <= lo_cut), diff, np.nan)
    rgba = diff_to_rgba(display, vmax=vmax)

    center = [lat_center, (bounds.left + bounds.right) / 2]
    m = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron")

    folium.raster_layers.ImageOverlay(
        image=rgba,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        opacity=0.85,
        name="NDBI change 2016→2024",
    ).add_to(m)

    legend_html = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: white; padding: 12px 16px; border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3); font-family: sans-serif; font-size: 13px; max-width: 280px;">
      <b>{ISLAND_LABEL[island]} — NDBI Change, 2016→2024</b><br>
      <span style="color:#b2182b;">■</span> Relative increase &nbsp;
      <span style="color:#2166ac;">■</span> Relative decrease<br><br>
      Exploratory visualization of where the built-up signal shifted most
      within {ISLAND_LABEL[island]} — not a precise area total. See the
      Governance &amp; Encroachment page for this study's validated,
      quantified built-up change figure.
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl().add_to(m)

    island_dir = os.path.join(OUT_DIR, f"{island}_settlement_encroachment_webmap")
    os.makedirs(island_dir, exist_ok=True)
    out_path = os.path.join(island_dir, "index.html")
    m.save(out_path)

    pct_strong_increase = (valid_values >= hi_cut).sum() / valid_values.size * 100
    pct_strong_decrease = (valid_values <= lo_cut).sum() / valid_values.size * 100
    print(f"  Saved: {out_path}")
    print(f"    Land area analyzed: {total_valid_km2:.1f} km²  |  {valid_values.size} land pixels")
    print(f"    Top {HOTSPOT_PERCENTILE}% increase cut: NDBI >= {hi_cut:.4f} ({pct_strong_increase:.1f}% of pixels)")
    print(f"    Top {HOTSPOT_PERCENTILE}% decrease cut: NDBI <= {lo_cut:.4f} ({pct_strong_decrease:.1f}% of pixels)")
    return {"island": island, "area_analyzed_km2": round(total_valid_km2, 1),
            "land_pixels": int(valid_values.size)}


def main():
    print("Building settlement encroachment maps...\n")
    results = []
    for island in ISLANDS:
        print(f"{island.upper()}:")
        r = build_island_map(island)
        if r:
            results.append(r)
        print()
    print("Done.")
    if results:
        print("Summary:")
        for r in results:
            print(f"  {r['island']:<12} {r['area_analyzed_km2']} km² land analyzed ({r['land_pixels']} pixels)")


if __name__ == "__main__":
    main()
