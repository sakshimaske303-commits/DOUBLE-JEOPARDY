"""Per-pixel NDBI raster (2016 vs 2024) for the 3 mangrove islands; water
isn't masked here since it's unreliable per-scene on atolls -- done later
via the boundary polygons instead.
"""
import os
import time
import numpy as np
import rasterio
from rasterio.transform import from_bounds
import requests
from auth_sentinelhub import get_sentinelhub_token

PROCESS_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"
OUTPUT_DIR = "data/settlement_encroachment"

# Same bounding boxes already used and validated by download_ndbi_encroachment.py
ISLAND_BBOX = {
    "maldives": (72.9, 3.0, 73.6, 4.5),
    "seychelles": (55.3, -4.8, 55.6, -4.5),
    "fiji": (177.2, -18.3, 178.0, -17.5),
}

OUTPUT_SIZE_PX = 1024  # square output raster; Process API resamples to this

# Scene Classification Layer codes to exclude from the yearly mean — cloud,
# cloud shadow, cirrus, snow/ice, saturated/defective, and no-data. Water (6)
# and land (2/4/5/7) are both kept here; land-vs-water is handled afterward
# by clipping to the project's own island boundary polygons instead.
BAD_SCL = {0, 1, 3, 8, 9, 10, 11}

EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B11", "B08", "SCL"] }],
    output: { bands: 2, sampleType: "FLOAT32" },
    mosaicking: "ORBIT"
  };
}
function evaluatePixel(samples) {
  var badSCL = [0, 1, 3, 8, 9, 10, 11];
  var sum = 0;
  var count = 0;
  for (var i = 0; i < samples.length; i++) {
    var s = samples[i];
    if (badSCL.indexOf(s.SCL) === -1) {
      sum += (s.B11 - s.B08) / (s.B11 + s.B08 + 1e-6);
      count += 1;
    }
  }
  if (count === 0) {
    return [0, 0];
  }
  return [sum / count, 1];
}
"""


def make_bbox_geometry(bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    return {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat], [max_lon, min_lat],
            [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]
        ]]
    }


def request_ndbi_raster(access_token, bbox, year):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "input": {
            "bounds": {
                "geometry": make_bbox_geometry(bbox),
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": f"{year}-01-01T00:00:00Z", "to": f"{year + 1}-01-01T00:00:00Z"},
                    "maxCloudCoverage": 40,
                },
            }],
        },
        "output": {
            "width": OUTPUT_SIZE_PX,
            "height": OUTPUT_SIZE_PX,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}],
        },
        "evalscript": EVALSCRIPT,
    }
    # ORBIT mosaicking pulls every scene in the year for aggregation, so this
    # is a heavier request than a single-scene fetch — give it more time, and
    # retry once on failure since these heavier requests seem to fail
    # transiently on the server side occasionally.
    for attempt in (1, 2):
        try:
            response = requests.post(PROCESS_API_URL, headers=headers, json=payload, timeout=300)
        except requests.exceptions.RequestException as e:
            print(f"    Attempt {attempt} network error: {e}")
            response = None
        if response is not None and response.status_code == 200:
            return response.content
        if response is not None:
            print(f"    Attempt {attempt} FAILED ({response.status_code}): {response.text[:300]}")
        if attempt == 1:
            print("    Retrying once...")
            time.sleep(5)
    return None


def save_tiff(raw_bytes, bbox, out_path):
    tmp_path = out_path + ".raw.tif"
    with open(tmp_path, "wb") as f:
        f.write(raw_bytes)
    with rasterio.open(tmp_path) as src:
        ndbi = src.read(1)
        mask = src.read(2)
    ndbi = np.where(mask > 0, ndbi, np.nan)

    min_lon, min_lat, max_lon, max_lat = bbox
    transform = from_bounds(min_lon, min_lat, max_lon, max_lat, OUTPUT_SIZE_PX, OUTPUT_SIZE_PX)
    with rasterio.open(
        out_path, "w", driver="GTiff", height=OUTPUT_SIZE_PX, width=OUTPUT_SIZE_PX,
        count=1, dtype="float32", crs="EPSG:4326", transform=transform, nodata=np.nan,
    ) as dst:
        dst.write(ndbi.astype("float32"), 1)
    os.remove(tmp_path)


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for island, bbox in ISLAND_BBOX.items():
        print(f"Processing {island}...")
        paths = {}
        for year_label, year in [("2016", 2016), ("2024", 2024)]:
            print(f"  Requesting {year_label}...")
            raw = request_ndbi_raster(access_token, bbox, year)
            if raw is None:
                continue
            out_path = os.path.join(OUTPUT_DIR, f"{island}_ndbi_{year_label}.tif")
            save_tiff(raw, bbox, out_path)
            paths[year_label] = out_path
            print(f"    Saved: {out_path}")

        diff_path = os.path.join(OUTPUT_DIR, f"{island}_ndbi_diff.tif")
        if "2016" in paths and "2024" in paths:
            with rasterio.open(paths["2016"]) as src16, rasterio.open(paths["2024"]) as src24:
                ndbi16 = src16.read(1)
                ndbi24 = src24.read(1)
                profile = src16.profile
            diff = ndbi24 - ndbi16
            with rasterio.open(diff_path, "w", **profile) as dst:
                dst.write(diff.astype("float32"), 1)
            print(f"  Saved: {diff_path}")
        else:
            # Don't leave a stale diff file from an earlier, possibly-broken
            # run lying around if this run didn't get fresh data for both
            # years — that silently reuses wrong data downstream.
            if os.path.exists(diff_path):
                os.remove(diff_path)
                print(f"  Removed stale {diff_path} — one or both years failed this run, rerun to retry {island}.")
            else:
                print(f"  Skipped {island} — one or both years failed this run, rerun to retry.")
        print()

    print("Done. Run build_encroachment_map.py next to turn these rasters into the interactive map.")


if __name__ == "__main__":
    main()
