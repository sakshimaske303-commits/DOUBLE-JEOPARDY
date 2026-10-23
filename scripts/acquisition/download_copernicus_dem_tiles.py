"""Download Copernicus DEM GLO-30 tiles for any study island and build a lightweight VRT
mosaic (data/terrain/<island>_elevation_v2.vrt).

Run from the repository root:
    python scripts/acquisition/download_copernicus_dem_tiles.py seychelles lakshadweep
    python scripts/acquisition/download_copernicus_dem_tiles.py --all
"""
import math
import os
import sys
import time
import xml.etree.ElementTree as ET

import requests

BASE_URL = "https://copernicus-dem-30m.s3.amazonaws.com"
RAW_DIR = "data/terrain/raw_tiles"

# (min_lon, min_lat, max_lon, max_lat): settlement extent + ~0.1 deg margin.
# Fiji crosses the antimeridian, so it gets two boxes.
ISLAND_BOUNDS = {
    "maldives": [(72.53, -0.79, 73.86, 7.20)],
    "lakshadweep": [(71.80, 8.18, 73.78, 12.50)],
    "seychelles": [(46.11, -10.32, 56.38, -3.62)],
    "canary": [(-18.25, 27.54, -13.33, 29.51)],
    "fiji": [(176.90, -21.84, 179.999, -12.37), (-180.0, -21.84, -178.30, -12.37)],
}


def tile_name(lat_deg, lon_deg):
    ns = "N" if lat_deg >= 0 else "S"
    ew = "E" if lon_deg >= 0 else "W"
    return f"Copernicus_DSM_COG_10_{ns}{abs(lat_deg):02d}_00_{ew}{abs(lon_deg):03d}_00_DEM"


def tiles_for_bounds(minx, miny, maxx, maxy):
    for lat in range(math.floor(miny), math.floor(maxy) + 1):
        for lon in range(math.floor(minx), math.floor(maxx) + 1):
            yield tile_name(lat, lon)


def download_tile(name, out_dir, max_retries=2):
    out_path = os.path.join(out_dir, f"{name}_DEM.tif")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10_000:
        return out_path, "cached"
    url = f"{BASE_URL}/{name}/{name}.tif"
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, stream=True, timeout=120)
            if r.status_code in (403, 404):
                return None, "no tile (open ocean)"
            r.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
            return out_path, "downloaded"
        except Exception as e:  # network hiccup: retry
            print(f"    {name}: attempt {attempt} failed ({e})")
            time.sleep(3)
    return None, "FAILED"


def build_vrt(tile_paths, vrt_path):
    """Write a GDAL VRT mosaic of the tiles (all share the same 1-arc-second grid
    for |lat| < 50, which covers every study island)."""
    import rasterio

    infos = []
    for p in tile_paths:
        with rasterio.open(p) as src:
            infos.append((p, src.bounds, src.width, src.height, src.res, src.crs, src.dtypes[0], src.nodata))
    res_x, res_y = infos[0][4]
    left = min(i[1].left for i in infos)
    top = max(i[1].top for i in infos)
    right = max(i[1].right for i in infos)
    bottom = min(i[1].bottom for i in infos)
    width = int(round((right - left) / res_x))
    height = int(round((top - bottom) / res_y))
    dtype = {"float32": "Float32", "int16": "Int16"}.get(infos[0][6], "Float32")
    nodata = infos[0][7]

    root = ET.Element("VRTDataset", rasterXSize=str(width), rasterYSize=str(height))
    ET.SubElement(root, "SRS").text = infos[0][5].to_wkt()
    ET.SubElement(root, "GeoTransform").text = f"{left}, {res_x}, 0.0, {top}, 0.0, {-res_y}"
    band = ET.SubElement(root, "VRTRasterBand", dataType=dtype, band="1")
    # Areas with no tile (open ocean) read as this value, so they are reported
    # as "nodata" rather than mistaken for 0 m terrain.
    ET.SubElement(band, "NoDataValue").text = str(nodata if nodata is not None else -32767)
    for p, b, w, h, *_ in infos:
        src = ET.SubElement(band, "SimpleSource")
        ET.SubElement(src, "SourceFilename", relativeToVRT="1").text = os.path.relpath(p, os.path.dirname(vrt_path)).replace("\\", "/")
        ET.SubElement(src, "SourceBand").text = "1"
        ET.SubElement(src, "SrcRect", xOff="0", yOff="0", xSize=str(w), ySize=str(h))
        ET.SubElement(src, "DstRect", xOff=str(int(round((b.left - left) / res_x))),
                      yOff=str(int(round((top - b.top) / res_y))), xSize=str(w), ySize=str(h))
    ET.ElementTree(root).write(vrt_path)
    return width, height


def process(island):
    print(f"\n=== {island.upper()} ===")
    out_dir = os.path.join(RAW_DIR, island)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for box in ISLAND_BOUNDS[island]:
        for name in tiles_for_bounds(*box):
            path, status = download_tile(name, out_dir)
            print(f"  {name}: {status}")
            if path:
                paths.append(path)
    if not paths:
        print("  no tiles; nothing to build")
        return
    if island == "fiji":
        # A single VRT cannot span the antimeridian; build one per side.
        east = [p for p in paths if "_E" in os.path.basename(p)]
        west = [p for p in paths if "_W" in os.path.basename(p)]
        for tag, group in (("", east), ("_west_of_antimeridian", west)):
            if group:
                vrt = f"data/terrain/{island}_elevation_v2{tag}.vrt"
                print(f"  wrote {vrt} {build_vrt(group, vrt)}")
        print("  dem_sampling.py uses the *_west_of_antimeridian.vrt for settlements with longitude < 0.")
    else:
        vrt = f"data/terrain/{island}_elevation_v2.vrt"
        print(f"  wrote {vrt} {build_vrt(paths, vrt)} from {len(paths)} tiles")


if __name__ == "__main__":
    targets = list(ISLAND_BOUNDS) if "--all" in sys.argv or len(sys.argv) == 1 else sys.argv[1:]
    for island in targets:
        process(island)
