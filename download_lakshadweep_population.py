"""
Download + clip Lakshadweep population data

Lakshadweep population was skipped originally because the only version
found meant downloading a population raster for the whole of India. Found
a smaller option since — WorldPop's constrained, UN-adjusted 2020 India
raster is ~466MB instead of multiple GB. This downloads it once, clips it
straight down to the Lakshadweep bounding box (from
data/boundaries/lakshadweep_islands.gpkg, same as the rest of the
pipeline), saves the small clipped file, then deletes the large source so
it isn't sitting around taking up space.

Run from the project root: python download_lakshadweep_population.py
Downloads ~466MB, then writes data/population/lakshadweep_population_clean.tif.
Re-run population_weighted_exposure.py after — Lakshadweep gets picked up
automatically.

Needs: requests, rasterio, geopandas
"""

import os
import requests
import rasterio
from rasterio.windows import from_bounds
import geopandas as gpd

WORLDPOP_URL = "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/BSGM/IND/ind_ppp_2020_UNadj_constrained.tif"
TEMP_DOWNLOAD_PATH = "data/population/_temp_india_population.tif"
BOUNDARY_PATH = "data/boundaries/lakshadweep_islands.gpkg"
OUTPUT_PATH = "data/population/lakshadweep_population_clean.tif"

# Small buffer (in degrees) added around Lakshadweep's actual boundary extent,
# consistent with the buffered bounding-box approach used elsewhere in this
# project (e.g., the WDPA and IBTrACS bbox filtering).
BUFFER_DEGREES = 0.1


def download_file(url, out_path):
    if os.path.exists(out_path):
        print(f"Already downloaded: {out_path} — skipping download.")
        return
    print(f"Downloading {url} ...")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r  {downloaded / 1e6:,.0f} MB / {total / 1e6:,.0f} MB ({pct:.1f}%)", end="")
    print("\nDownload complete.")


def get_lakshadweep_bbox():
    gdf = gpd.read_file(BOUNDARY_PATH)
    minx, miny, maxx, maxy = gdf.total_bounds
    return (
        minx - BUFFER_DEGREES,
        miny - BUFFER_DEGREES,
        maxx + BUFFER_DEGREES,
        maxy + BUFFER_DEGREES,
    )


def clip_to_lakshadweep(source_path, bbox, output_path):
    minx, miny, maxx, maxy = bbox
    with rasterio.open(source_path) as src:
        window = from_bounds(minx, miny, maxx, maxy, transform=src.transform)
        data = src.read(1, window=window)
        transform = src.window_transform(window)
        profile = src.profile.copy()
        profile.update(
            height=data.shape[0],
            width=data.shape[1],
            transform=transform,
            compress="lzw",
        )
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(data, 1)
    print(f"Clipped Lakshadweep population raster saved to: {output_path}")
    print(f"  shape: {data.shape}, size on disk: {os.path.getsize(output_path) / 1e6:.2f} MB")


if __name__ == "__main__":
    os.makedirs("data/population", exist_ok=True)

    bbox = get_lakshadweep_bbox()
    print(f"Lakshadweep bounding box (with {BUFFER_DEGREES} degree buffer): {bbox}")

    download_file(WORLDPOP_URL, TEMP_DOWNLOAD_PATH)
    clip_to_lakshadweep(TEMP_DOWNLOAD_PATH, bbox, OUTPUT_PATH)

    print("Removing large temporary India-wide download to save disk space...")
    os.remove(TEMP_DOWNLOAD_PATH)
    print("Done. You can now re-run population_weighted_exposure.py.")
