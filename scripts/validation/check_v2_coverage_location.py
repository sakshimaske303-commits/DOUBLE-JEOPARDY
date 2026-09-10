import numpy as np
import rasterio
from rasterio.transform import xy
import geopandas as gpd

ISLANDS = ["maldives", "lakshadweep"]


def check_island(island):
    dem_path = f"data/terrain/{island}_elevation_v2.tif"
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"

    with rasterio.open(dem_path) as src:
        arr = src.read(1)
        print(f"\n{island.upper()} (v2, freshly downloaded)")
        print(f"  raster shape: {arr.shape}  ({arr.size:,} pixels total)")

        nonzero = np.argwhere(arr != 0)
        print(f"  non-zero pixel count: {len(nonzero):,} "
              f"({len(nonzero) / arr.size * 100:.4f}% of the raster)")

        if len(nonzero) == 0:
            print("  NO non-zero pixels anywhere in this file.")
            return

        gdf = gpd.read_file(settlements_path)
        sample_size = min(20000, len(nonzero))
        idx = np.random.choice(len(nonzero), size=sample_size, replace=False) if len(nonzero) > sample_size else np.arange(len(nonzero))
        nonzero_xy = np.array([xy(src.transform, int(r), int(c)) for r, c in nonzero[idx]])

        distances = []
        elevations = []
        for geom in gdf.geometry:
            x, y = geom.centroid.x, geom.centroid.y
            d = np.sqrt((nonzero_xy[:, 0] - x) ** 2 + (nonzero_xy[:, 1] - y) ** 2)
            distances.append(d.min())
            row, col = src.index(x, y)
            elevations.append(float(arr[row, col]) if 0 <= row < arr.shape[0] and 0 <= col < arr.shape[1] else None)
        distances = np.array(distances)
        elevations = np.array([e for e in elevations if e is not None])

        print(f"  settlement-to-nearest-non-zero-pixel distance (degrees):")
        print(f"    min: {distances.min():.5f}  median: {np.median(distances):.5f}  max: {distances.max():.5f}")
        close_count = int((distances < 0.001).sum())  # roughly within ~100m
        close_1km = int((distances < 0.01).sum())
        print(f"    settlements within ~100m of any non-zero pixel: {close_count} / {len(distances)} "
              f"({close_count / len(distances) * 100:.1f}%)")
        print(f"    settlements within ~1km of any non-zero pixel: {close_1km} / {len(distances)} "
              f"({close_1km / len(distances) * 100:.1f}%)")

        n_zero_reading = int((elevations == 0).sum())
        print(f"  settlements whose OWN pixel still reads exactly 0.0m: {n_zero_reading} / {len(elevations)} "
              f"({n_zero_reading / len(elevations) * 100:.1f}%)  -- was {96 if island=='maldives' else 78}%-ish before")


for island in ISLANDS:
    try:
        check_island(island)
    except Exception as e:
        print(f"{island.upper()}: ERROR - {e}")
