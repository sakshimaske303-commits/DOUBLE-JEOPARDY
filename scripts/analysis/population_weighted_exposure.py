"""Population-weighted physical exposure at or below a 1m sea-level-rise threshold."""

# Results are written to data/population_weighted_exposure.csv.

# Main exposure measure; runs once per elevation source (DeltaDTM, Copernicus).

import os
import sys
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import Window, from_bounds
from rasterio.warp import reproject, Resampling, transform_bounds, transform_geom
from scipy.ndimage import minimum_filter, maximum_filter

ELEVATION_THRESHOLD_M = 1.0
BUFFER_DEGREES = 0.1  # small buffer around each island's real known extent

# Islands whose elevation file needs the flat-neighborhood void check
# (see module docstring) rather than being trusted as-is.
VOID_CHECK_ISLANDS = {"Maldives", "Lakshadweep"}
VOID_HALF_WINDOW = 2  # 2 -> 5x5 window, matching slr_exposure_analysis.py

# Mask population to the validated island boundaries (data/boundaries_v2).
APPLY_BOUNDARY_MASK = True

# Large windows are processed in CHUNK_DEG x CHUNK_DEG pieces so the 1-arc-second
# DEM read stays small (Seychelles spans ~10 x 7 degrees).
CHUNK_DEG = 1.0

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.common.dem_sampling import (DELTADTM_CEILING_M, DELTADTM_TRUST_MAX_COP_M, available_sources,  # noqa: E402
                                         deltadtm_path, elevation_path, primary_source)


def build_void_mask(elev_array, half_window=VOID_HALF_WINDOW):
    """True where a pixel reads exactly 0.0 AND its (2*half_window+1)^2
    neighborhood is also entirely 0.0 -- the flat-void signature no real
    terrain produces. Same logic as slr_exposure_analysis.py's settlement-
    point check, applied here across the whole raster at once."""
    size = 2 * half_window + 1
    local_min = minimum_filter(elev_array, size=size, mode="nearest")
    local_max = maximum_filter(elev_array, size=size, mode="nearest")
    return (elev_array == 0.0) & (local_min == 0.0) & (local_max == 0.0)

# Each island: elevation/population/boundary file paths, plus a list of
# (minx, miny, maxx, maxy) windows in EPSG:4326. Normally one window per
# island; Fiji gets two (west-of-dateline, east-of-dateline) since its
# territory straddles the antimeridian.
ISLANDS = {
    "Maldives": {
        "elevation": elevation_path("maldives"),
        "key": "maldives",
        "population": "data/population/maldives_population_clean.tif",
        "boundary": "data/boundaries_v2/maldives_islands_v2.gpkg",
        # from data/boundaries/maldives_islands.gpkg total_bounds
        "windows": [(72.68 - BUFFER_DEGREES, -0.69 - BUFFER_DEGREES,
                     73.76 + BUFFER_DEGREES, 7.11 + BUFFER_DEGREES)],
    },
    "Seychelles": {
        "elevation": elevation_path("seychelles"),
        "key": "seychelles",
        "population": "data/population/seychelles_population_clean.tif",
        "boundary": "data/boundaries_v2/seychelles_islands_v2.gpkg",
        # from data/boundaries/seychelles_islands.gpkg total_bounds
        "windows": [(46.21 - BUFFER_DEGREES, -9.76 - BUFFER_DEGREES,
                     56.29 + BUFFER_DEGREES, -3.79 + BUFFER_DEGREES)],
    },
    "Fiji": {
        "elevation": elevation_path("fiji"),
        "key": "fiji",
        "population": "data/population/fiji_population_clean.tif",
        "boundary": "data/boundaries_v2/fiji_islands_v2.gpkg",
        # two windows straddling the antimeridian — mirrors the "two
        # sub-queries" approach already used for Fiji's WDPA data
        "windows": [
            (176.5, -20.7, 180.0, -12.4),    # west-of-dateline half
            (-180.0, -20.7, -178.0, -12.4),  # east-of-dateline half
        ],
    },
    "Canary Islands": {
        "elevation": elevation_path("canary"),
        "key": "canary",
        "population": "data/population/canary_population_clean.tif",
        "boundary": "data/boundaries_v2/canary_islands_v2.gpkg",
        # from data/boundaries/canary_islands.gpkg total_bounds
        "windows": [(-18.17 - BUFFER_DEGREES, 27.64 - BUFFER_DEGREES,
                     -13.42 + BUFFER_DEGREES, 29.24 + BUFFER_DEGREES)],
    },
    "Lakshadweep": {
        "elevation": elevation_path("lakshadweep"),
        "key": "lakshadweep",
        "population": "data/population/lakshadweep_population_clean.tif",
        "boundary": "data/boundaries_v2/lakshadweep_islands_v2.gpkg",
        # from data/boundaries/lakshadweep_islands.gpkg total_bounds
        "windows": [(72.17 - BUFFER_DEGREES, 8.25 - BUFFER_DEGREES,
                     73.68 + BUFFER_DEGREES, 11.69 + BUFFER_DEGREES)],
    },
}


