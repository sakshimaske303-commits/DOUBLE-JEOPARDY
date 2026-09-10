"""Per-settlement lon/lat/elevation export feeding build_slr_exposure_map.py;
same 0.0-as-bad-DEM-read logic as precompute_elevations.py (Canary + Fiji), plus
the same 5x5-neighborhood void check used in slr_exposure_analysis.py for
Maldives and Lakshadweep, whose original elevation.tif files turned out to be
a severe DEM coverage gap (~99.99% flat 0.0) rather than genuine low-lying
terrain. Those two now read from the re-downloaded elevation_v2.tif.
"""
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
import os

ISLANDS = ["maldives", "seychelles", "fiji", "lakshadweep"]  # canary already done
SLR_THRESHOLD_M = 1.0
ZERO_IS_NODATA = {"canary", "fiji"}  # fiji: same zero-spike signature as canary, see precompute_elevations.py
VOID_CHECK_ISLANDS = {"maldives", "lakshadweep"}
VOID_HALF_WINDOW = 2  # 5x5 window
OUT_DIR = "data/settlement_elevations_full"


def is_void_neighborhood(arr, src, x, y):
    row, col = src.index(x, y)
    r0, r1 = max(0, row - VOID_HALF_WINDOW), min(arr.shape[0], row + VOID_HALF_WINDOW + 1)
    c0, c1 = max(0, col - VOID_HALF_WINDOW), min(arr.shape[1], col + VOID_HALF_WINDOW + 1)
    return bool(np.all(arr[r0:r1, c0:c1] == 0))


def export_island(island):
    gdf = gpd.read_file(f"data/settlements/{island}_settlements_clean.gpkg")
    elevation_file = f"{island}_elevation_v2.tif" if island in VOID_CHECK_ISLANDS \
        else f"{island}_elevation.tif"
    with rasterio.open(f"data/terrain/{elevation_file}") as src:
        coords = [(g.x, g.y) for g in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]

        if island in VOID_CHECK_ISLANDS:
            arr = src.read(1).astype("float64")
            is_void = [
                e == 0.0 and is_void_neighborhood(arr, src, c[0], c[1])
                for e, c in zip(elevations, coords)
            ]
        else:
            is_void = [False] * len(elevations)

    out = pd.DataFrame({
        "name": gdf["name"].fillna("Unnamed settlement"),
        "place": gdf["place"] if "place" in gdf.columns else "",
        "lon": [c[0] for c in coords],
        "lat": [c[1] for c in coords],
        "elevation_m": elevations,
        "_is_void": is_void,
    })

    if island in ZERO_IS_NODATA:
        out = out[out["elevation_m"] != 0.0].copy()
    elif island in VOID_CHECK_ISLANDS:
        n_excluded = int(out["_is_void"].sum())
        out = out[~out["_is_void"]].copy()
        if n_excluded:
            print(f"  ({island}: excluded {n_excluded} settlements sitting on a detected DEM coverage-gap patch)")

    out = out.drop(columns=["_is_void"])
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
