import geopandas as gpd
import os

RAW_BASE = r"D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\New folder\DIGITAL_TWIN_ISLANDS\02_data_raw"
OUTPUT_DIR = "data/protected_areas_wdpa"

# Approximate bounding boxes per island (min_lon, min_lat, max_lon, max_lat)
ISLAND_BBOX = {
    "maldives": (72.0, -1.0, 74.0, 7.5),
    "canary": (-18.5, 27.5, -13.0, 29.5),
    "seychelles": (46.0, -10.5, 56.5, -3.5),
    "lakshadweep": (71.5, 8.0, 74.0, 12.5),
    "fiji_west": (177.0, -21.0, 180.0, -12.0),
    "fiji_east": (-180.0, -21.0, -178.0, -12.0),  # Fiji crosses antimeridian
}

PARTS = ["WDPA_extracted_0", "WDPA_extracted_1", "WDPA_extracted_2"]


def filter_polygons_for_island(island_name, bbox):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_matches = []

    for part in PARTS:
        shp_path = os.path.join(RAW_BASE, part, "WDPA_Jun2026_Public_shp-polygons.shp")
        print(f"  Reading {part} for {island_name} (bbox filter, memory-efficient)...")

        try:
            gdf = gpd.read_file(shp_path, bbox=bbox)
            if len(gdf) > 0:
                all_matches.append(gdf)
                print(f"    Found {len(gdf)} matching features")
        except Exception as e:
            print(f"    Error reading {part}: {e}")

    if all_matches:
        import pandas as pd
        combined = gpd.GeoDataFrame(pd.concat(all_matches, ignore_index=True), crs=all_matches[0].crs)
        output_path = os.path.join(OUTPUT_DIR, f"{island_name}_wdpa.gpkg")
        combined.to_file(output_path, driver="GPKG")
        print(f"  Saved: {output_path} ({len(combined)} total features)")
    else:
        print(f"  No WDPA protected areas found for {island_name}")


def main():
    filter_polygons_for_island("maldives", ISLAND_BBOX["maldives"])
    filter_polygons_for_island("canary", ISLAND_BBOX["canary"])
    filter_polygons_for_island("seychelles", ISLAND_BBOX["seychelles"])
    filter_polygons_for_island("lakshadweep", ISLAND_BBOX["lakshadweep"])
    filter_polygons_for_island("fiji_west", ISLAND_BBOX["fiji_west"])
    filter_polygons_for_island("fiji_east", ISLAND_BBOX["fiji_east"])


if __name__ == "__main__":
    main()