def load_boundary_geoms(boundary_path, dst_crs):
    """All island polygons for this boundary file, reprojected to dst_crs
    (the population raster's CRS) as a list of __geo_interface__ mappings —
    what rasterio.features.geometry_mask expects."""
    gdf = gpd.read_file(boundary_path)
    if gdf.crs is not None and str(gdf.crs) != str(dst_crs):
        gdf = gdf.to_crs(dst_crs)
    return [geom.__geo_interface__ for geom in gdf.geometry if geom is not None and not geom.is_empty]


def _clean(arr, nodata):
    """NaN for NoData, values <= -1000 and exact 0.0 (flattened water surface)."""
    bad = ~np.isfinite(arr) | (arr <= -1000.0) | (arr == 0.0)
    if nodata is not None:
        bad |= arr == nodata
    return np.where(bad, np.nan, arr)


def _fill_from_copernicus(ddtm, ddtm_transform, ddtm_crs, cop_src, bounds):
    """Where DeltaDTM is empty, use Copernicus if it is above the 10 m ceiling."""
    window = from_bounds(*bounds, transform=cop_src.transform).round_offsets().round_lengths()
    window = window.intersection(Window(0, 0, cop_src.width, cop_src.height))
    if window.width <= 0 or window.height <= 0:
        return ddtm
    cop = _clean(cop_src.read(1, window=window).astype("float32"), cop_src.nodata)
    cop_on_grid = np.full(ddtm.shape, np.nan, dtype="float32")
    reproject(source=cop, destination=cop_on_grid, src_transform=cop_src.window_transform(window),
              src_crs=cop_src.crs, src_nodata=np.nan, dst_transform=ddtm_transform, dst_crs=ddtm_crs,
              dst_nodata=np.nan, resampling=Resampling.nearest)
    high = np.isfinite(cop_on_grid) & (
        (np.isnan(ddtm) & (cop_on_grid > DELTADTM_CEILING_M))   # DeltaDTM empty above its 10 m scope
        | (cop_on_grid > DELTADTM_TRUST_MAX_COP_M))             # high terrain: DeltaDTM out of scope
    return np.where(high, cop_on_grid, ddtm)


