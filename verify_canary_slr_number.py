import geopandas as gpd
import rasterio

gdf = gpd.read_file("data/settlements/canary_settlements_clean.gpkg")

with rasterio.open("data/terrain/canary_elevation.tif") as src:
    coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
    elevations = [val[0] for val in src.sample(coords)]

gdf["elevation_m"] = elevations
gdf["at_risk"] = gdf["elevation_m"] <= 1.0

print("Total settlements:", len(gdf))
print("At risk (<=1m):", gdf["at_risk"].sum())
print("Percentage:", (gdf["at_risk"].sum() / len(gdf)) * 100)
print()
print("Sample elevation values:", gdf["elevation_m"].head(20).tolist())