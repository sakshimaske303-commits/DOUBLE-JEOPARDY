"""SUPERSEDED — not used by any current analysis. Divides compute_wdpa_area.py's
marine+terrestrial-mixed WDPA area by land-only island area, which is what
produced the impossible 1005.69 ratio for Seychelles (see compute_wdpa_area.py
and DJ_Development_Log.md). Replaced by wdpa_coastal_buffer.py's 10km-buffer
approach; data/wdpa_normalized.csv below is kept only as a record of the bug,
not read by governance_correlation_test.py or anything else downstream.
"""

import geopandas as gpd
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]

wdpa_df = pd.read_csv("data/wdpa_area_by_island.csv").set_index("island")

results = []
for island in ISLANDS:
    boundary_path = f"data/boundaries/{island}_islands.gpkg"
    gdf = gpd.read_file(boundary_path)
    gdf_proj = gdf.to_crs("EPSG:6933")
    island_area_km2 = gdf_proj.geometry.area.sum() / 1_000_000

    wdpa_area = wdpa_df.loc[island, "wdpa_area_km2"]
    ratio = (wdpa_area / island_area_km2) if island_area_km2 > 0 else 0

    results.append({
        "island": island,
        "island_land_area_km2": round(island_area_km2, 2),
        "wdpa_area_km2": wdpa_area,
        "wdpa_ratio": round(ratio, 2),
    })
    print(f"{island.upper()}: land={island_area_km2:.2f} km2, WDPA={wdpa_area:.2f} km2, ratio={ratio:.2f}")

df = pd.DataFrame(results)
df.to_csv("data/wdpa_normalized.csv", index=False)
print("\nSaved: data/wdpa_normalized.csv")