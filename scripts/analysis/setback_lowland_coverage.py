"""Share of low-lying LAND (not buildings) that lies within each coastal setback.

The building measure in setback_calibration.py is judged on today's building stock, much of which
predates the rules. A setback governs where new buildings may go, so the land it covers is the
measure that does not depend on what has already been built. This script lays a regular grid of
points over every island polygon, samples bare-earth elevation with the same rule as the building
analysis (DeltaDTM v1.1, Copernicus GLO-30 where DeltaDTM is empty and Copernicus is above 10 m, or
where Copernicus is above 30 m), measures each point's distance to the shoreline, and reports the
share of land at or below 1 m that lies within 20, 25 and 100 m and within each statutory setback.
It also repeats the shares for low land with no building point within 20 m ("open low land"),
which is where a setback would decide future siting.

Run from the repository root (needs the DeltaDTM and Copernicus tiles in data/terrain and the
building points in data/buildings):
    python scripts/analysis/setback_lowland_coverage.py
Optional: --spacing-m 30 (default 30 m for atolls and Seychelles, 60 m for Fiji and the Canary Islands)
Optional: --islands fiji canary (rows for other islands already in the CSV are kept)
Writes data/setback_lowland_coverage.csv and data/setback_lowland_curve.csv.
"""
import os, sys, time, argparse, numpy as np, pandas as pd
from matplotlib.path import Path
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import setback_calibration as sc   # reuses the GeoPackage reader, elevation rule and shoreline distance

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=".")
ap.add_argument("--spacing-m", type=float, default=None)
ap.add_argument("--islands", nargs="*", default=sc.ISLANDS)
args = ap.parse_args()
sc.D = os.path.join(args.root, "data")
D = sc.D
SPACING = {"maldives": 30, "lakshadweep": 30, "seychelles": 30, "fiji": 60, "canary": 60}
WIDTHS = [10, 20, 25, 50, 100, 150, 200, 300, 500]
MAX_DIST_M = 1000.0


def grid_on_land(polys, spacing_m, wrap):
    """Regular lon/lat grid inside the island polygons (holes removed). The polygons are filled into
    an image once (PIL), which is far faster than testing every point against every polygon."""
    from PIL import Image as _Img, ImageDraw
    if wrap:
        polys = [[np.c_[np.where(r[:, 0] < 0, r[:, 0] + 360, r[:, 0]), r[:, 1]] for r in p] for p in polys]
    allpts = np.vstack([p[0] for p in polys])
    x0, y0 = allpts.min(0); x1, y1 = allpts.max(0)
    lat0 = (y0 + y1) / 2
    dlat = spacing_m / 110574.0
    dlon = spacing_m / (111320 * np.cos(np.radians(lat0)))
    ncol = int(np.ceil((x1 - x0) / dlon)) + 1; nrow = int(np.ceil((y1 - y0) / dlat)) + 1
    img = _Img.new("L", (ncol, nrow), 0); dr = ImageDraw.Draw(img)
    def px(r):
        return list(zip(((r[:, 0] - x0) / dlon).tolist(), ((y1 - r[:, 1]) / dlat).tolist()))
    for p in polys:
        if len(p[0]) >= 3:
            dr.polygon(px(p[0]), fill=1)
            for h in p[1:]:
                if len(h) >= 3:
                    dr.polygon(px(h), fill=0)
    m = np.asarray(img, dtype=np.uint8); del img
    rr, cc = np.nonzero(m); del m
    lon = x0 + (cc + 0.5) * dlon; lat = y1 - (rr + 0.5) * dlat
    if wrap:
        lon = np.where(lon > 180, lon - 360, lon)
    return lon, lat


def coast_distance(polys, lon, lat, wrap):
    """Distance (m) from each point to the densified polygon edge; same geometry as setback_calibration."""
    if wrap:
        lon = np.where(lon < 0, lon + 360, lon)
        polys = [[np.c_[np.where(r[:, 0] < 0, r[:, 0] + 360, r[:, 0]), r[:, 1]] for r in p] for p in polys]
    lat0 = np.nanmean(lat); kx = 111320 * np.cos(np.radians(lat0)); ky = 110574.0
    pts = []
    for p in polys:
        for r in p:
            x, y = r[:, 0] * kx, r[:, 1] * ky
            seg = np.hypot(np.diff(x), np.diff(y)); n = np.maximum(np.ceil(seg / 5.0).astype(int), 1)
            starts = np.repeat(np.c_[x[:-1], y[:-1]], n, axis=0)
            ends = np.repeat(np.c_[x[1:], y[1:]], n, axis=0)
            f = (np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)) / np.repeat(n, n)
            pts.append(starts + f[:, None] * (ends - starts))
    tree = cKDTree(np.vstack(pts))
    # only distances up to MAX_DIST_M matter for setbacks; farther points come back as inf
    d, _ = tree.query(np.c_[lon * kx, lat * ky], workers=-1, distance_upper_bound=MAX_DIST_M)
    return d


