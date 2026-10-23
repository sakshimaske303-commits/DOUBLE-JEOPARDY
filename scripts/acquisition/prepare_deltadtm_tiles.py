"""Prepare DeltaDTM (bare-earth coastal elevation) tiles for the five islands.

Run from the repository root:
    python scripts/acquisition/prepare_deltadtm_tiles.py
"""
import glob
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COP_RAW = os.path.join(ROOT, "data", "terrain", "raw_tiles")
DDTM_DIR = os.path.join(ROOT, "data", "terrain", "deltadtm")
ZIP_DIR = os.path.join(DDTM_DIR, "zips")
GEE_DIR = os.path.join(DDTM_DIR, "gee")
TILE_DIR = os.path.join(DDTM_DIR, "tiles")
ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

# N04_00_E073 (Copernicus) or N04E073 / N04_E073 (other products)
CODE_RE = re.compile(r"([NS])(\d{1,2})(?:_00)?_?([EW])(\d{1,3})", re.IGNORECASE)
WGS84_WKT = ('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],'
             'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]')


def parse_code(name):
    m = CODE_RE.search(os.path.basename(name))
    if not m:
        return None
    ns, lat, ew, lon = m.groups()
    lat = int(lat) * (1 if ns.upper() == "N" else -1)
    lon = int(lon) * (1 if ew.upper() == "E" else -1)
    return lat, lon


def needed_tiles(island):
    """(lat, lon) lower-left corners of the Copernicus tiles present for this island."""
    out = set()
    for p in glob.glob(os.path.join(COP_RAW, island, "*.tif")):
        c = parse_code(p)
        if c:
            out.add(c)
    return out


def is_tile(member):
    low = member.lower()
    return low.endswith((".tif", ".tiff")) and "mask" not in low


def tile_cell(bounds):
    """Lower-left 1-degree cell of a tile from its real bounds."""
    cx = (bounds.left + bounds.right) / 2
    cy = (bounds.bottom + bounds.top) / 2
    return math.floor(cy), math.floor(cx)


def index_zips():
    """{(lat, lon): (zip_path, member)} for every DeltaDTM tile in every zip, by name."""
    by_name = {}
    members_all = []
    zips = sorted(glob.glob(os.path.join(ZIP_DIR, "*.zip")))
    for zp in zips:
        with zipfile.ZipFile(zp) as z:
            for m in z.namelist():
                if not is_tile(m):
                    continue
                members_all.append((zp, m))
                c = parse_code(m)
                if c and c not in by_name:
                    by_name[c] = (zp, m)
    return zips, by_name, members_all


def find_by_bounds(missing, members_all):
    """Slow path: open each tile header inside the zip to read its real bounds."""
    import rasterio

    found = {}
    for zp, m in members_all:
        if not missing - set(found):
            break
        path = "/vsizip/" + zp.replace("\\", "/") + "/" + m
        try:
            with rasterio.open(path) as src:
                cell = tile_cell(src.bounds)
        except Exception:
            continue
        if cell in missing and cell not in found:
            found[cell] = (zp, m)
    return found


def extract(zp, member, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, os.path.basename(member))
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return out
    with zipfile.ZipFile(zp) as z, z.open(member) as fsrc, open(out, "wb") as fdst:
        while True:
            chunk = fsrc.read(1 << 20)
            if not chunk:
                break
            fdst.write(chunk)
    return out


def check_and_cell(path):
    """Read one block to prove the file decodes (ZSTD). Returns (cell, info) or raises."""
    import rasterio
    from rasterio.windows import Window

    with rasterio.open(path) as src:
        src.read(1, window=Window(0, 0, min(256, src.width), min(256, src.height)))
        return tile_cell(src.bounds), (path, src.bounds, src.width, src.height, src.res, src.dtypes[0], src.nodata)


def build_vrt(infos, vrt_path):
    res_x = min(i[4][0] for i in infos)
    res_y = min(i[4][1] for i in infos)
    left = min(i[1].left for i in infos)
    top = max(i[1].top for i in infos)
    right = max(i[1].right for i in infos)
    bottom = min(i[1].bottom for i in infos)
    width = int(round((right - left) / res_x))
    height = int(round((top - bottom) / res_y))
    dtype = {"float32": "Float32", "float64": "Float64", "int16": "Int16"}.get(infos[0][5], "Float32")
    nodata = infos[0][6] if infos[0][6] is not None else -9999

    root = ET.Element("VRTDataset", rasterXSize=str(width), rasterYSize=str(height))
    # Horizontal WGS84 only. The tiles' compound CRS (EPSG:9518, WGS84 + EGM2008
    # height) is the same horizontally; writing plain EPSG:4326 keeps reprojection
    # to the population grid simple. Heights stay EGM2008, as for Copernicus.
    ET.SubElement(root, "SRS").text = WGS84_WKT
    ET.SubElement(root, "GeoTransform").text = f"{left}, {res_x}, 0.0, {top}, 0.0, {-res_y}"
    band = ET.SubElement(root, "VRTRasterBand", dataType=dtype, band="1")
    ET.SubElement(band, "NoDataValue").text = str(nodata)
    for p, b, w, h, *_ in infos:
        src = ET.SubElement(band, "SimpleSource")
        ET.SubElement(src, "SourceFilename", relativeToVRT="1").text = \
            os.path.relpath(p, os.path.dirname(vrt_path)).replace("\\", "/")
        ET.SubElement(src, "SourceBand").text = "1"
        ET.SubElement(src, "SrcRect", xOff="0", yOff="0", xSize=str(w), ySize=str(h))
        ET.SubElement(src, "DstRect",
                      xOff=str(int(round((b.left - left) / res_x))),
                      yOff=str(int(round((top - b.top) / res_y))),
                      xSize=str(int(round((b.right - b.left) / res_x))),
                      ySize=str(int(round((b.top - b.bottom) / res_y))))
    ET.ElementTree(root).write(vrt_path)
    return width, height


