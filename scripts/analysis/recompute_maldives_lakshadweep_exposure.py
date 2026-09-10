import geopandas as gpd
import numpy as np
import rasterio
import pandas as pd

ISLANDS = ["maldives", "lakshadweep"]
THRESHOLDS = [0.5, 1.0, 1.5]


def recompute(island):
    dem_path = f"data/terrain/{island}_elevation_v2.tif"
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"

    gdf = gpd.read_file(settlements_path)

    with rasterio.open(dem_path) as src:
        arr = src.read(1).astype("float64")

        coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]
        gdf["elevation_m"] = elevations

        # Same NoData-exclusion logic already used for Canary/Fiji, applied
        # here with an explicit check: a settlement reading exactly 0.0m is
        # excluded (treated as "no elevation data available") ONLY if its
        # 5x5 neighborhood is also entirely 0.0 -- i.e. it's sitting in a
        # real coverage gap, not on genuinely low real terrain.
        exclude_mask = pd.Series(False, index=gdf.index)
        for idx, geom in zip(gdf.index, gdf.geometry):
            elev = gdf.loc[idx, "elevation_m"]
            if elev == 0.0:
                row, col = src.index(geom.centroid.x, geom.centroid.y)
                r0, r1 = max(0, row - 2), min(arr.shape[0], row + 3)
                c0, c1 = max(0, col - 2), min(arr.shape[1], col + 3)
                window = arr[r0:r1, c0:c1]
                if np.all(window == 0):
                    exclude_mask.loc[idx] = True

    total_before = len(gdf)
    n_excluded = int(exclude_mask.sum())
    gdf_valid = gdf.loc[~exclude_mask].copy()
    total_valid = len(gdf_valid)

    print(f"\n{island.upper()}")
    print(f"  total settlements: {total_before}")
    print(f"  excluded as no-data-coverage-gap: {n_excluded} ({n_excluded/total_before*100:.1f}%)")
    print(f"  valid settlements used for exposure calc: {total_valid}")

    for t in THRESHOLDS:
        at_risk = (gdf_valid["elevation_m"] <= t).sum()
        pct = at_risk / total_valid * 100 if total_valid else float("nan")
        marker = "  <-- used in this study" if t == 1.0 else ""
        print(f"    @ {t}m threshold: {at_risk} / {total_valid} at risk = {pct:.1f}%{marker}")

    return {
        "island": island,
        "total_settlements": total_before,
        "excluded_no_data": n_excluded,
        "valid_settlements": total_valid,
        **{f"pct_at_risk_{t}m": (gdf_valid["elevation_m"] <= t).sum() / total_valid * 100 if total_valid else float("nan")
           for t in THRESHOLDS},
    }


results = [recompute(island) for island in ISLANDS]
pd.DataFrame(results).to_csv("data/slr_exposure_summary_maldives_lakshadweep_v2.csv", index=False)
print("\nSaved: data/slr_exposure_summary_maldives_lakshadweep_v2.csv")
