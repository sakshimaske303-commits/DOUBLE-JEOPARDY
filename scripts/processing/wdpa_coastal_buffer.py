"""Protected-area coverage within a 10 km coastal zone around each island."""
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.ops import unary_union

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]
BUFFER_KM = 10
EQUAL_AREA = "EPSG:6933"
STRICT_IUCN = {"Ia", "Ib", "II", "III", "IV"}

results = []
for island in ISLANDS:
    land = gpd.read_file(f"data/boundaries_v2/{island}_islands_v2.gpkg").to_crs(EQUAL_AREA)
    land_union = unary_union(land.geometry.buffer(0))
    zone = land_union.buffer(BUFFER_KM * 1000)          # land + 10 km of sea
    land_km2 = land_union.area / 1e6
    zone_km2 = zone.area / 1e6

    row = {"island": island, "land_km2": round(land_km2, 2), "coastal_zone_km2": round(zone_km2, 2)}
    try:
        wdpa = gpd.read_file(f"data/ecosystem_buffers/{island}_wdpa.gpkg").to_crs(EQUAL_AREA)
    except Exception:
        wdpa = None

    if wdpa is None or len(wdpa) == 0:
        row.update({"wdpa_sum_km2_overlapping": np.nan, "wdpa_coastal_km2": np.nan,
                    "pct_coastal_zone_protected": np.nan, "pct_coastal_zone_strict_iucn": np.nan,
                    "ratio": np.nan, "wdpa_available": False})
    else:
        clipped = wdpa.geometry.buffer(0).intersection(zone)
        summed = clipped.area.sum() / 1e6                      # old method (double counts overlaps)
        dissolved = unary_union(list(clipped)).area / 1e6       # correct: union first
        strict = wdpa[wdpa.get("IUCN_CAT", pd.Series(dtype=str)).isin(STRICT_IUCN)]
        strict_km2 = (unary_union(list(strict.geometry.buffer(0).intersection(zone))).area / 1e6) if len(strict) else 0.0
        row.update({
            "wdpa_sum_km2_overlapping": round(summed, 2),
            "wdpa_coastal_km2": round(dissolved, 2),
            "pct_coastal_zone_protected": round(dissolved / zone_km2 * 100, 2),
            "pct_coastal_zone_strict_iucn": round(strict_km2 / zone_km2 * 100, 2),
            "ratio": round(dissolved / land_km2, 2),
            "wdpa_available": True,
        })
    results.append(row)
    print(row)

df = pd.DataFrame(results)
df.to_csv("data/wdpa_coastal_normalized.csv", index=False)
print("\nSaved: data/wdpa_coastal_normalized.csv")
