"""NOAA Coral Reef Watch DHW averaged over the 5 km cells that actually
contain mapped coral reef, per island.

Added 2026-10-10 after the Forensic Review. The existing series use one
hand-picked 5 km cell per island (data/coral_bleaching) or a +-0.15 deg box
around it (data/coral_bleaching_v2). Neither is tied to where the reefs are,
and the Maldives and Seychelles reef systems span hundreds of kilometres.
This script:
  1. reads the mapped reef polygons in data/ecosystem_buffers/<island>_coral_clean.gpkg
  2. finds every 0.05 deg DHW cell those polygons touch
  3. downloads DHW for each 1 x 1 deg block that contains reef (ERDDAP griddap),
     keeps only reef cells, and writes:
       data/coral_bleaching_v3/<island>_dhw_reefcells_raw.csv   (time, lat, lon, dhw)
       data/coral_bleaching_v3/<island>_dhw_reefcells_mean.csv  (time, dhw_mean,
            dhw_p90, pct_cells_ge4, pct_cells_ge8, n_cells)
The Canary Islands are skipped: no coral reefs are mapped there.

TIME_STRIDE_DAYS = 30 keeps comparability with the earlier series; 7 captures
annual peaks better (annual maximum DHW is the standard bleaching metric).
Needs geopandas, numpy, pandas, requests, rasterio.

Robust to NOAA server errors (updated after the first run hit many 502s):
  * each 1-degree block is requested in 5-year pieces (smaller, faster requests)
  * every piece is cached in data/coral_bleaching_v3/blocks/ as soon as it
    arrives, so a re-run only fetches what is still missing
  * up to 6 attempts per piece with growing waits (15 s, 30 s, 60 s ...)
  * the per-island mean file is written ONLY when every block is complete;
    otherwise the script lists what is missing. Just run it again later
    (NOAA ERDDAP is often overloaded in US daytime; Indian night-time works better).
"""
import io
import math
import os
import time

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from rasterio.features import rasterize
from rasterio.transform import from_origin

ERDDAP = "https://coastwatch.noaa.gov/erddap/griddap/noaacrwdhwDaily"
ISLANDS = ["maldives", "seychelles", "fiji", "lakshadweep"]
START, END = "1996-01-01", "2020-12-31"
TIME_STRIDE_DAYS = 30
CELL = 0.05
OUT_DIR = "data/coral_bleaching_v3"
HEADERS = {"User-Agent": "Mozilla/5.0 (research script; DOUBLE JEOPARDY)"}


def reef_cells(island):
    reefs = gpd.read_file(f"data/ecosystem_buffers/{island}_coral_clean.gpkg").to_crs(epsg=4326)
    reefs = reefs[reefs.geometry.notnull() & ~reefs.geometry.is_empty]
    cells = set()
    for geom in reefs.geometry:
        minx, miny, maxx, maxy = geom.bounds
        x0, y1 = math.floor(minx / CELL) * CELL, math.ceil(maxy / CELL) * CELL
        w = max(1, int(round((math.ceil(maxx / CELL) * CELL - x0) / CELL)))
        h = max(1, int(round((y1 - math.floor(miny / CELL) * CELL) / CELL)))
        m = rasterize([(geom, 1)], out_shape=(h, w), transform=from_origin(x0, y1, CELL, CELL),
                      all_touched=True, dtype="uint8")
        for r, c in zip(*np.nonzero(m)):
            lon = round(x0 + (c + 0.5) * CELL, 3)
            lat = round(y1 - (r + 0.5) * CELL, 3)
            cells.add((lat, lon))
    return cells


YEAR_CHUNKS = [("1996-01-01", "2000-12-31"), ("2001-01-01", "2005-12-31"), ("2006-01-01", "2010-12-31"),
               ("2011-01-01", "2015-12-31"), ("2016-01-01", "2020-12-31")]
MAX_ATTEMPTS = 6
CACHE_DIR = os.path.join(OUT_DIR, "blocks")


def fetch_piece(lat0, lon0, start, end):
    """One 1-degree block for one 5-year piece, cached on disk."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.join(CACHE_DIR, f"{lat0}_{lon0}_{start[:4]}_{end[:4]}_s{TIME_STRIDE_DAYS}.csv")
    if os.path.exists(cache) and os.path.getsize(cache) > 0:
        return pd.read_csv(cache)
    url = (f"{ERDDAP}.csv?degree_heating_week[({start}):{TIME_STRIDE_DAYS}:({end})]"
           f"[({lat0}):1:({lat0 + 0.999})][({lon0}):1:({lon0 + 0.999})]")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=300)
            r.raise_for_status()
            df = pd.read_csv(io.StringIO(r.text), skiprows=[1])
            df.columns = [c.strip().lower() for c in df.columns]
            df = df.rename(columns={"degree_heating_week": "dhw"})
            df.to_csv(cache, index=False)
            return df
        except Exception as e:
            wait = 15 * 2 ** (attempt - 1)
            print(f"    block {lat0},{lon0} {start[:4]}-{end[:4]} attempt {attempt} failed "
                  f"({str(e)[:60]}); waiting {wait}s")
            time.sleep(wait)
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for island in ISLANDS:
        cells = reef_cells(island)
        blocks = sorted({(math.floor(lat), math.floor(lon)) for lat, lon in cells})
        print(f"{island}: {len(cells)} reef cells in {len(blocks)} one-degree blocks")
        parts, missing = [], []
        for lat0, lon0 in blocks:
            for start, end in YEAR_CHUNKS:
                df = fetch_piece(lat0, lon0, start, end)
                if df is None:
                    missing.append(f"{lat0},{lon0} {start[:4]}-{end[:4]}")
                    continue
                df["key"] = list(zip(df["latitude"].round(3), df["longitude"].round(3)))
                parts.append(df[df["key"].isin(cells)].drop(columns="key"))
                time.sleep(1)
        if missing:
            print(f"  INCOMPLETE: {len(missing)} block pieces still missing: {missing}")
            print("  Not writing the mean file. Run this script again later; finished pieces are cached.")
            for stale in (f"{OUT_DIR}/{island}_dhw_reefcells_mean.csv", f"{OUT_DIR}/{island}_dhw_reefcells_raw.csv"):
                if os.path.exists(stale):  # an older, partial file must not be used by coral_trend_test.py
                    os.remove(stale)
                    print(f"  removed stale partial file {stale}")
            continue
        if not parts:
            print("  nothing downloaded")
            continue
        raw = pd.concat(parts, ignore_index=True)
        # ERDDAP snaps request edges to the nearest grid cell, so a cell on the
        # border of two 1-degree blocks can come back twice. Keep one copy.
        before = len(raw)
        raw = raw.drop_duplicates(subset=["time", "latitude", "longitude"])
        if len(raw) < before:
            print(f"  removed {before - len(raw)} duplicate border-cell rows")
        raw.to_csv(f"{OUT_DIR}/{island}_dhw_reefcells_raw.csv", index=False)
        g = raw.dropna(subset=["dhw"]).groupby("time")["dhw"]
        mean = pd.DataFrame({
            "dhw_mean": g.mean(), "dhw_p90": g.quantile(0.9),
            "pct_cells_ge4": g.apply(lambda v: (v >= 4).mean() * 100),
            "pct_cells_ge8": g.apply(lambda v: (v >= 8).mean() * 100),
            "n_cells": g.size(),
        }).reset_index()
        mean.to_csv(f"{OUT_DIR}/{island}_dhw_reefcells_mean.csv", index=False)
        print(f"  saved {len(mean)} time steps, median {int(mean['n_cells'].median())} valid reef cells")


if __name__ == "__main__":
    main()
