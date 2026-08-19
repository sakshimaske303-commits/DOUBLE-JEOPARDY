"""Per-settlement lon/lat/elevation export feeding build_slr_exposure_map.py;
same Canary-only 0.0-as-bad-DEM-read logic as precompute_elevations.py.
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
