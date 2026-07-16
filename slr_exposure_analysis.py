import geopandas as gpd
import rasterio
from rasterio.sample import sample_gen
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

SLR_THRESHOLD_M = 1.0  # standard 1-meter sea-level-rise scenario


def analyze_island(island):
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"
    elevation_path = f"data/terrain/{island}_elevation.tif"

    gdf = gpd.read_file(settlements_path)

    with rasterio.open(elevation_path) as src:
        coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]

    gdf["elevation_m"] = elevations

    total = len(gdf)
    at_risk = (gdf["elevation_m"] <= SLR_THRESHOLD_M).sum()
    pct_at_risk = (at_risk / total * 100) if total > 0 else 0

    print(f"{island.upper()}:")
    print(f"  Total settlements: {total}")
    print(f"  At risk (<= {SLR_THRESHOLD_M}m elevation): {at_risk} ({pct_at_risk:.1f}%)")
    print()

    return {"island": island, "total": total, "at_risk": at_risk, "pct_at_risk": pct_at_risk}


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