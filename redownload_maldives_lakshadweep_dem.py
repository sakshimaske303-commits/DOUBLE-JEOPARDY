import math
import os
import time

import numpy as np
import rasterio
import requests
from rasterio.merge import merge

BASE_URL = "https://copernicus-dem-30m.s3.amazonaws.com"

ISLANDS = {
    "maldives": {
        # from the current (broken) file's own reported bounds
        "bounds": (72.68486111111112, -0.688472069936509, 73.75291664580227, 7.107083333333322),
    },
    "lakshadweep": {
        "bounds": (72.1726388888889, 8.249583333333332, 73.68430555555555, 11.694027777777777),
    },
}

RAW_DIR = "data/terrain/raw_tiles"
os.makedirs(RAW_DIR, exist_ok=True)


def tile_name(lat_deg, lon_deg):
    ns = "N" if lat_deg >= 0 else "S"
    ew = "E" if lon_deg >= 0 else "W"
    lat_str = f"{ns}{abs(lat_deg):02d}_00"
    lon_str = f"{ew}{abs(lon_deg):03d}_00"
    return f"Copernicus_DSM_COG_10_{lat_str}_{lon_str}_DEM"


def tiles_for_bounds(minx, miny, maxx, maxy):
    lat0, lat1 = math.floor(miny), math.floor(maxy)
    lon0, lon1 = math.floor(minx), math.floor(maxx)
    names = []
    for lat in range(lat0, lat1 + 1):
        for lon in range(lon0, lon1 + 1):
            names.append(tile_name(lat, lon))
    return names


def download_tile(name, out_dir, max_retries=2):
    out_path = os.path.join(out_dir, f"{name}_DEM.tif")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000:
        print(f"    already have {name} ({os.path.getsize(out_path) / 1e6:.1f} MB) -- skipping")
        return out_path
    url = f"{BASE_URL}/{name}/{name}.tif"
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, stream=True, timeout=60)
            if r.status_code == 404:
                print(f"    {name}: NOT FOUND (404) -- this tile may not exist (e.g. far offshore)")
                return None
            r.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
            size_mb = os.path.getsize(out_path) / 1e6
            print(f"    {name}: downloaded, {size_mb:.1f} MB")
            return out_path
        except Exception as e:
            print(f"    {name}: attempt {attempt} failed ({e})")
            time.sleep(2)
    print(f"    {name}: GAVE UP after {max_retries} attempts")
    return None


def process_island(island, bounds):
    print(f"\n=== {island.upper()} ===")
    minx, miny, maxx, maxy = bounds
    names = tiles_for_bounds(minx, miny, maxx, maxy)
    print(f"  need {len(names)} tiles: {names}")

    out_dir = os.path.join(RAW_DIR, island)
    os.makedirs(out_dir, exist_ok=True)

    downloaded = []
    for name in names:
        path = download_tile(name, out_dir)
        if path:
            downloaded.append(path)

    print(f"  successfully have {len(downloaded)} / {len(names)} tiles")
    if len(downloaded) < len(names):
        print("  WARNING: not all tiles downloaded -- check the messages above before trusting the merged output.")

    if not downloaded:
        print("  no tiles available, cannot build a mosaic.")
        return

    srcs = [rasterio.open(p) for p in downloaded]
    mosaic, out_transform = merge(srcs)
    meta = srcs[0].meta.copy()
    meta.update({
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_transform,
    })
    for s in srcs:
        s.close()

    out_path = f"data/terrain/{island}_elevation_v2.tif"
    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(mosaic)
    print(f"  wrote merged mosaic: {out_path}")

    # Quick sanity check on the new mosaic
    with rasterio.open(out_path) as src:
        arr = src.read(1)
        nodata = src.nodata
        print(f"  new mosaic nodata value: {nodata}")
        print(f"  new mosaic shape: {arr.shape}")
        zero_pct = (np.sum(arr == 0) / arr.size) * 100
        print(f"  fraction of pixels exactly 0.0 in new mosaic: {zero_pct:.2f}%")
        valid = arr if nodata is None else arr[arr != nodata]
        if valid.size:
            print(f"  new mosaic min/max (excluding nodata): {valid.min():.2f}m / {valid.max():.2f}m")


for island, cfg in ISLANDS.items():
    process_island(island, cfg["bounds"])

print("\nDone. Files written as data/terrain/<island>_elevation_v2.tif -- "
      "the ORIGINAL *_elevation.tif files were NOT touched or overwritten.")
