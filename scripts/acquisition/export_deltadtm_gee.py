"""Export DeltaDTM tiles for the five islands from Google Earth Engine to Google Drive.

Added 2026-10-11 because the 4TU.ResearchData download was offline for
maintenance. Same product: DeltaDTM v1.1 (Pronk et al. 2024), curated in the
GEE community catalogue as
    projects/sat-io/open-datasets/DELTARES/deltadtm_v1-1   (ee.Image, band "b1")
In v1.1 values are clipped at 30 m (a value of 30 means "30 m or higher");
that is dry at every threshold used here, so it needs no special handling.
Cells with no value (open water) are written as -9999.

One export task per 1 x 1 degree tile, for exactly the tiles that exist for
Copernicus in data/terrain/raw_tiles/<island>/ (tiles without land are skipped).
Each tile is exported on DeltaDTM's own 1-arc-second grid.

One-time setup (in PowerShell, from the repository root):
    pip install earthengine-api
    earthengine authenticate
Then:
    python scripts/acquisition/export_deltadtm_gee.py --project YOUR_GEE_PROJECT_ID

Your GEE project ID is shown at the top right of https://code.earthengine.google.com
(the same one used for STOLEN STRATA). The script starts all tasks and exits.
Watch them in the Tasks tab of the Code Editor or at
https://code.earthengine.google.com/tasks . When all are done, download the
Google Drive folder "DeltaDTM_DOUBLE_JEOPARDY", unzip it, and put the .tif files in
    data/terrain/deltadtm/gee/
Then run:  python scripts/acquisition/prepare_deltadtm_tiles.py
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COP_RAW = os.path.join(ROOT, "data", "terrain", "raw_tiles")
ASSET = "projects/sat-io/open-datasets/DELTARES/deltadtm_v1-1"
DRIVE_FOLDER = "DeltaDTM_DOUBLE_JEOPARDY"
NODATA = -9999
ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]
CODE_RE = re.compile(r"([NS])(\d{1,2})(?:_00)?_?([EW])(\d{1,3})", re.IGNORECASE)


def needed_tiles():
    out = {}
    for isl in ISLANDS:
        for p in glob.glob(os.path.join(COP_RAW, isl, "*.tif")):
            m = CODE_RE.search(os.path.basename(p))
            if m:
                ns, lat, ew, lon = m.groups()
                lat = int(lat) * (1 if ns.upper() == "N" else -1)
                lon = int(lon) * (1 if ew.upper() == "E" else -1)
                out[(lat, lon)] = isl
    return out


def tile_name(lat, lon):
    return f"DeltaDTM_v1-1_{'N' if lat >= 0 else 'S'}{abs(lat):02d}{'E' if lon >= 0 else 'W'}{abs(lon):03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="your Google Earth Engine cloud project ID")
    ap.add_argument("--dry-run", action="store_true", help="list the tiles without starting tasks")
    args = ap.parse_args()

    tiles = needed_tiles()
    if not tiles:
        sys.exit("No Copernicus tiles in data/terrain/raw_tiles/. Run download_copernicus_dem_tiles.py --all first.")
    print(f"{len(tiles)} tiles needed:")
    for isl in ISLANDS:
        print(f"  {isl}: {sum(1 for v in tiles.values() if v == isl)}")
    if args.dry_run:
        for (lat, lon) in sorted(tiles):
            print("   ", tile_name(lat, lon))
        return

    import ee
    ee.Initialize(project=args.project)
    img = ee.Image(ASSET).select("b1").toFloat().unmask(NODATA)
    proj = ee.Image(ASSET).select("b1").projection().getInfo()
    if not proj.get("transform"):  # fall back to the standard 1-arc-second global grid
        proj = {"crs": "EPSG:4326", "transform": [1 / 3600, 0, -180, 0, -1 / 3600, 90]}
    print(f"DeltaDTM native grid: {proj.get('crs')} {proj.get('transform')}")

    started = 0
    for (lat, lon), isl in sorted(tiles.items()):
        name = tile_name(lat, lon)
        region = ee.Geometry.Rectangle([lon, lat, lon + 1, lat + 1], "EPSG:4326", False)
        task = ee.batch.Export.image.toDrive(
            image=img,
            description=name,
            folder=DRIVE_FOLDER,
            fileNamePrefix=name,
            region=region,
            crs=proj.get("crs", "EPSG:4326"),
            crsTransform=proj.get("transform"),
            maxPixels=1e9,
            fileFormat="GeoTIFF",
            formatOptions={"cloudOptimized": True, "noData": NODATA},
        )
        task.start()
        started += 1
        print(f"  started {name} ({isl})")
    print(f"\n{started} export tasks started. Follow them at https://code.earthengine.google.com/tasks")
    print(f"When all are COMPLETED, download the Drive folder '{DRIVE_FOLDER}' and put the .tif files in "
          f"data/terrain/deltadtm/gee/, then run scripts/acquisition/prepare_deltadtm_tiles.py")


if __name__ == "__main__":
    main()
