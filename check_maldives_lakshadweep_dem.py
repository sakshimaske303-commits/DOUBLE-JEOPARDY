import geopandas as gpd
import numpy as np
import rasterio

ISLANDS = ["maldives", "lakshadweep"]


def check_island(island):
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"
    elevation_path = f"data/terrain/{island}_elevation.tif"

    gdf = gpd.read_file(settlements_path)

    with rasterio.open(elevation_path) as src:
        print(f"\n{island.upper()}")
        print(f"  DEM nodata value (as declared in the file): {src.nodata}")

        arr = src.read(1).astype("float64")
        nodata = src.nodata
        valid = arr if nodata is None else arr[arr != nodata]
        print(f"  Whole-raster min / max elevation (excluding declared nodata): "
              f"{valid.min():.3f}m / {valid.max():.3f}m")
        print(f"  Fraction of ALL raster pixels reading exactly 0.0: "
              f"{(np.sum(arr == 0).sum() / arr.size) * 100:.2f}%")

        coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
        elevations = [val[0] for val in src.sample(coords)]
        gdf["elevation_m"] = elevations

        total = len(gdf)
        zero_mask = gdf["elevation_m"] == 0.0
        n_zero = int(zero_mask.sum())
        print(f"  Settlement points: {total}")
        print(f"  Exactly 0.0m: {n_zero} ({n_zero / total * 100:.1f}%)")

        # For every settlement reading exactly 0.0, look at the 3x3 pixel
        # neighborhood around it. A genuine low-lying atoll point should sit
        # inside a smooth, mostly-nonzero micro-gradient (0.2m, 0.6m, 1.1m...)
        # even if noisy. A NoData/void artifact tends to be a flat, uniform
        # patch of exact zeros with no internal texture at all.
        all_zero_neighborhood = 0
        mixed_neighborhood = 0
        checked = 0
        for geom in gdf.loc[zero_mask, "geometry"]:
            row, col = src.index(geom.centroid.x, geom.centroid.y)
            r0, r1 = max(0, row - 1), min(arr.shape[0], row + 2)
            c0, c1 = max(0, col - 1), min(arr.shape[1], col + 2)
            window = arr[r0:r1, c0:c1]
            checked += 1
            if np.all(window == 0):
                all_zero_neighborhood += 1
            else:
                mixed_neighborhood += 1

        print(f"  Of those exact-0.0 points, checked {checked} 3x3 neighborhoods:")
        print(f"    entire 3x3 neighborhood is ALSO exactly 0.0 (flat void, artifact-like): "
              f"{all_zero_neighborhood} ({(all_zero_neighborhood / checked * 100) if checked else 0:.1f}%)")
        print(f"    neighborhood has some non-zero variation (looks like real low terrain): "
              f"{mixed_neighborhood} ({(mixed_neighborhood / checked * 100) if checked else 0:.1f}%)")


for island in ISLANDS:
    try:
        check_island(island)
    except Exception as e:
        print(f"{island.upper()}: ERROR - {e}")
