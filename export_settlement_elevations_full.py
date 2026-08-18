"""One-time export: per-settlement lon/lat/elevation for the SLR exposure maps.

Companion to build_slr_exposure_map.py — that script only needs a small CSV
per island, but sampling the elevation rasters themselves needs the actual
data/terrain/*.tif files, which are too large to move off this machine. Run
this here once per island (or all at once, it's quick — rasterio only reads
the pixels under each settlement point, not the full raster into memory).

Same sampling logic as precompute_elevations.py / slr_exposure_analysis.py:
exact 0.0 elevation is only treated as a bad DEM read for Canary (verified
against QGIS's own raster sampling, see data/canary_python_elevations_check.csv);
every other island's 0m readings are genuine low-lying/coastal elevation and
are kept.

Run from the DOUBLE_JEOPARDY folder:
    python export_settlement_elevations_full.py

Writes data/settlement_elevations_full/{island}.csv for maldives, fiji,
seychelles, lakshadweep (canary.csv already exists, built from the earlier
QGIS-comparison CSV). build_slr_exposure_map.py picks these up automatically
next run — just push the new CSVs to the repo, no other step needed.
"""
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
import os

ISLANDS = ["maldives", "seychelles", "fiji", "lakshadweep"]  # canary already done
SLR_THRESHOLD_M = 1.0
ZERO_IS_NODATA = {"canary"}  # kept here for parity, doesn't affect this list
OUT_DIR = "data/settlement_elevations_full"


def export_island(island):
    gdf = gpd.read_file(f"data/settlements/{island}_settlements_clean.gpkg")
    with rasterio.open(f"data/terrain/{island}_elevation.tif") as src:
        coords = [(g.x, g.y) for g in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]

    out = pd.DataFrame({
        "name": gdf["name"].fillna("Unnamed settlement"),
        "place": gdf["place"] if "place" in gdf.columns else "",
        "lon": [c[0] for c in coords],
        "lat": [c[1] for c in coords],
        "elevation_m": elevations,
    })

    if island in ZERO_IS_NODATA:
        out = out[out["elevation_m"] != 0.0].copy()

    out["at_risk"] = out["elevation_m"] <= SLR_THRESHOLD_M

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{island}.csv")
    out.to_csv(out_path, index=False)
    at_risk_pct = out["at_risk"].mean() * 100
    print(f"{island}: {len(out)} settlements, {out['at_risk'].sum()} at risk ({at_risk_pct:.1f}%) -> {out_path}")


def main():
    for island in ISLANDS:
        try:
            export_island(island)
        except FileNotFoundError as e:
            print(f"{island}: SKIPPED - {e}")


if __name__ == "__main__":
    main()
