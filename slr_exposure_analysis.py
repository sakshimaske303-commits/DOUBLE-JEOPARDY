import geopandas as gpd
import numpy as np
import rasterio
from rasterio.sample import sample_gen
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

SLR_THRESHOLD_M = 1.0  # standard 1-meter sea-level-rise scenario
SENSITIVITY_THRESHOLDS_M = [0.5, 1.0, 1.5]  # robustness check across a range of thresholds

# Canary's DEM returns a literal 0.0 at a cluster of settlement points that
# don't correspond to real near-sea-level terrain (Canary is volcanic and
# mountainous — verified independently against QGIS's own raster sampling,
# see data/canary_python_elevations_check.csv). Every other island's exact-zero
# readings are genuine low-lying/coastal elevation and are kept as real data.
ZERO_IS_NODATA = {"canary"}


def analyze_island(island):
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"
    elevation_path = f"data/terrain/{island}_elevation.tif"

    gdf = gpd.read_file(settlements_path)

    with rasterio.open(elevation_path) as src:
        coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]

    gdf["elevation_m"] = elevations

    if island in ZERO_IS_NODATA:
        gdf = gdf[gdf["elevation_m"] != 0.0].copy()

    total = len(gdf)
    at_risk = (gdf["elevation_m"] <= SLR_THRESHOLD_M).sum()
    pct_at_risk = (at_risk / total * 100) if total > 0 else 0

    sensitivity = {}
    for t in SENSITIVITY_THRESHOLDS_M:
        n_risk = (gdf["elevation_m"] <= t).sum()
        sensitivity[f"pct_at_risk_{t}m"] = (n_risk / total * 100) if total > 0 else 0

    print(f"{island.upper()}:")
    print(f"  Total settlements: {total}")
    print(f"  At risk (<= {SLR_THRESHOLD_M}m elevation): {at_risk} ({pct_at_risk:.1f}%)")
    for t in SENSITIVITY_THRESHOLDS_M:
        print(f"    @ {t}m threshold: {sensitivity[f'pct_at_risk_{t}m']:.2f}%")
    print()

    result = {"island": island, "total": total, "at_risk": at_risk, "pct_at_risk": pct_at_risk}
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