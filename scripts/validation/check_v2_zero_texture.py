import geopandas as gpd
import numpy as np
import rasterio

ISLANDS = ["maldives", "lakshadweep"]


def check_island(island):
    dem_path = f"data/terrain/{island}_elevation_v2.tif"
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"

    gdf = gpd.read_file(settlements_path)

    with rasterio.open(dem_path) as src:
        arr = src.read(1).astype("float64")
        print(f"\n{island.upper()} (v2)")

        coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]
        gdf["elevation_m"] = elevations

        total = len(gdf)
        zero_mask = gdf["elevation_m"] == 0.0
        n_zero = int(zero_mask.sum())
        print(f"  settlement points: {total}, exactly 0.0m: {n_zero} ({n_zero/total*100:.1f}%)")

        all_zero_neighborhood = 0
        mixed_neighborhood = 0
        checked = 0
        for geom in gdf.loc[zero_mask, "geometry"]:
            row, col = src.index(geom.centroid.x, geom.centroid.y)
            r0, r1 = max(0, row - 2), min(arr.shape[0], row + 3)
            c0, c1 = max(0, col - 2), min(arr.shape[1], col + 3)
            window = arr[r0:r1, c0:c1]  # 5x5 this time, wider net
            checked += 1
            if np.all(window == 0):
                all_zero_neighborhood += 1
            else:
                mixed_neighborhood += 1

        print(f"  of those exact-0.0 points, checked {checked} 5x5 neighborhoods:")
        print(f"    entirely 0.0 (still looks void/artifact-like): {all_zero_neighborhood} "
              f"({(all_zero_neighborhood/checked*100) if checked else 0:.1f}%)")
        print(f"    has non-zero variation nearby (looks like real low terrain): {mixed_neighborhood} "
              f"({(mixed_neighborhood/checked*100) if checked else 0:.1f}%)")


for island in ISLANDS:
    try:
        check_island(island)
    except Exception as e:
        print(f"{island.upper()}: ERROR - {e}")
