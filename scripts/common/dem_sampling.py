"""Single, shared rule for reading a DEM value at each settlement point."""

import os

import numpy as np
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]
SNAP_HALF_WINDOW = 2          # 2 -> 5x5 window (about +-60 m at 1 arc-second)
NODATA_FLOOR = -1000.0        # anything at or below this is treated as NoData
KEPT_STATUSES = {"valid", "snapped_to_land", "above_10m"}
ELEVATION_SOURCES = ("copernicus", "deltadtm")
DELTADTM_CEILING_M = 10.0     # DeltaDTM's intended range; above it an empty cell is taken as dry land
# Above this Copernicus height DeltaDTM is not used (it can read forested hills as sea level).
DELTADTM_TRUST_MAX_COP_M = 30.0


def repo_path(*parts):
    """Absolute path inside the repository, wherever the caller runs from."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, *parts)


def deltadtm_path(island, west_of_antimeridian=False):
    """data/terrain/deltadtm/<island>_deltadtm.vrt, written by
    scripts/acquisition/prepare_deltadtm_tiles.py (None if not prepared)."""
    tag = "_west_of_antimeridian" if west_of_antimeridian else ""
    p = repo_path("data", "terrain", "deltadtm", f"{island}_deltadtm{tag}.vrt")
    if os.path.exists(p):
        return p
    if west_of_antimeridian:
        return deltadtm_path(island)
    return None


def deltadtm_ready():
    """True when a DeltaDTM VRT exists for every island."""
    return all(deltadtm_path(i) for i in ISLANDS)


def available_sources():
    """Copernicus always; DeltaDTM when prepared for all five islands."""
    return ["copernicus"] + (["deltadtm"] if deltadtm_ready() else [])


def primary_source():
    """The source reported as the main result: DeltaDTM when it
    is ready for every island, otherwise Copernicus, with a loud warning."""
    if deltadtm_ready():
        return "deltadtm"
    print("WARNING: DeltaDTM is not prepared for all islands (run "
          "scripts/acquisition/prepare_deltadtm_tiles.py). Main results fall back to "
          "Copernicus GLO-30, a surface model.", flush=True)
    return "copernicus"


def elevation_path(island, west_of_antimeridian=False):
    """Order of preference:
      1. data/terrain/<island>_elevation_v2.vrt   (tiles from
         scripts/acquisition/download_copernicus_dem_tiles.py)
      2. data/terrain/<island>_elevation_v2.tif   (earlier merged re-download)
      3. data/terrain/<island>_elevation.tif      (original file)
    For Fiji settlements with longitude < 0 (Lau group), the separate
    <island>_elevation_v2_west_of_antimeridian.vrt is used when it exists."""
    if west_of_antimeridian:
        w = repo_path("data", "terrain", f"{island}_elevation_v2_west_of_antimeridian.vrt")
        if os.path.exists(w):
            return w
    for name in (f"{island}_elevation_v2.vrt", f"{island}_elevation_v2.tif", f"{island}_elevation.tif"):
        p = repo_path("data", "terrain", name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"No elevation raster found for {island} in data/terrain/")


def _is_nodata(value, nodata):
    if value is None or np.isnan(value):
        return True
    if nodata is not None and not np.isnan(nodata) and value == nodata:
        return True
    return value <= NODATA_FLOOR


def sample_point(src, x, y, snap_zero_to_land=True, half_window=SNAP_HALF_WINDOW):
    """Return (raw_value, elevation_m, status) for one point. elevation_m is NaN
    for excluded statuses."""
    from rasterio.windows import Window

    nodata = src.nodata
    row, col = src.index(x, y)
    if not (0 <= row < src.height and 0 <= col < src.width):
        return np.nan, np.nan, "out_of_extent"

    raw = float(src.read(1, window=Window(col, row, 1, 1))[0, 0])
    if _is_nodata(raw, nodata):
        return raw, np.nan, "nodata"
    if raw != 0.0:
        return raw, raw, "valid"

    if not snap_zero_to_land:
        return raw, np.nan, "water_no_land_nearby"

    fill = nodata if nodata is not None else np.nan
    win = Window(col - half_window, row - half_window, 2 * half_window + 1, 2 * half_window + 1)
    block = src.read(1, window=win, boundless=True, fill_value=fill).astype("float64")
    land = block[(block != 0.0) & ~np.isnan(block) & (block > NODATA_FLOOR)]
    if nodata is not None:
        land = land[land != nodata]
    if land.size == 0:
        return raw, np.nan, "water_no_land_nearby"
    return raw, float(np.median(land)), "snapped_to_land"


def sample_point_fill(src, x, y, half_window=SNAP_HALF_WINDOW):
    """DeltaDTM reading: value at the point, or the median of valid pixels in the
    5x5 window when the point itself is empty or 0.0 (coast/tile edge).
    Returns (raw_value, elevation_m, status)."""
    from rasterio.windows import Window

    nodata = src.nodata
    row, col = src.index(x, y)
    if not (0 <= row < src.height and 0 <= col < src.width):
        return np.nan, np.nan, "out_of_extent"
    raw = float(src.read(1, window=Window(col, row, 1, 1))[0, 0])
    if not _is_nodata(raw, nodata) and raw != 0.0:
        return raw, raw, "valid"
    fill = nodata if nodata is not None else np.nan
    win = Window(col - half_window, row - half_window, 2 * half_window + 1, 2 * half_window + 1)
    block = src.read(1, window=win, boundless=True, fill_value=fill).astype("float64")
    ok = (block != 0.0) & ~np.isnan(block) & (block > NODATA_FLOOR)
    if nodata is not None:
        ok &= block != nodata
    if ok.any():
        return raw, float(np.median(block[ok])), "snapped_to_land"
    return raw, np.nan, "nodata"


def fix_antimeridian_lon(island, lon):
    """Six Fiji settlements (Lau Group, Vanua Levu Group, Taveuni, Vanua Levu,
    Korolevu Island, Rabi) were stored at longitude ~0 deg: their point was
    computed as the plain average of polygon vertices on both sides of the
    180 deg meridian (e.g. 179.9 and -179.9 -> 0.0). Their latitude is right.
    Adding 180 deg recovers the true position (e.g. Vanua Levu -0.59 -> 179.41)."""
    if island == "fiji" and abs(lon) < 10:
        lon = lon + 180.0
        if lon > 180:
            lon -= 360.0
    return lon


def sample_settlements(island, snap_zero_to_land=True, source="copernicus"):
    """One row per settlement in data/settlements/<island>_settlements_clean.gpkg
    with columns name, place, lon, lat, raw_value, elevation_m, status, dem_file,
    elevation_source. For source="deltadtm" see the module docstring."""
    if source not in ELEVATION_SOURCES:
        raise ValueError(f"unknown elevation source {source!r}")
    import geopandas as gpd
    import rasterio

    gdf = gpd.read_file(repo_path("data", "settlements", f"{island}_settlements_clean.gpkg"))
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    main_dem = elevation_path(island)
    west_dem = elevation_path(island, west_of_antimeridian=True)
    rows = []
    with rasterio.open(main_dem) as src_main, rasterio.open(west_dem) as src_west:
        for _, rec in gdf.iterrows():
            pt = rec.geometry.centroid
            x = fix_antimeridian_lon(island, pt.x)
            src = src_west if (x < 0 and west_dem != main_dem) else src_main
            raw, elev, status = sample_point(src, x, pt.y, snap_zero_to_land=snap_zero_to_land)
            rows.append({
                "name": rec.get("name") if pd.notna(rec.get("name")) else "Unnamed settlement",
                "place": rec.get("place", ""),
                "lon": x, "lat": pt.y,
                "raw_value": raw, "elevation_m": elev, "status": status,
                "dem_file": os.path.basename(src.name),
                "elevation_source": "copernicus",
            })
    df = pd.DataFrame(rows)
    if source == "deltadtm":
        df = _apply_deltadtm(island, df)
    return df


def _apply_deltadtm(island, df):
    """Replace heights with DeltaDTM for places Copernicus kept (same place set)."""
    import rasterio

    main = deltadtm_path(island)
    if main is None:
        raise FileNotFoundError(f"No DeltaDTM VRT for {island}; run prepare_deltadtm_tiles.py")
    west = deltadtm_path(island, west_of_antimeridian=True)
    df = df.copy()
    df["copernicus_m"] = df["elevation_m"]
    with rasterio.open(main) as d_main, rasterio.open(west) as d_west:
        for i, r in df.iterrows():
            if r["status"] not in ("valid", "snapped_to_land"):
                continue  # excluded under Copernicus too: keep the same denominator
            src = d_west if (r["lon"] < 0 and west != main) else d_main
            raw, elev, st = sample_point_fill(src, r["lon"], r["lat"])
            if r["copernicus_m"] > DELTADTM_TRUST_MAX_COP_M:
                df.at[i, "raw_value"], df.at[i, "status"] = raw, "above_10m"
                df.at[i, "dem_file"] = os.path.basename(src.name)
                continue  # high terrain: DeltaDTM out of scope, keep the Copernicus height
            if st in ("valid", "snapped_to_land"):
                df.at[i, "raw_value"], df.at[i, "elevation_m"], df.at[i, "status"] = raw, elev, st
            elif r["copernicus_m"] > DELTADTM_CEILING_M:
                df.at[i, "raw_value"], df.at[i, "status"] = raw, "above_10m"
                # elevation_m keeps the Copernicus height (> 10 m, dry at every threshold used)
            else:
                df.at[i, "raw_value"], df.at[i, "elevation_m"], df.at[i, "status"] = raw, np.nan, "deltadtm_nodata"
            df.at[i, "dem_file"] = os.path.basename(src.name)
    df["elevation_source"] = "deltadtm"
    return df


def status_counts(df):
    return df["status"].value_counts().to_dict()