def process_bbox(pop_src, elev_src, bbox, boundary_geoms, threshold, void_check=False, cop_src=None):
    minx, miny, maxx, maxy = bbox

    pop_window = from_bounds(minx, miny, maxx, maxy, transform=pop_src.transform)
    pop_window = pop_window.round_offsets().round_lengths()
    pop_window = pop_window.intersection(Window(0, 0, pop_src.width, pop_src.height))
    if pop_window.width <= 0 or pop_window.height <= 0:
        raise ValueError("bbox does not overlap the population raster at all")

    pop_array = pop_src.read(1, window=pop_window).astype("float32")
    pop_nodata = pop_src.nodata
    pop_transform = pop_src.window_transform(pop_window)
    pop_crs = pop_src.crs
    pop_shape = pop_array.shape

    if pop_nodata is not None:
        pop_array = np.where(pop_array == pop_nodata, 0, pop_array)
    pop_array = np.where(pop_array < 0, 0, pop_array)

    # Polygon mask: zero out any population pixel whose center falls
    # outside the island's actual boundary polygon, so a bbox window that
    # spans a lot of open water (Fiji, Seychelles) doesn't count ocean
    # pixels as "population at risk" or "population not at risk" — they
    # should count as neither, since no one lives there.
    if boundary_geoms:
        # all_touched=True so narrow atoll islands are not dropped.
        land_mask = geometry_mask(
            boundary_geoms, out_shape=pop_shape, transform=pop_transform, invert=True,
            all_touched=True,
        )
        pop_array = np.where(land_mask, pop_array, 0)

    if elev_src.crs != pop_crs:
        e_minx, e_miny, e_maxx, e_maxy = transform_bounds(pop_crs, elev_src.crs, minx, miny, maxx, maxy)
    else:
        e_minx, e_miny, e_maxx, e_maxy = minx, miny, maxx, maxy

    elev_window = from_bounds(e_minx, e_miny, e_maxx, e_maxy, transform=elev_src.transform)
    elev_window = elev_window.round_offsets().round_lengths()
    elev_window = elev_window.intersection(Window(0, 0, elev_src.width, elev_src.height))
    if elev_window.width <= 0 or elev_window.height <= 0:
        raise ValueError("bbox does not overlap the elevation raster at all")

    elev_window_data = elev_src.read(1, window=elev_window).astype("float32")
    elev_window_transform = elev_src.window_transform(elev_window)

    # NoData, NaN and 0 m water pixels are dropped before resampling; cells with no land are excluded and reported.
    elev_window_data = _clean(elev_window_data, elev_src.nodata)
    if cop_src is not None:  # DeltaDTM run: fill empty cells that Copernicus puts above 10 m
        elev_window_data = _fill_from_copernicus(elev_window_data, elev_window_transform, elev_src.crs,
                                                 cop_src, (e_minx, e_miny, e_maxx, e_maxy))

    elev_on_pop_grid = np.full(pop_shape, np.nan, dtype="float32")
    reproject(
        source=elev_window_data,
        destination=elev_on_pop_grid,
        src_transform=elev_window_transform,
        src_crs=elev_src.crs,
        src_nodata=np.nan,
        dst_transform=pop_transform,
        dst_crs=pop_crs,
        dst_nodata=np.nan,
        resampling=Resampling.average,
    )

    no_elev = ~np.isfinite(elev_on_pop_grid)
    excluded_pop = float(pop_array[no_elev].sum())
    pop_array = np.where(no_elev, 0, pop_array)

    at_risk_mask = np.isfinite(elev_on_pop_grid) & (elev_on_pop_grid <= threshold)
    return pop_array[at_risk_mask].sum(), pop_array.sum(), excluded_pop


def population_in_bbox(pop_src, bbox, boundary_geoms=None):
    """Just the population total in a bbox (optionally polygon-masked), with
    no elevation requirement — used to report how many people fall in a
    window we had to skip."""
    minx, miny, maxx, maxy = bbox
    window = from_bounds(minx, miny, maxx, maxy, transform=pop_src.transform)
    window = window.round_offsets().round_lengths()
    window = window.intersection(Window(0, 0, pop_src.width, pop_src.height))
    if window.width <= 0 or window.height <= 0:
        return 0.0
    arr = pop_src.read(1, window=window).astype("float32")
    nodata = pop_src.nodata
    if nodata is not None:
        arr = np.where(arr == nodata, 0, arr)
    arr = np.where(arr < 0, 0, arr)
    if boundary_geoms:
        land_mask = geometry_mask(
            boundary_geoms, out_shape=arr.shape,
            transform=pop_src.window_transform(window), invert=True,
            all_touched=True,
        )
        arr = np.where(land_mask, arr, 0)
    return float(arr.sum())


def split_bbox(bbox, step=CHUNK_DEG):
    minx, miny, maxx, maxy = bbox
    xs = list(np.arange(minx, maxx, step)) + [maxx]
    ys = list(np.arange(miny, maxy, step)) + [maxy]
    return [(xs[i], ys[j], xs[i + 1], ys[j + 1]) for i in range(len(xs) - 1) for j in range(len(ys) - 1)]


