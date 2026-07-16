import geopandas as gpd
import rasterio
import os
import numpy as np

BASE = "data"

# Expected approximate bounding boxes per island (min_lon, min_lat, max_lon, max_lat)
ISLAND_BOUNDS = {
    "maldives": (72.5, -0.7, 73.7, 7.1),
    "canary": (-18.2, 27.6, -13.3, 29.5),
    "seychelles": (46.2, -10.2, 56.0, -3.7),
    "fiji": (176.0, -21.0, -178.0, -12.0),  # crosses antimeridian
    "lakshadweep": (71.5, 8.0, 74.0, 12.5),
}


def check_vector(filepath, island):
    try:
        gdf = gpd.read_file(filepath)
        rows = len(gdf)
        crs = gdf.crs
        bounds = gdf.total_bounds
        dupes = gdf.duplicated(subset="geometry").sum()
        nulls = gdf.geometry.isnull().sum()

        print(f"  Rows: {rows} | CRS: {crs} | Duplicate geoms: {dupes} | Null geoms: {nulls}")
        print(f"  Bounds: {bounds}")

        if island in ISLAND_BOUNDS and rows > 0:
            exp = ISLAND_BOUNDS[island]
            minx, miny, maxx, maxy = bounds
            in_range = (exp[0] - 2 <= minx <= exp[2] + 2) or (exp[0] - 2 <= maxx <= exp[2] + 2)
            if not in_range:
                print(f"  ⚠️ WARNING: bounds don't look like they match {island}!")

    except Exception as e:
        print(f"  ❌ ERROR reading file: {e}")


def check_raster(filepath, island):
    try:
        with rasterio.open(filepath) as src:
            crs = src.crs
            bounds = src.bounds
            data = src.read(1, masked=True)
            print(f"  CRS: {crs} | Shape: {src.shape}")
            print(f"  Bounds: {bounds}")
            print(f"  Min: {data.min():.2f} | Max: {data.max():.2f} | Mean: {data.mean():.2f} | NoData%: {(data.mask.sum()/data.size)*100:.1f}%")
    except Exception as e:
        print(f"  ❌ ERROR reading file: {e}")


def scan_folder(folder_path, is_raster=False):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    for fname in sorted(os.listdir(folder_path)):
        filepath = os.path.join(folder_path, fname)
        island = next((i for i in ISLAND_BOUNDS if i in fname.lower()), "unknown")

        print(f"\n📂 {fname} (island: {island})")
        if fname.endswith(".tif"):
            check_raster(filepath, island)
        elif fname.endswith(".gpkg"):
            check_vector(filepath, island)


def main():
    print("=" * 60)
    print("SETTLEMENTS")
    print("=" * 60)
    scan_folder(os.path.join(BASE, "settlements"))

    print("\n" + "=" * 60)
    print("ECOSYSTEM BUFFERS")
    print("=" * 60)
    scan_folder(os.path.join(BASE, "ecosystem_buffers"))

    print("\n" + "=" * 60)
    print("TERRAIN")
    print("=" * 60)
    scan_folder(os.path.join(BASE, "terrain"))

    print("\n" + "=" * 60)
    print("POPULATION")
    print("=" * 60)
    scan_folder(os.path.join(BASE, "population"))

    print("\n" + "=" * 60)
    print("BOUNDARIES")
    print("=" * 60)
    scan_folder(os.path.join(BASE, "boundaries"))


if __name__ == "__main__":
    main()