def index_gee():
    """{(lat, lon): path} for loose .tif tiles exported from Earth Engine."""
    out = {}
    for p in glob.glob(os.path.join(GEE_DIR, "**", "*.tif"), recursive=True):
        c = parse_code(p)
        if c and is_tile(p):
            out[c] = p
    return out


def main():
    gee = index_gee()
    zips, by_name, members_all = index_zips()
    if not zips and not gee:
        sys.exit(f"No DeltaDTM tiles found. Either put the continent zips in {ZIP_DIR}, or export the "
                 f"tiles with export_deltadtm_gee.py and put the .tif files in {GEE_DIR}.")
    if gee:
        print(f"Earth Engine tiles in {GEE_DIR}: {len(gee)}")
    if zips:
        print(f"Zips: {', '.join(os.path.basename(z) for z in zips)}  ({len(members_all)} tiles inside)")

    need = {isl: needed_tiles(isl) for isl in ISLANDS}
    all_needed = set().union(*need.values())
    if not all_needed:
        sys.exit("No Copernicus tiles found in data/terrain/raw_tiles/. Run "
                 "download_copernicus_dem_tiles.py --all first.")
    located = {c: ("GEE", gee[c]) for c in all_needed if c in gee}
    located.update({c: by_name[c] for c in all_needed if c in by_name and c not in located})
    missing = all_needed - set(located)
    if missing and members_all:
        print(f"{len(missing)} tiles not matched by name; checking real bounds inside the zips "
              f"(this can take a few minutes)...")
        located.update(find_by_bounds(missing, members_all))

    summary = []
    for isl in ISLANDS:
        out_dir = os.path.join(TILE_DIR, isl)
        infos, bad, absent = [], [], []
        for cell in sorted(need[isl]):
            if cell not in located:
                absent.append(cell)
                continue
            zp, m = located[cell]
            path = m if zp == "GEE" else extract(zp, m, out_dir)
            try:
                real_cell, info = check_and_cell(path)
            except Exception as e:
                bad.append((cell, str(e)))
                continue
            if real_cell != cell:
                print(f"  {isl}: tile {os.path.basename(path)} covers {real_cell}, expected {cell}; skipped")
                absent.append(cell)
                continue
            infos.append(info)

        if bad:
            print(f"\n{isl.upper()}: {len(bad)} tile(s) could not be READ. Usually this means your "
                  f"GDAL/rasterio has no ZSTD support. Fix: conda install -c conda-forge rasterio "
                  f"(or pip install --upgrade rasterio). First error: {bad[0][1]}")
        if infos:
            if isl == "fiji":
                east = [i for i in infos if (i[1].left + i[1].right) / 2 >= 0]
                west = [i for i in infos if (i[1].left + i[1].right) / 2 < 0]
                for tag, group in (("", east), ("_west_of_antimeridian", west)):
                    if group:
                        build_vrt(group, os.path.join(DDTM_DIR, f"fiji_deltadtm{tag}.vrt"))
            else:
                build_vrt(infos, os.path.join(DDTM_DIR, f"{isl}_deltadtm.vrt"))
        summary.append((isl, len(need[isl]), len(infos), len(absent), len(bad), absent))

    print(f"\n{'island':<12} {'needed':>7} {'ready':>6} {'missing':>8} {'unreadable':>11}")
    for isl, n, ok, miss, bad, absent in summary:
        print(f"{isl:<12} {n:>7} {ok:>6} {miss:>8} {bad:>11}")
        if absent:
            print("    missing tiles (lat, lon of lower-left corner): " + ", ".join(map(str, absent)))
    print("\nA missing tile is fine if DeltaDTM has no low-lying coast there; points on it are then "
          "taken from Copernicus when above 10 m and reported as 'deltadtm_nodata' otherwise.")
    print("If a whole island is missing, download that continent's zip and run this again.")


if __name__ == "__main__":
    main()
