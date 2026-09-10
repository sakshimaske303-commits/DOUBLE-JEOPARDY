import numpy as np
import rasterio
from rasterio.transform import xy
import geopandas as gpd

ISLANDS = ["maldives", "lakshadweep"]


def check_island(island):
    dem_path = f"data/terrain/{island}_elevation.tif"
    settlements_path = f"data/settlements/{island}_settlements_clean.gpkg"

    with rasterio.open(dem_path) as src:
        arr = src.read(1)
        print(f"\n{island.upper()}")
        print(f"  raster shape: {arr.shape}  ({arr.size:,} pixels total)")
        print(f"  raster bounds: {src.bounds}")

        nonzero = np.argwhere(arr != 0)
        print(f"  non-zero pixel count: {len(nonzero):,} "
              f"({len(nonzero) / arr.size * 100:.4f}% of the raster)")

        if len(nonzero) == 0:
            print("  NO non-zero pixels anywhere in this file -- there is no usable elevation data at all.")
            return

        rows, cols = nonzero[:, 0], nonzero[:, 1]
        print(f"  non-zero pixels span rows {rows.min()}-{rows.max()} of {arr.shape[0]}, "
              f"cols {cols.min()}-{cols.max()} of {arr.shape[1]}")

        top_left_xy = xy(src.transform, int(rows.min()), int(cols.min()))
        bottom_right_xy = xy(src.transform, int(rows.max()), int(cols.max()))
        print(f"  in map coordinates: roughly {top_left_xy} to {bottom_right_xy}")
        sample_n = min(10, len(rows))
        print(f"  sample of the actual non-zero values found: "
              f"{[round(float(arr[rows[i], cols[i]]), 2) for i in range(sample_n)]}")

        # Now check: how close is each real settlement point to the nearest
        # non-zero pixel? If settlements sit far from any non-zero pixel,
        # the "real" elevation data in this file doesn't cover where people
        # actually live at all.
        gdf = gpd.read_file(settlements_path)
        nonzero_xy = np.array([xy(src.transform, int(r), int(c)) for r, c in nonzero[:min(5000, len(nonzero))]])

        distances = []
        for geom in gdf.geometry:
            x, y = geom.centroid.x, geom.centroid.y
            d = np.sqrt((nonzero_xy[:, 0] - x) ** 2 + (nonzero_xy[:, 1] - y) ** 2)
            distances.append(d.min())
        distances = np.array(distances)

        print(f"  settlement-to-nearest-non-zero-pixel distance (degrees):")
        print(f"    min: {distances.min():.4f}  median: {np.median(distances):.4f}  max: {distances.max():.4f}")
        close_count = int((distances < 0.01).sum())  # roughly within ~1km
        print(f"    settlements within ~1km of any non-zero pixel: {close_count} / {len(distances)} "
              f"({close_count / len(distances) * 100:.1f}%)")


for island in ISLANDS:
    try:
        check_island(island)
    except Exception as e:
        print(f"{island.upper()}: ERROR - {e}")
