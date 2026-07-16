import geopandas as gpd
import rasterio

gdf = gpd.read_file("data/settlements/canary_settlements_clean.gpkg")

with rasterio.open("data/terrain/canary_elevation.tif") as src:
    coords = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
    elevations = [val[0] for val in src.sample(coords)]

gdf["elevation_m"] = elevations
gdf["at_risk"] = gdf["elevation_m"] <= 1.0

# Export first coordinate + elevation pairs so they can be directly
# cross-checked against QGIS's SAMPLE_1 values for the same points
gdf["lon"] = gdf.geometry.centroid.x
gdf["lat"] = gdf.geometry.centroid.y

export_df = gdf[["lon", "lat", "elevation_m", "at_risk"]].reset_index()
export_df.to_csv("data/canary_python_elevations_check.csv", index=False)
print("Saved: data/canary_python_elevations_check.csv")
print("First 10 rows:")
print(export_df.head(10))