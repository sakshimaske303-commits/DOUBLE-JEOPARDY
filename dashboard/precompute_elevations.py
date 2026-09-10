import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

# Canary Islands' DEM was verified to have 0.0 as a NoData artifact
# (confirmed via QGIS transparency settings and pixel inspection).
# Fiji added after a distributional check found the same signature: 31.3%
# of Fiji settlement points read exactly 0.0m -- a spike, not a gradient,
# on volcanic/mountainous terrain where near-sea-level readings aren't
# geologically expected. map1_slr_fiji.py already excluded Fiji's zeros
# independently; this brings the main pipeline in line with that.
ISLANDS_WITH_ZERO_AS_NODATA = {"canary", "fiji"}

# Update: Maldives and Lakshadweep's original elevation.tif turned out to
# be a severe DEM coverage gap (~99.99% of pixels a flat 0.0), not genuine
# low-lying terrain -- confirmed and fixed in slr_exposure_analysis.py.
# These two now read from the re-downloaded elevation_v2.tif, and use a
# neighborhood-based void check instead of the blanket zero-exclusion used
# for Canary Islands/Fiji above: a 0.0 reading is only dropped if its
# surrounding 5x5-pixel window is also entirely 0.0 (a flat void signature
# no real terrain would produce), since a real settlement on these two
# genuine low-lying atolls CAN legitimately sit at or near 0m.
ISLANDS_WITH_NEIGHBORHOOD_VOID_CHECK = {"maldives", "lakshadweep"}
VOID_HALF_WINDOW = 2  # 5x5 window


def is_void_neighborhood(arr, src, x, y):
    row, col = src.index(x, y)
    r0, r1 = max(0, row - VOID_HALF_WINDOW), min(arr.shape[0], row + VOID_HALF_WINDOW + 1)
    c0, c1 = max(0, col - VOID_HALF_WINDOW), min(arr.shape[1], col + VOID_HALF_WINDOW + 1)
    return bool(np.all(arr[r0:r1, c0:c1] == 0))


all_data = []

for island in ISLANDS:
    gdf = gpd.read_file(f"../data/settlements/{island}_settlements_clean.gpkg")
    elevation_file = f"{island}_elevation_v2.tif" if island in ISLANDS_WITH_NEIGHBORHOOD_VOID_CHECK \
        else f"{island}_elevation.tif"
    with rasterio.open(f"../data/terrain/{elevation_file}") as src:
        coords = [(g.centroid.x, g.centroid.y) for g in gdf.geometry]
        raw_elevations = [val[0] for val in src.sample(coords)]

        if island in ISLANDS_WITH_ZERO_AS_NODATA:
            elevations = [np.nan if e == 0.0 else e for e in raw_elevations]
        elif island in ISLANDS_WITH_NEIGHBORHOOD_VOID_CHECK:
            arr = src.read(1).astype("float64")
            elevations = []
            for e, geom in zip(raw_elevations, gdf.geometry):
                if e == 0.0 and is_void_neighborhood(arr, src, geom.centroid.x, geom.centroid.y):
                    elevations.append(np.nan)
                else:
                    elevations.append(e)
        else:
            elevations = raw_elevations

    for elev in elevations:
        if elev is not None and not np.isnan(elev):
            all_data.append({"island": island.capitalize(), "elevation_m": elev})

df = pd.DataFrame(all_data)
df.to_csv("static/settlement_elevations.csv", index=False)
print(f"Saved {len(df)} rows to static/settlement_elevations.csv")
print(df.groupby("island").size())
