import geopandas as gpd
import os

SHP_PATH = "data/mangroves/extracted_1996/gmw_v3_1996_vec.shp"
OUTPUT_DIR = "data/mangroves/gmw_1996_by_island"

ISLAND_BBOX = {
    "maldives": (72.0, -1.0, 74.0, 7.5),
    "canary": (-19.5, 26.5, -12.0, 30.5),
    "seychelles": (46.0, -10.5, 56.5, -3.5),
    "lakshadweep": (71.5, 8.0, 74.0, 12.5),
    "fiji_west": (177.0, -21.0, 180.0, -12.0),
    "fiji_east": (-180.0, -21.0, -178.0, -12.0),
}


def filter_island(island_name, bbox):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Filtering {island_name}...")

    gdf = gpd.read_file(SHP_PATH, bbox=bbox)

    if len(gdf) > 0:
        output_path = os.path.join(OUTPUT_DIR, f"{island_name}_mangroves_1996.gpkg")
        gdf.to_file(output_path, driver="GPKG")
        print(f"  Saved: {len(gdf)} features -> {output_path}")
    else:
        print(f"  No mangroves found for {island_name}")


def main():
    filter_island("maldives", ISLAND_BBOX["maldives"])
    filter_island("canary", ISLAND_BBOX["canary"])
    filter_island("seychelles", ISLAND_BBOX["seychelles"])
    filter_island("lakshadweep", ISLAND_BBOX["lakshadweep"])
    filter_island("fiji_west", ISLAND_BBOX["fiji_west"])
    filter_island("fiji_east", ISLAND_BBOX["fiji_east"])


if __name__ == "__main__":
    main()