def population_weighted_exposure(elevation_path, population_path, boundary_path, windows, threshold=1.0,
                                    void_check=False, west_elevation_path=None,
                                    cop_path=None, west_cop_path=None):
    total_at_risk = 0.0
    total_pop = 0.0
    skipped_pop = 0.0
    excluded_gap_pop = 0.0
    west_elevation_path = west_elevation_path or elevation_path
    from contextlib import ExitStack
    with ExitStack() as stack:
        pop_src = stack.enter_context(rasterio.open(population_path))
        elev_main = stack.enter_context(rasterio.open(elevation_path))
        elev_west = stack.enter_context(rasterio.open(west_elevation_path))
        cop_main = stack.enter_context(rasterio.open(cop_path)) if cop_path else None
        cop_west = stack.enter_context(rasterio.open(west_cop_path or cop_path)) if cop_path else None
        if not APPLY_BOUNDARY_MASK:
            boundary_geoms = None
        else:
            try:
                boundary_geoms = load_boundary_geoms(boundary_path, pop_src.crs)
            except Exception as e:
                print(f"    WARNING: couldn't load boundary polygon ({e}) — falling back to bbox-only, unmasked",
                      flush=True)
                boundary_geoms = None

        chunks = [c for w in windows for c in split_bbox(w)]
        for i, bbox in enumerate(chunks, start=1):
            elev_src = elev_west if bbox[0] < 0 else elev_main
            cop_src = (cop_west if bbox[0] < 0 else cop_main) if cop_main is not None else None
            print(f"    chunk {i}/{len(chunks)}: {tuple(round(v, 2) for v in bbox)}", flush=True)
            try:
                at_risk, total, excluded = process_bbox(pop_src, elev_src, bbox, boundary_geoms, threshold,
                                                          void_check=void_check, cop_src=cop_src)
                total_at_risk += at_risk
                total_pop += total
                excluded_gap_pop += excluded
            except Exception as e:
                cluster_pop = population_in_bbox(pop_src, bbox, boundary_geoms)
                skipped_pop += cluster_pop
                print(f"    SKIPPED window {i} — elevation file doesn't cover this area "
                      f"({cluster_pop:,.0f} people in this window excluded). Reason: {e}",
                      flush=True)
    if skipped_pop > 0:
        print(f"    NOTE: {skipped_pop:,.0f} people were in areas with no elevation "
              f"coverage and were excluded from this island's percentage.", flush=True)
    if excluded_gap_pop > 0:
        print(f"    NOTE: {excluded_gap_pop:,.0f} people sit on cells with no usable elevation "
              f"(NoData, no tile, or water-only DEM pixels) and were excluded from both the "
              f"numerator and denominator, rather than counted as at-risk.", flush=True)
    percent_at_risk = (total_at_risk / total_pop * 100) if total_pop > 0 else float("nan")
    return total_at_risk, total_pop, percent_at_risk, excluded_gap_pop


def run_source(source):
    rows = []
    print(f"\n===== elevation source: {source} =====")
    print(f"{'Island':<16} {'Pop. at risk':>15} {'Total pop.':>15} {'% at risk':>12} {'Excl. (no elev.)':>16}")
    print("-" * 78)
    for island, cfg in ISLANDS.items():
        print(f"  -> {island}...", flush=True)
        key = cfg["key"]
        try:
            if source == "deltadtm":
                kw = dict(elevation_path=deltadtm_path(key),
                          west_elevation_path=deltadtm_path(key, west_of_antimeridian=True),
                          cop_path=elevation_path(key),
                          west_cop_path=elevation_path(key, west_of_antimeridian=True))
            else:
                kw = dict(elevation_path=elevation_path(key),
                          west_elevation_path=elevation_path(key, west_of_antimeridian=True))
            at_risk, total, pct, excluded = population_weighted_exposure(
                population_path=cfg["population"], boundary_path=cfg["boundary"], windows=cfg["windows"],
                threshold=ELEVATION_THRESHOLD_M, void_check=(island in VOID_CHECK_ISLANDS), **kw)
            print(f"{island:<16} {at_risk:>15,.0f} {total:>15,.0f} {pct:>11.1f}% {excluded:>16,.0f}")
            rows.append({"island": island, "elevation_source": source, "pop_at_risk": at_risk,
                         "pop_with_elevation": total, "pct_at_risk": pct,
                         "pop_excluded_no_elevation": excluded,
                         "pct_pop_covered": total / (total + excluded) * 100 if (total + excluded) else float("nan")})
        except Exception as e:
            print(f"{island:<16}  ERROR: {e}")
    return rows


if __name__ == "__main__":
    import pandas as pd
    primary = primary_source()
    rows = []
    for source in available_sources():
        rows += run_source(source)
    out = pd.DataFrame(rows)
    out.to_csv("data/population_weighted_exposure_by_source.csv", index=False)
    out[out["elevation_source"] == primary].to_csv("data/population_weighted_exposure.csv", index=False)
    print(f"Saved: data/population_weighted_exposure.csv (primary source: {primary}) and "
          f"data/population_weighted_exposure_by_source.csv")
