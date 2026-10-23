"""Land area of each island boundary (data/boundaries_v2) against an independent
reference figure. Written for the paper's Section 6.3, so the validation numbers come
from a script rather than being typed in.
"""
import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union

# Reference land areas (km2) and their sources, as cited in the paper.
REFERENCE = {
    "maldives": (298, "World Bank (2024), WDI AG.LND.TOTL.K2, 2023 value"),
    "seychelles": (460, "World Bank (2024), WDI AG.LND.TOTL.K2, 2023 value"),
    "fiji": (18270, "World Bank (2024), WDI AG.LND.TOTL.K2, 2023 value"),
    "canary": (7446, "Instituto Canario de Estadistica (2026)"),
    "lakshadweep": (32, "Administration of UT of Lakshadweep"),
}

rows = []
for island, (ref_km2, source) in REFERENCE.items():
    gdf = gpd.read_file(f"data/boundaries_v2/{island}_islands_v2.gpkg").to_crs("EPSG:6933")
    area = unary_union(gdf.geometry.buffer(0)).area / 1e6
    rows.append({"island": island, "boundary_km2": round(area, 1), "reference_km2": ref_km2,
                 "difference_pct": round((area - ref_km2) / ref_km2 * 100, 1), "reference_source": source})

out = pd.DataFrame(rows)
print(out.to_string(index=False))
out.to_csv("data/boundary_area_validation.csv", index=False)
print("Saved: data/boundary_area_validation.csv")
