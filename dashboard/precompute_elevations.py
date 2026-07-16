import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

# Only Canary Islands' DEM was verified to have 0.0 as a NoData artifact
# (confirmed via QGIS transparency settings and pixel inspection).
# For other islands, 0.0 may represent genuine near-sea-level elevation
# and should NOT be treated as missing data.
ISLANDS_WITH_ZERO_AS_NODATA = {"canary"}

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