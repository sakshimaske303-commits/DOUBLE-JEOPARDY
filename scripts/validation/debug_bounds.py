import geopandas as gpd

gdf = gpd.read_file("data/settlements/maldives_settlements_clean.gpkg")
bounds = gdf.total_bounds
print("Maldives bounds:", bounds)

gdf2 = gpd.read_file("data/settlements/canary_settlements_clean.gpkg")
bounds2 = gdf2.total_bounds
print("Canary bounds:", bounds2)