def inside_exact(polys, lon, lat, wrap):
    """Exact point-in-polygon test (holes removed), used only for grid points next to the shoreline,
    where the image fill can include cells whose centre lies just offshore."""
    if wrap:
        lon = np.where(lon < 0, lon + 360, lon)
        polys = [[np.c_[np.where(r[:, 0] < 0, r[:, 0] + 360, r[:, 0]), r[:, 1]] for r in p] for p in polys]
    ins_all = np.zeros(lon.shape, bool)
    for p in polys:
        ext = p[0]; x0, y0 = ext.min(0); x1, y1 = ext.max(0)
        cand = np.flatnonzero((lon >= x0) & (lon <= x1) & (lat >= y0) & (lat <= y1) & ~ins_all)
        if not len(cand):
            continue
        q = np.c_[lon[cand], lat[cand]]; ins = Path(ext).contains_points(q)
        for h in p[1:]:
            ins &= ~Path(h).contains_points(q)
        ins_all[cand[ins]] = True
    return ins_all


def open_land(lon, lat, b, radius_m=20.0):
    """True where no building point lies within radius_m."""
    if b is None or not len(b):
        return np.ones(lon.shape, bool)
    lat0 = np.nanmean(lat); kx = 111320 * np.cos(np.radians(lat0)); ky = 110574.0
    bl = np.where(b.lon.values < 0, b.lon.values + 360, b.lon.values) if (lon < 0).any() and (lon > 0).any() else b.lon.values
    gl = np.where(lon < 0, lon + 360, lon) if (lon < 0).any() and (lon > 0).any() else lon
    tree = cKDTree(np.c_[bl * kx, b.lat.values * ky])
    d, _ = tree.query(np.c_[gl * kx, lat * ky], workers=-1, distance_upper_bound=radius_m)
    return ~np.isfinite(d)


rows, curves = [], []
for isl in args.islands:
    gpkg = os.path.join(D, f"boundaries_v2/{isl}_islands_v2.gpkg")
    if not os.path.exists(gpkg):
        print(f"{isl}: {gpkg} missing"); continue
    spacing = args.spacing_m or SPACING[isl]
    polys = sc.polygons(gpkg)
    t0 = time.time()
    lon, lat = grid_on_land(polys, spacing, wrap=(isl == "fiji"))
    print(f"{isl}: {len(lon):,} land points at {spacing:.0f} m ({time.time() - t0:.0f} s)", flush=True)
    dist = coast_distance(polys, lon, lat, wrap=(isl == "fiji"))
    edge = np.flatnonzero(dist < spacing)               # cells the shoreline passes through or next to
    keep = np.ones(lon.shape, bool)
    keep[edge] = inside_exact(polys, lon[edge], lat[edge], wrap=(isl == "fiji"))
    lon, lat, dist = lon[keep], lat[keep], dist[keep]
    land = np.ones(lon.shape, bool)
    print(f"{isl}: shoreline distance done ({time.time() - t0:.0f} s)", flush=True)
    z, src, cv = sc.elevation(isl, lon, lat)
    print(f"{isl}: elevation done ({time.time() - t0:.0f} s)", flush=True)
    ok = land & np.isfinite(z)
    bf = os.path.join(D, f"buildings/{isl}_building_points.csv.gz")
    bpts = pd.read_csv(bf, usecols=["lon", "lat"]) if os.path.exists(bf) else None
    opn = open_land(lon, lat, bpts)
    cell_km2 = (spacing / 1000.0) ** 2
    low = ok & (z <= sc.THR)
    for variant, mask in (("all_low_land", low), ("open_low_land", low & opn)):
        n = int(mask.sum())
        r = dict(island=sc.LABEL[isl], variant=variant, spacing_m=spacing,
                 land_points=int(land.sum()), land_points_with_elevation=int(ok.sum()),
                 low_points=n, low_land_km2=round(n * cell_km2, 2),
                 low_land_pct_of_land=round(100 * low.sum() / max(ok.sum(), 1), 2),
                 statutory_setback_m="/".join(map(str, sc.SETBACK[isl])) or "none",
                 low_land_median_dist_m=round(float(np.median(dist[mask])), 1) if n else np.nan)
        for w in (20, 25, 100):
            r[f"pct_low_land_within_{w}m"] = round(100 * (dist[mask] <= w).mean(), 2) if n else np.nan
        sb = sc.SETBACK[isl]
        r["pct_low_land_within_statutory_setback"] = round(100 * (dist[mask] <= max(sb)).mean(), 2) if (n and sb) else np.nan
        rows.append(r)
        for w in WIDTHS:
            curves.append(dict(island=sc.LABEL[isl], variant=variant, distance_m=w,
                               pct_low_land_within=round(100 * (dist[mask] <= w).mean(), 2) if n else np.nan))
        print(f"{isl:12s} {variant:14s} low land {r['low_land_km2']:8.2f} km2  within 20 m {r['pct_low_land_within_20m']}%  "
              f"within statutory {r['pct_low_land_within_statutory_setback']}", flush=True)

if rows:
    done = {r["island"] for r in rows}
    for name, new in (("setback_lowland_coverage.csv", rows), ("setback_lowland_curve.csv", curves)):
        path = os.path.join(D, name); new = pd.DataFrame(new)
        if os.path.exists(path):
            old = pd.read_csv(path); new = pd.concat([old[~old["island"].isin(done)], new], ignore_index=True)
        order = {sc.LABEL[i]: k for k, i in enumerate(sc.ISLANDS)}
        new = new.sort_values(["island"], key=lambda c: c.map(order), kind="stable")
        new.to_csv(path, index=False)
    print("wrote data/setback_lowland_coverage.csv and data/setback_lowland_curve.csv")
