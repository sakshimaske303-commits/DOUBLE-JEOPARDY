import geopandas as gpd
import pandas as pd

ISLANDS = ["maldives", "seychelles", "fiji", "canary", "lakshadweep"]
BUFFER_KM = 10

results = []
for island in ISLANDS:
    boundary = gpd.read_file(f"data/boundaries/{island}_islands.gpkg").to_crs("EPSG:6933")
    coastal_buffer = boundary.buffer(BUFFER_KM * 1000).unary_union

    island_area_km2 = boundary.geometry.area.sum() / 1_000_000

    if island == "lakshadweep":
        wdpa_in_buffer_km2 = 0.0
    else:
        wdpa = gpd.read_file(f"data/ecosystem_buffers/{island}_wdpa.gpkg").to_crs("EPSG:6933")
        wdpa_clipped = wdpa.intersection(coastal_buffer)
        wdpa_in_buffer_km2 = wdpa_clipped.area.sum() / 1_000_000

    ratio = (wdpa_in_buffer_km2 / island_area_km2) if island_area_km2 > 0 else 0

    results.append({"island": island, "wdpa_coastal_km2": round(wdpa_in_buffer_km2, 2), "ratio": round(ratio, 2)})
    print(f"{island.upper()}: WDPA-within-{BUFFER_KM}km-coastal-buffer = {wdpa_in_buffer_km2:.2f} km2, ratio={ratio:.2f}")

df = pd.DataFrame(results)
df.to_csv("data/wdpa_coastal_normalized.csv", index=False)
print("\nSaved: data/wdpa_coastal_normalized.csv")