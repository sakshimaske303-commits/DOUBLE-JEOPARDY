import geopandas as gpd

for name, path, utm_epsg in [
    ("Maldives", "data/boundaries/maldives_islands.gpkg", 32640),
    ("Lakshadweep", "data/boundaries/lakshadweep_islands.gpkg", 32643),
]:
    gdf = gpd.read_file(path)
    gdf_m = gdf.to_crs(epsg=utm_epsg)  # reproject to a metric UTM CRS to measure real area
    areas_km2 = gdf_m.geometry.area / 1e6
    print(f"\n{name}")
    print(f"  features: {len(gdf)}")
    print(f"  TOTAL polygon land area: {areas_km2.sum():.2f} km2")
    print(f"  largest 5 features (km2): {sorted(areas_km2, reverse=True)[:5]}")
    print(f"  smallest 5 features (km2): {sorted(areas_km2)[:5]}")
