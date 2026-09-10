import geopandas as gpd
import numpy as np
import rasterio
from rasterio.sample import sample_gen
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

SLR_THRESHOLD_M = 1.0  # standard 1-meter sea-level-rise scenario
SENSITIVITY_THRESHOLDS_M = [0.5, 1.0, 1.5]  # robustness check across a range of thresholds

# Canary's DEM returns literal 0.0 at some settlement points that aren't real
# near-sea-level terrain (volcanic, mountainous -- verified against QGIS, see
# data/canary_python_elevations_check.csv). Fiji shows the same signature
# (31.3% of points exactly 0.0m on volcanic/mountainous terrain -- an
# implausible spike, not real near-sea-level readings) and is now excluded
# the same way; see map1_slr_fiji.py, which already treated Fiji's zeros
# as NoData independently of this script. For both islands, EVERY exact-zero
# reading is dropped -- a blanket rule, justified because their terrain is
# volcanic/mountainous and a real settlement at true sea level would be
# geologically implausible in the first place.
ZERO_IS_NODATA = {"canary", "fiji"}

# Maldives and Lakshadweep are different: they're genuine low-lying coral
# atolls, so a real settlement CAN legitimately sit at or near 0.0m -- a
# blanket "drop every exact zero" rule would wrongly delete real at-risk
# points, not just artifacts. The original data/terrain/{island}_elevation.tif
# files for these two turned out to be almost entirely a raster coverage gap
# (99.99% of pixels were exactly 0.0, and settlement points were on average
# nowhere near any real, non-zero pixel) -- confirmed by re-downloading the
# source Copernicus DEM GLO-30 tiles directly from ESA's public archive and
# comparing. The redownloaded files are data/terrain/{island}_elevation_v2.tif.
# Even in the v2 files, a small remaining fraction of settlement points still
# read exactly 0.0m (some source tiles returned 404 -- genuine gaps in the
# public Copernicus archive, not a bug on our end). For those, this script
# tells a real reading apart from a leftover void the same way the DEM
# investigation did: look at the 5x5 pixel neighborhood around the point.
# If every pixel in that neighborhood is also exactly 0.0, it's a flat void
# signature (no real terrain reads perfectly flat across 25 adjacent 30m
# pixels) and the point is excluded as a coverage gap. If the neighborhood
# has real variation, the 0.0m reading is kept as genuine low terrain.
NEIGHBORHOOD_CHECK_NODATA = {"maldives", "lakshadweep"}
NEIGHBORHOOD_HALF_WINDOW = 2  # 2 -> 5x5 window


def is_void_neighborhood(arr, src, x, y):
    row, col = src.index(x, y)
    r0, r1 = max(0, row - NEIGHBORHOOD_HALF_WINDOW), min(arr.shape[0], row + NEIGHBORHOOD_HALF_WINDOW + 1)
    c0, c1 = max(0, col - NEIGHBORHOOD_HALF_WINDOW), min(arr.shape[1], col + NEIGHBORHOOD_HALF_WINDOW + 1)
    window = arr[r0:r1, c0:c1]
    return bool(np.all(window == 0))


def analyze_island(island):
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"
    if island in NEIGHBORHOOD_CHECK_NODATA:
        elevation_path = f"data/terrain/{island}_elevation_v2.tif"
    else:
        elevation_path = f"data/terrain/{island}_elevation.tif"

    gdf = gpd.read_file(settlements_path)
    n_excluded_coverage_gap = 0

    with rasterio.open(elevation_path) as src:
        coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]
        gdf["elevation_m"] = elevations

        if island in ZERO_IS_NODATA:
            keep_mask = gdf["elevation_m"] != 0.0
            n_excluded_coverage_gap = int((~keep_mask).sum())
            gdf = gdf[keep_mask].copy()
        elif island in NEIGHBORHOOD_CHECK_NODATA:
            arr = src.read(1).astype("float64")
            exclude_mask = pd.Series(False, index=gdf.index)
            for idx, geom in zip(gdf.index, gdf.geometry):
                if gdf.loc[idx, "elevation_m"] == 0.0:
                    if is_void_neighborhood(arr, src, geom.centroid.x, geom.centroid.y):
                        exclude_mask.loc[idx] = True
            n_excluded_coverage_gap = int(exclude_mask.sum())
            gdf = gdf[~exclude_mask].copy()

    total = len(gdf)
    at_risk = (gdf["elevation_m"] <= SLR_THRESHOLD_M).sum()
    pct_at_risk = (at_risk / total * 100) if total > 0 else 0

    sensitivity = {}
    for t in SENSITIVITY_THRESHOLDS_M:
        n_risk = (gdf["elevation_m"] <= t).sum()
        sensitivity[f"pct_at_risk_{t}m"] = (n_risk / total * 100) if total > 0 else 0

    print(f"{island.upper()}:")
    if n_excluded_coverage_gap:
        print(f"  Excluded as DEM coverage gap: {n_excluded_coverage_gap}")
    print(f"  Total settlements (after exclusions): {total}")
    print(f"  At risk (<= {SLR_THRESHOLD_M}m elevation): {at_risk} ({pct_at_risk:.1f}%)")
    for t in SENSITIVITY_THRESHOLDS_M:
        print(f"    @ {t}m threshold: {sensitivity[f'pct_at_risk_{t}m']:.2f}%")
    print()

    result = {"island": island, "total": total, "at_risk": at_risk, "pct_at_risk": pct_at_risk,
               "excluded_coverage_gap": n_excluded_coverage_gap}
    result.update(sensitivity)
    return result


def main():
    results = []
    for island in ISLANDS:
        try:
            result = analyze_island(island)
            results.append(result)
        except Exception as e:
            print(f"{island.upper()}: ERROR - {e}\n")

    df = pd.DataFrame(results)
    df.to_csv("data/slr_exposure_summary.csv", index=False)
    print("Saved: data/slr_exposure_summary.csv")


if __name__ == "__main__":
    main()
