import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
import os

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

all_data = []

for island in ISLANDS:
    gdf = gpd.read_file(f"../data/settlements/{island}_settlements_clean.gpkg")
    with rasterio.open(f"../data/terrain/{island}_elevation.tif") as src:
        coords = [(g.centroid.x, g.centroid.y) for g in gdf.geometry]
        raw_elevations = [val[0] for val in src.sample(coords)]
    elevations = [np.nan if e == 0.0 else e for e in raw_elevations]

    for elev in elevations:
        if not np.isnan(elev):
            all_data.append({"island": island.capitalize(), "elevation_m": elev})

df = pd.DataFrame(all_data)
df.to_csv("static/settlement_elevations.csv", index=False)
print(f"Saved {len(df)} rows to static/settlement_elevations.csv")
print(df.groupby("island").size())