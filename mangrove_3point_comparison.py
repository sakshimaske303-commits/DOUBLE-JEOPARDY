import geopandas as gpd

islands = ["maldives", "seychelles", "fiji"]
years = ["1996", "2010", "2020"]

for island in islands:
    print(f"{island.upper()}:")
    areas = {}
    for year in years:
        gdf = gpd.read_file(f"data/mangroves/gmw_{year}_by_island/{island}_mangroves_{year}.gpkg")
        gdf_proj = gdf.to_crs("EPSG:6933")
        area_km2 = gdf_proj.geometry.area.sum() / 1_000_000
        areas[year] = area_km2
        print(f"  {year}: {area_km2:.2f} km2")

    change_1996_2020 = areas["2020"] - areas["1996"]
    pct_change = (change_1996_2020 / areas["1996"]) * 100 if areas["1996"] > 0 else 0
    print(f"  Net change (1996-2020): {change_1996_2020:+.2f} km2 ({pct_change:+.1f}%)")
    print()