"""Turn the Overture building footprints (data/buildings/*.parquet) into one compact
point table per island: centroid, footprint area and source dataset.

Run from the repository root:
    python scripts/processing/export_building_points.py
"""
import glob
import os

import geopandas as gpd
import pandas as pd

GROUPS = {
    "maldives": ["maldives"], "lakshadweep": ["lakshadweep"], "seychelles": ["seychelles"],
    "fiji": ["fiji_west", "fiji_east"], "canary": ["canary"],
}


def first_source(s):
    """Overture 'sources' is a list of records; keep the dataset of the first one."""
    try:
        if s is None or len(s) == 0:
            return ""
        rec = s[0]
        return str(rec.get("dataset", "")) if hasattr(rec, "get") else str(rec)
    except Exception:
        return ""


for island, parts in GROUPS.items():
    frames = []
    for part in parts:
        path = f"data/buildings/{part}_buildings.parquet"
        if not os.path.exists(path):
            print(f"missing {path}")
            continue
        gdf = gpd.read_parquet(path)
        if gdf.crs is None:
            gdf = gdf.set_crs(4326)
        gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
        pts = gdf.geometry.representative_point()          # always inside the footprint
        area = gdf.geometry.to_crs(6933).area
        src = gdf["sources"].apply(first_source) if "sources" in gdf.columns else ""
        frames.append(pd.DataFrame({"id": gdf.get("id", pd.Series(range(len(gdf)))).values,
                                    "lon": pts.x.round(6).values, "lat": pts.y.round(6).values,
                                    "area_m2": area.round(1).values, "source": src.values}))
    if frames:
        out = pd.concat(frames, ignore_index=True).drop_duplicates(subset="id")
        dest = f"data/buildings/{island}_building_points.csv.gz"
        out.to_csv(dest, index=False, compression="gzip")
        print(f"{island}: {len(out):,} buildings -> {dest}  sources: {out['source'].value_counts().to_dict()}")
