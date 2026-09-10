import geopandas as gpd
import os

folder = "data/ecosystem_buffers"

KEEP_COLUMNS = ["NAME", "DESIG", "DESIG_ENG", "IUCN_CAT", "STATUS", "STATUS_YR", "REP_AREA", "GIS_AREA", "geometry"]

WDPA_FILES = ["maldives_wdpa.gpkg", "canary_wdpa.gpkg", "seychelles_wdpa.gpkg", "fiji_wdpa.gpkg"]


def clean_wdpa_file(filename):
    filepath = os.path.join(folder, filename)
    gdf = gpd.read_file(filepath, on_invalid="ignore")
    print(f"\n{filename}: {len(gdf)} rows, {len(gdf.columns)} columns (before cleanup)")

    before_drop = len(gdf)
    gdf = gdf[gdf.geometry.notnull()]
    dropped = before_drop - len(gdf)
    if dropped > 0:
        print(f"  Dropped {dropped} row(s) with invalid geometry")

    cols_to_keep = [c for c in KEEP_COLUMNS if c in gdf.columns]
    gdf_clean = gdf[cols_to_keep]

    gdf_clean.to_file(filepath, driver="GPKG")
    print(f"  Cleaned and overwritten: {filename} ({len(gdf_clean.columns)} columns, {len(gdf_clean)} rows)")


def main():
    for filename in WDPA_FILES:
        clean_wdpa_file(filename)


if __name__ == "__main__":
    main()