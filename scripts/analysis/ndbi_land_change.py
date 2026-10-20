"""Built-up (NDBI) change 2016 -> 2024 measured on LAND only, from the
cloud-masked annual NDBI rasters (download_ndbi_encroachment_raster.py:
Sentinel-2 L2A, SCL cloud/shadow/cirrus masked, ORBIT mosaicking).

Added 2026-10-10 after the Forensic Review. The numbers previously reported in
the paper (Fiji -0.0008, Maldives +0.0461, Seychelles +0.1135) come from
analyze_ndbi_change.py, which averages Statistical-API half-year composites
over the whole bounding box with no cloud or water mask. Those boxes are
99.7% ocean (Maldives), 85% (Seychelles) and 30% (Fiji), and the half-year
values differ by up to 0.22 within one year, more than the 2016->2024 change.
Using these masked rasters instead, the forensic check found:
  bbox mean change   Fiji -0.027, Maldives +0.012, Seychelles -0.033
  land-only change   Fiji -0.011, Maldives +0.044, Seychelles -0.0003

This script reports, per island:
  * land-only mean NDBI in 2016 and 2024 and the change
  * share of land pixels with change > +DELTA and < -DELTA
  * the same restricted to land within BUFFER_M of mapped mangrove/coral
    polygons (the "near ecosystem buffer" question the paper actually asks)
  * a bootstrap 95% interval of the mean land change (resampling pixels in
    BLOCK x BLOCK blocks to respect spatial autocorrelation)

Run from the repository root. Needs rasterio, geopandas, numpy, pandas.
"""
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize

ISLANDS = ["maldives", "seychelles", "fiji"]
DELTA = 0.10
BUFFER_M = 1000
BLOCK = 16
N_BOOT = 2000
ECOSYSTEM_FILES = {
    "maldives": ["data/ecosystem_buffers/maldives_mangroves_clean.gpkg", "data/ecosystem_buffers/maldives_coral_clean.gpkg"],
    "seychelles": ["data/ecosystem_buffers/seychelles_mangroves_clean.gpkg", "data/ecosystem_buffers/seychelles_coral_clean.gpkg"],
    "fiji": ["data/ecosystem_buffers/fiji_mangroves_clean.gpkg", "data/ecosystem_buffers/fiji_coral_clean.gpkg"],
}


def mask_from(gdf, transform, shape):
    geoms = [g for g in gdf.geometry if g is not None and not g.is_empty]
    if not geoms:
        return np.zeros(shape, bool)
    return rasterize([(g, 1) for g in geoms], out_shape=shape, transform=transform, fill=0,
                     dtype="uint8", all_touched=True).astype(bool)


def block_bootstrap_mean(diff, mask, rng):
    h, w = diff.shape
    blocks = []
    for r in range(0, h, BLOCK):
        for c in range(0, w, BLOCK):
            m = mask[r:r + BLOCK, c:c + BLOCK]
            if m.any():
                d = diff[r:r + BLOCK, c:c + BLOCK][m]
                d = d[np.isfinite(d)]
                if d.size:
                    blocks.append((d.sum(), d.size))
    if len(blocks) < 2:
        return np.nan, np.nan
    sums, counts = np.array(blocks).T
    idx = rng.integers(0, len(blocks), size=(N_BOOT, len(blocks)))
    means = sums[idx].sum(1) / counts[idx].sum(1)
    return np.percentile(means, 2.5), np.percentile(means, 97.5)


def main():
    rng = np.random.default_rng(42)
    rows = []
    for island in ISLANDS:
        with rasterio.open(f"data/settlement_encroachment/{island}_ndbi_2016.tif") as s16, \
             rasterio.open(f"data/settlement_encroachment/{island}_ndbi_2024.tif") as s24:
            a16 = s16.read(1).astype("float64")
            a24 = s24.read(1).astype("float64")
            transform, shape, crs = s16.transform, a16.shape, s16.crs
        diff = a24 - a16

        land = gpd.read_file(f"data/boundaries_v2/{island}_islands_v2.gpkg").to_crs(crs)
        land_mask = mask_from(land, transform, shape)

        eco = [gpd.read_file(f) for f in ECOSYSTEM_FILES[island] if os.path.exists(f)]
        near_mask = np.zeros(shape, bool)
        if eco:
            eco_gdf = pd.concat([e.to_crs("EPSG:6933") for e in eco])
            near = gpd.GeoSeries(eco_gdf.geometry.buffer(BUFFER_M), crs="EPSG:6933").to_crs(crs)
            near_mask = mask_from(gpd.GeoDataFrame(geometry=near), transform, shape) & land_mask

        for zone, m in [("all_land", land_mask), (f"land_within_{BUFFER_M}m_of_ecosystems", near_mask)]:
            ok = m & np.isfinite(diff)
            if ok.sum() == 0:
                continue
            lo, hi = block_bootstrap_mean(diff, ok, rng)
            rows.append({
                "island": island, "zone": zone, "pixels": int(ok.sum()),
                "land_fraction_of_bbox": float(land_mask.mean()),
                "ndbi_2016": float(np.nanmean(a16[ok])), "ndbi_2024": float(np.nanmean(a24[ok])),
                "mean_change": float(np.nanmean(diff[ok])), "ci95_low": lo, "ci95_high": hi,
                f"pct_pixels_up_gt_{DELTA}": float((diff[ok] > DELTA).mean() * 100),
                f"pct_pixels_down_gt_{DELTA}": float((diff[ok] < -DELTA).mean() * 100),
            })
            print(rows[-1])

    pd.DataFrame(rows).to_csv("data/ndbi_land_change.csv", index=False)
    print("Saved: data/ndbi_land_change.csv")


if __name__ == "__main__":
    main()
