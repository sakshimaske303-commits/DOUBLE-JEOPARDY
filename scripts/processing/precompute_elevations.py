import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
import os

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

# Canary Islands' DEM was verified to have 0.0 as a NoData artifact
# (confirmed via QGIS transparency settings and pixel inspection).
# Fiji added after a distributional check found the same signature: 31.3%
# of Fiji settlement points read exactly 0.0m -- a spike, not a gradient,
# on volcanic/mountainous terrain where near-sea-level readings aren't
# geologically expected (see DJ_Development_Log.md, later entry, for the
# full check). map1_slr_fiji.py already excluded Fiji's zeros
# independently; this brings the main pipeline in line with that.
# Maldives (99.0% zero) and Lakshadweep (77.8% zero) show a similar
# zero-spike but are NOT added here: both are low-lying coral atolls where
# genuine near-sea-level terrain across most settlements is the expected
# geology, not an anomaly, so the same statistical flag doesn't carry the
# same evidentiary weight there. Flagged as an open item for a future
# QGIS-level check, not treated as confirmed either way.
ISLANDS_WITH_ZERO_AS_NODATA = {"canary", "fiji"}

all_data = []

for island in ISLANDS:
    gdf = gpd.read_file(f"../data/settlements/{island}_settlements_clean.gpkg")
    with rasterio.open(f"../data/terrain/{island}_elevation.tif") as src:
        coords = [(g.centroid.x, g.centroid.y) for g in gdf.geometry]
        raw_elevations = [val[0] for val in src.sample(coords)]

    if island in ISLANDS_WITH_ZERO_AS_NODATA:
        elevations = [np.nan if e == 0.0 else e for e in raw_elevations]
    else:
        elevations = raw_elevations

    for elev in elevations:
        if elev is not None and not np.isnan(elev):
            all_data.append({"island": island.capitalize(), "elevation_m": elev})

df = pd.DataFrame(all_data)
df.to_csv("static/settlement_elevations.csv", index=False)
print(f"Saved {len(df)} rows to static/settlement_elevations.csv")
print(df.groupby("island").size())