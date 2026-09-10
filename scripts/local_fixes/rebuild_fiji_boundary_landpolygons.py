
import os
import geopandas as gpd
from shapely.ops import unary_union

SHAPEFILE_PATH = "data/boundaries/land-polygons-complete-4326/land_polygons.shp"

OUTPUT_PATH = "data/boundaries_v2/fiji_islands_v2.gpkg"
V1_PATH = "data/boundaries/fiji_islands.gpkg"
UTM_EPSG = 32760

WINDOWS = [
    (176.5, -20.7, 180.0, -12.4),
    (-180.0, -20.7, -178.0, -12.4),
]


def _resolve_shapefile_path():
    if os.path.exists(SHAPEFILE_PATH):
        return SHAPEFILE_PATH

    search_root = os.path.dirname(SHAPEFILE_PATH) or "."
    if not os.path.isdir(search_root):
        return None

    found = []
    for root, _dirs, files in os.walk(search_root):
        for f in files:
            if f.lower().endswith(".shp"):
                found.append(os.path.join(root, f))

    if len(found) == 1:
        print(f"NOTE: {SHAPEFILE_PATH} not found, but found exactly 1 .shp file under "
              f"{search_root}: {found[0]} -- using that instead.")
        return found[0]
    elif len(found) > 1:
        print(f"NOTE: {SHAPEFILE_PATH} not found, and found multiple .shp files under "
              f"{search_root}:")
        for f in found:
            print(f"  {f}")
        print("Update SHAPEFILE_PATH at the top of this script to the correct one.")
        return None
    return None


def main():
    shapefile_path = _resolve_shapefile_path()
    if not shapefile_path:
        print(f"ERROR: could not find a .shp file at or near {SHAPEFILE_PATH}.")
        print("Download and unzip https://osmdata.openstreetmap.de/download/land-polygons-complete-4326.zip")
        print("then update SHAPEFILE_PATH at the top of this script to point at the .shp file inside it.")
        return

    pieces = []
    for i, (min_lon, min_lat, max_lon, max_lat) in enumerate(WINDOWS, start=1):
        print(f"Reading window {i}/{len(WINDOWS)}: {(min_lon, min_lat, max_lon, max_lat)}")
        gdf = gpd.read_file(shapefile_path, bbox=(min_lon, min_lat, max_lon, max_lat))
        print(f"  {len(gdf)} land polygon features intersect this window")
        if len(gdf) == 0:
            continue
        clipped = gpd.clip(gdf, (min_lon, min_lat, max_lon, max_lat))
        pieces.append(clipped)

    if not pieces:
        print("No land polygons found in either window -- check SHAPEFILE_PATH and the windows.")
        return

    combined = gpd.GeoDataFrame(pd_concat(pieces), crs=pieces[0].crs)
    dissolved = unary_union(combined.geometry.values)
    result = gpd.GeoDataFrame(geometry=[dissolved], crs=combined.crs).explode(index_parts=False)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    result.to_file(OUTPUT_PATH, driver="GPKG")

    area_km2 = result.to_crs(epsg=UTM_EPSG).geometry.area.sum() / 1e6

    area_v1_km2 = None
    if os.path.exists(V1_PATH):
        try:
            gdf_v1 = gpd.read_file(V1_PATH).to_crs(epsg=UTM_EPSG)
            area_v1_km2 = gdf_v1.geometry.area.sum() / 1e6
        except Exception as e:
            print(f"(could not read v1 file for comparison: {e})")

    print(f"\nSaved: {OUTPUT_PATH}")
    print(f"v1 (old) area: {area_v1_km2:.2f} km2" if area_v1_km2 is not None else "v1 (old) area: n/a")
    print(f"new area (land polygons dataset): {area_km2:.2f} km2  ({len(result)} polygons)")
    if area_v1_km2 is not None:
        if area_km2 < area_v1_km2:
            print(f"*** Still smaller than v1 ({area_v1_km2:.2f} km2) -- if so, send back this "
                  f"output and we'll look at whether the windows need widening. ***")
        else:
            print("OK: at or above v1 -- still confirm against a cited reference area before "
                  "using it in the paper (see REFERENCE_LAND_AREA_KM2 note in the other script).")


def pd_concat(gdfs):
    import pandas as pd
    return pd.concat(gdfs, ignore_index=True)


if __name__ == "__main__":
    main()
