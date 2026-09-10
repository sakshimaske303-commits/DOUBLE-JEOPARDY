
import os
import sys
import time
import requests
import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import polygonize, unary_union

OUTPUT_DIR = "data/boundaries_v2"
BBOX_PAD_DEG = 0.02

ISLAND_WINDOWS = {
    "maldives": [(72.68, -0.69, 73.76, 7.11)],
    "seychelles": [(46.21, -9.76, 56.29, -3.79)],
    "fiji": [
        (176.5, -20.7, 178.25, -16.55), (178.25, -20.7, 180.0, -16.55),
        (176.5, -16.55, 178.25, -12.4), (178.25, -16.55, 180.0, -12.4),
        (-180.0, -20.7, -179.0, -16.55), (-179.0, -20.7, -178.0, -16.55),
        (-180.0, -16.55, -179.0, -12.4), (-179.0, -16.55, -178.0, -12.4),
    ],
    "canary": [(-18.17, 27.64, -13.42, 29.24)],
    "lakshadweep": [(72.17, 8.25, 73.68, 11.69)],
}

UTM_EPSG = {
    "maldives": 32640,
    "seychelles": 32740,
    "fiji": 32760,
    "canary": 32628,
    "lakshadweep": 32643,
}

REFERENCE_LAND_AREA_KM2 = {
    "maldives": None,
    "seychelles": None,
    "fiji": None,
    "canary": None,
    "lakshadweep": None,
}

CONTACT_EMAIL = "sakshimaske303@gmail.com"
OVERPASS_HEADERS = {
    "User-Agent": f"DOUBLE-JEOPARDY-research-boundary-fix/1.3 (contact: {CONTACT_EMAIL})",
}
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def _post_overpass(query, max_retries=4):
    last_error = None
    for endpoint in OVERPASS_ENDPOINTS:
        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.post(
                    endpoint, data={"data": query}, headers=OVERPASS_HEADERS, timeout=280
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("remark"):
                        print(f"    NOTE: Overpass returned a remark (possible partial "
                              f"result): {data['remark'][:200]}")
                    return data
                last_error = f"HTTP {resp.status_code}"
            except Exception as e:
                last_error = str(e)
            wait = 25 * attempt
            print(f"    ({endpoint} attempt {attempt}/{max_retries} failed: {last_error}, "
                  f"waiting {wait}s)")
            time.sleep(wait)
    raise RuntimeError(f"All Overpass endpoints/retries failed. Last error: {last_error}")


def fetch_coastline_ways(min_lon, min_lat, max_lon, max_lat):
    min_lon = max(-180.0, min_lon - BBOX_PAD_DEG)
    min_lat = max(-90.0, min_lat - BBOX_PAD_DEG)
    max_lon = min(180.0, max_lon + BBOX_PAD_DEG)
    max_lat = min(90.0, max_lat + BBOX_PAD_DEG)
    query = f"""
    [out:json][timeout:270];
    (
      way["natural"="coastline"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out body;
    >;
    out skel qt;
    """
    return _post_overpass(query)


def extract_ways(osm_json, seen_way_ids, way_pool):
    nodes = {}
    ways = []
    for el in osm_json.get("elements", []):
        if el["type"] == "node":
            nodes[el["id"]] = (el["lon"], el["lat"])
        elif el["type"] == "way":
            ways.append(el)

    added, duplicates, unusable = 0, 0, 0
    for way in ways:
        way_id = way.get("id")
        if way_id in seen_way_ids:
            duplicates += 1
            continue
        node_ids = way.get("nodes", [])
        if len(node_ids) < 2:
            unusable += 1
            continue
        try:
            coords = [nodes[nid] for nid in node_ids]
            way_pool[way_id] = LineString(coords)
            seen_way_ids.add(way_id)
            added += 1
        except Exception:
            unusable += 1

    return added, duplicates, unusable


def process_island(island, windows):
    print(f"\n=== {island} ===")
    seen_way_ids = set()
    way_pool = {}

    for i, (min_lon, min_lat, max_lon, max_lat) in enumerate(windows, start=1):
        print(f"  window {i}/{len(windows)}: {(min_lon, min_lat, max_lon, max_lat)}")
        osm_json = fetch_coastline_ways(min_lon, min_lat, max_lon, max_lat)
        added, dup, unusable = extract_ways(osm_json, seen_way_ids, way_pool)
        print(f"    +{added} new ways ({dup} already seen from another window, "
              f"{unusable} unusable)")
        time.sleep(8)

    if not way_pool:
        print(f"  WARNING: no coastline ways found for {island} at all.")
        return

    polygons = [p for p in polygonize(list(way_pool.values())) if p.is_valid and p.area > 0]
    print(f"  {len(way_pool)} unique ways total -> {len(polygons)} closed rings assembled")

    if not polygons:
        print(f"  WARNING: ways were fetched but no closed rings formed for {island}.")
        return

    dissolved = unary_union(polygons)
    gdf = gpd.GeoDataFrame(geometry=[dissolved], crs="EPSG:4326").explode(index_parts=False)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{island}_islands_v2.gpkg")
    gdf.to_file(out_path, driver="GPKG")

    utm_epsg = UTM_EPSG[island]
    area_v2_km2 = gdf.to_crs(epsg=utm_epsg).geometry.area.sum() / 1e6

    v1_path = f"data/boundaries/{island}_islands.gpkg"
    area_v1_km2 = None
    if os.path.exists(v1_path):
        try:
            gdf_v1 = gpd.read_file(v1_path).to_crs(epsg=utm_epsg)
            area_v1_km2 = gdf_v1.geometry.area.sum() / 1e6
        except Exception as e:
            print(f"  (could not read v1 file for comparison: {e})")

    ref = REFERENCE_LAND_AREA_KM2.get(island)
    print(f"  Saved: {out_path}")
    print(f"  v1 (old) area: {area_v1_km2:.2f} km2" if area_v1_km2 is not None else "  v1 (old) area: n/a")
    print(f"  new area: {area_v2_km2:.2f} km2  ({len(gdf)} polygons)")
    print(f"  cited reference area: {ref if ref is not None else 'NOT FILLED IN YET -- see script header'}")
    if area_v1_km2 is not None and area_v2_km2 < area_v1_km2:
        print(f"  *** REGRESSION WARNING: new area ({area_v2_km2:.2f} km2) is SMALLER than v1 "
              f"({area_v1_km2:.2f} km2). Do NOT use this for {island} yet. ***")
    else:
        print(f"  OK: new area is >= v1 -- looks like a real improvement, but still confirm "
              f"against a cited reference figure before using it in the paper.")


def main():
    requested = [a.lower() for a in sys.argv[1:]] or list(ISLAND_WINDOWS.keys())
    unknown = [a for a in requested if a not in ISLAND_WINDOWS]
    if unknown:
        print(f"Unknown island name(s): {unknown}. Valid names: {list(ISLAND_WINDOWS.keys())}")
        return

    failures = []
    for island in requested:
        try:
            process_island(island, ISLAND_WINDOWS[island])
        except Exception as e:
            print(f"\n=== {island} FAILED: {e} ===")
            failures.append(island)
            continue

    print("\nDone. Send back the data/boundaries_v2/*.gpkg files plus this")
    print("console output.")
    if failures:
        print(f"These islands FAILED and have no v2 file yet: {failures}. Re-run just "
              f"those, e.g.: python rebuild_boundary_polygons_osm.py {' '.join(failures)}")


if __name__ == "__main__":
    main()
