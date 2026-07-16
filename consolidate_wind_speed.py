import geopandas as gpd
import os

folder = "data/cyclone_tracks"

WIND_PRIORITY = ["WMO_WIND", "USA_WIND", "REU_WIND", "BOM_WIND", "TOK_WIND", "CMA_WIND", "HKO_WIND"]

FILES = ["maldives_cyclone_tracks.shp.gpkg", "fiji_cyclone_tracks.shp.gpkg",
         "seychelles_cyclone_tracks.shp.gpkg", "lakshadweep_cyclone_tracks.shp.gpkg"]


def consolidate_wind(filename):
    filepath = os.path.join(folder, filename)
    gdf = gpd.read_file(filepath)

    # Take the first non-null wind speed across all available agencies, in priority order
    gdf["WIND_CONSOLIDATED"] = gdf[WIND_PRIORITY].bfill(axis=1).iloc[:, 0]

    valid_count = gdf["WIND_CONSOLIDATED"].notna().sum()
    print(f"{filename}: {len(gdf)} total, {valid_count} with consolidated wind speed")

    keep_cols = ["SID", "SEASON", "NAME", "ISO_TIME", "NATURE", "LAT", "LON",
                 "WIND_CONSOLIDATED", "DIST2LAND", "LANDFALL", "geometry"]
    gdf_final = gdf[[c for c in keep_cols if c in gdf.columns]]

    output_path = filepath.replace(".shp.gpkg", "_final.gpkg")
    gdf_final.to_file(output_path, driver="GPKG")
    print(f"  Saved: {output_path}")


def main():
    for f in FILES:
        consolidate_wind(f)


if __name__ == "__main__":
    main()