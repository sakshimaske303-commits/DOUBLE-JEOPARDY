"""Population-weighted physical exposure at or below a 1m sea-level-rise
threshold.

v4 used simple bbox windows around each island. This undercounted
Maldives by about 1/3, because a bbox also covers open water next to
the island.

v5 tries to fix this by masking to each island's real boundary shape
(data/boundaries/) instead of just the bbox. But when this was tested
against the real population and elevation rasters, the boundary files
turned out to be incomplete.

For Maldives, the boundary polygons only add up to about 118 sq km of
land. Real Maldives land area is close to 298 sq km. A lot of real
islands are just missing from this file.

For Lakshadweep, the polygon file's total area is close to correct
(about 34 sq km vs a real ~32 sq km), but the mask still only catches
about 13% of the real population. So even the islands that ARE in the
file are drawn smaller than their real built-up area.

This was checked carefully: the population raster itself is fine
(checked pixel by pixel -- the values are real and not blurred or
repeated). The masking code is also fine (all_touched=True is set
below, and that part works as intended). The only problem is the
boundary polygon files -- they don't fully match the real islands.

Because of this, v5 is not ready to use yet. The paper still reports
the v4 (bbox) numbers for now, and already flags those as less
accurate for irregular islands. Fixing this properly needs a better,
more complete set of island boundary shapes -- not another code
change. Needs rasterio, geopandas, numpy.
"""

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import Window, from_bounds
from rasterio.warp import reproject, Resampling, transform_bounds, transform_geom

ELEVATION_THRESHOLD_M = 1.0
BUFFER_DEGREES = 0.1  # small buffer around each island's real known extent

# Each island: elevation/population/boundary file paths, plus a list of
# (minx, miny, maxx, maxy) windows in EPSG:4326. Normally one window per
# island; Fiji gets two (west-of-dateline, east-of-dateline) since its
# territory straddles the antimeridian.
ISLANDS = {
    "Maldives": {
        "elevation": "data/terrain/maldives_elevation.tif",
        "population": "data/population/maldives_population_clean.tif",
        "boundary": "data/boundaries/maldives_islands.gpkg",
        # from data/boundaries/maldives_islands.gpkg total_bounds
        "windows": [(72.68 - BUFFER_DEGREES, -0.69 - BUFFER_DEGREES,
                     73.76 + BUFFER_DEGREES, 7.11 + BUFFER_DEGREES)],
    },
    "Seychelles": {
        "elevation": "data/terrain/seychelles_elevation.tif",
        "population": "data/population/seychelles_population_clean.tif",
        "boundary": "data/boundaries/seychelles_islands.gpkg",
        # from data/boundaries/seychelles_islands.gpkg total_bounds
        "windows": [(46.21 - BUFFER_DEGREES, -9.76 - BUFFER_DEGREES,
                     56.29 + BUFFER_DEGREES, -3.79 + BUFFER_DEGREES)],
    },
    "Fiji": {
        "elevation": "data/terrain/fiji_elevation.tif",
        "population": "data/population/fiji_population_clean.tif",
        "boundary": "data/boundaries/fiji_islands.gpkg",
        # two windows straddling the antimeridian — mirrors the "two
        # sub-queries" approach already used for Fiji's WDPA data
        "windows": [
            (176.5, -20.7, 180.0, -12.4),    # west-of-dateline half
            (-180.0, -20.7, -178.0, -12.4),  # east-of-dateline half
        ],
    },
    "Canary Islands": {
        "elevation": "data/terrain/canary_elevation.tif",
        "population": "data/population/canary_population_clean.tif",
        "boundary": "data/boundaries/canary_islands.gpkg",
        # from data/boundaries/canary_islands.gpkg total_bounds
        "windows": [(-18.17 - BUFFER_DEGREES, 27.64 - BUFFER_DEGREES,
                     -13.42 + BUFFER_DEGREES, 29.24 + BUFFER_DEGREES)],
    },
    "Lakshadweep": {
        "elevation": "data/terrain/lakshadweep_elevation.tif",
        "population": "data/population/lakshadweep_population_clean.tif",
        "boundary": "data/boundaries/lakshadweep_islands.gpkg",
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


def process_bbox(pop_src, elev_src, bbox, boundary_geoms, threshold):
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
        # all_touched=True: count any pixel the polygon touches at all, not
        # just pixels whose center falls inside it. Narrow atoll islands
        # (Maldives, Lakshadweep) are often thinner than a WorldPop pixel,
        # so a center-point test (the geometry_mask default) drops most of
        # their population as "outside the boundary" even though real
        # people live there -- confirmed by comparing against the raw,
        # unmasked population-raster totals (see Dev Log).
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

    elev_window_data = elev_src.read(1, window=elev_window)
    elev_window_transform = elev_src.window_transform(elev_window)

    elev_on_pop_grid = np.empty(pop_shape, dtype="float32")
    reproject(
        source=elev_window_data,
        destination=elev_on_pop_grid,
        src_transform=elev_window_transform,
        src_crs=elev_src.crs,
        dst_transform=pop_transform,
        dst_crs=pop_crs,
        resampling=Resampling.bilinear,
    )

    at_risk_mask = elev_on_pop_grid <= threshold
    return pop_array[at_risk_mask].sum(), pop_array.sum()


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


def population_weighted_exposure(elevation_path, population_path, boundary_path, windows, threshold=1.0):
    total_at_risk = 0.0
    total_pop = 0.0
    skipped_pop = 0.0
    with rasterio.open(population_path) as pop_src, rasterio.open(elevation_path) as elev_src:
        try:
            boundary_geoms = load_boundary_geoms(boundary_path, pop_src.crs)
        except Exception as e:
            print(f"    WARNING: couldn't load boundary polygon ({e}) — falling back to bbox-only, unmasked",
                  flush=True)
            boundary_geoms = None

        for i, bbox in enumerate(windows, start=1):
            print(f"    window {i}/{len(windows)}: {bbox}", flush=True)
            try:
                at_risk, total = process_bbox(pop_src, elev_src, bbox, boundary_geoms, threshold)
                total_at_risk += at_risk
                total_pop += total
            except Exception as e:
                cluster_pop = population_in_bbox(pop_src, bbox, boundary_geoms)
                skipped_pop += cluster_pop
                print(f"    SKIPPED window {i} — elevation file doesn't cover this area "
                      f"({cluster_pop:,.0f} people in this window excluded). Reason: {e}",
                      flush=True)
    if skipped_pop > 0:
        print(f"    NOTE: {skipped_pop:,.0f} people were in areas with no elevation "
              f"coverage and were excluded from this island's percentage.", flush=True)
    percent_at_risk = (total_at_risk / total_pop * 100) if total_pop > 0 else float("nan")
    return total_at_risk, total_pop, percent_at_risk


if __name__ == "__main__":
    print(f"{'Island':<16} {'Pop. at risk':>15} {'Total pop.':>15} {'% at risk':>12}")
    print("-" * 62)
    for island, cfg in ISLANDS.items():
        print(f"  -> {island}...", flush=True)
        try:
            at_risk, total, pct = population_weighted_exposure(
                cfg["elevation"], cfg["population"], cfg["boundary"], cfg["windows"], ELEVATION_THRESHOLD_M
            )
            print(f"{island:<16} {at_risk:>15,.0f} {total:>15,.0f} {pct:>11.1f}%")
        except Exception as e:
            print(f"{island:<16}  ERROR: {e}")
