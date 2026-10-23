"""Building-level coastal setback calibration: share of buildings at or below 1 m that
stand landward of each statutory setback.

Run from the repository root:
    python scripts/analysis/setback_calibration.py
"""
import sys, os, glob, re, struct, sqlite3, numpy as np, pandas as pd
from PIL import Image
from matplotlib.path import Path
from scipy.spatial import cKDTree
Image.MAX_IMAGE_PIXELS = None
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
D = os.path.join(ROOT, "data")
PLOTS = os.path.join(ROOT, "outputs", "plots")
ISLANDS = ["maldives", "lakshadweep", "seychelles", "fiji", "canary"]
LABEL = {"maldives": "Maldives", "lakshadweep": "Lakshadweep", "seychelles": "Seychelles",
         "fiji": "Fiji", "canary": "Canary Islands"}
COLOR = {"maldives": "#2c7fb8", "seychelles": "#e34a33", "fiji": "#31a354",
         "canary": "#756bb1", "lakshadweep": "#fd8d3c"}
SETBACK = {"canary": [100, 20], "seychelles": [25], "lakshadweep": [20], "maldives": [], "fiji": []}
THR = 1.0  # m above EGM2008

# ---------- GeoPackage reader (sqlite + WKB) ----------
def parse_wkb(b, o=0):
    bo = '<' if b[o] == 1 else '>'; t = struct.unpack(bo+'I', b[o+1:o+5])[0]; o += 5
    dims = 2; base = t
    if t > 1000: base = t % 1000; dims = 3 if t//1000 in (1, 2) else 4
    if t & 0x80000000: base = t & 0xFFFF; dims = 3
    def ring(o):
        n = struct.unpack(bo+'I', b[o:o+4])[0]; o += 4
        a = np.frombuffer(b, dtype=np.dtype(bo+'f8'), count=n*dims, offset=o).reshape(n, dims)[:, :2]
        return a, o + n*dims*8
    if base == 3:
        nr = struct.unpack(bo+'I', b[o:o+4])[0]; o += 4; rs = []
        for _ in range(nr): r, o = ring(o); rs.append(r)
        return [rs], o
    if base in (6, 7):
        n = struct.unpack(bo+'I', b[o:o+4])[0]; o += 4; ps = []
        for _ in range(n): g, o = parse_wkb(b, o); ps += g
        return ps, o
    return [], o
def polygons(path):
    con = sqlite3.connect(path)
    tn, gc = con.execute("select table_name,column_name from gpkg_geometry_columns").fetchone()
    P = []
    for (blob,) in con.execute(f'select "{gc}" from "{tn}"'):
        if blob is None: continue
        env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
        P += parse_wkb(blob, 8 + env)[0]
    return P

# ---------- raster sampling ----------
def sample_files(files, lon, lat):
    out = np.full(lon.shape, np.nan)
    for f in files:
        im = Image.open(f); t = im.tag_v2
        ox, oy = t[33922][3], t[33922][4]; rx, ry = t[33550][0], t[33550][1]
        w, h = im.size
        c = np.floor((lon-ox)/rx).astype(int); r = np.floor((oy-lat)/ry).astype(int)
        ok = (c >= 0) & (c < w) & (r >= 0) & (r < h) & np.isnan(out)
        if not ok.any(): continue
        a = np.array(im).astype("float32")
        v = a[r[ok], c[ok]]
        nd = t.get(42113)
        if nd not in (None, ''): v[v == float(nd)] = np.nan
        v[(v <= -1000) | (v == 0.0) | ~np.isfinite(v)] = np.nan
        idx = np.flatnonzero(ok); out[idx] = np.where(np.isfinite(v), v, np.nan)
        del a
    return out
def tile_ok(name, lon, lat):
    m = re.search(r'([NS])(\d{2})_?0?0?_?([EW])(\d{3})', name.replace("_00_", "_"))
    if not m: return True
    la = int(m[2]) * (1 if m[1] == 'N' else -1); lo = int(m[4]) * (1 if m[3] == 'E' else -1)
    # DeltaDTM names tiles by lower-left corner, Copernicus by lower-left too (N28 = 28..29)
    return ((lon >= lo-0.01) & (lon < lo+1.01) & (lat >= la-0.01) & (lat < la+1.01)).any()
def elevation(isl, lon, lat):
    dd = [f for f in sorted(glob.glob(os.path.join(D, "terrain/deltadtm/gee/*.tif"))) if tile_ok(os.path.basename(f), lon, lat)]
    cp = [f for f in sorted(glob.glob(os.path.join(D, f"terrain/raw_tiles/{isl}/*.tif"))) if tile_ok(os.path.basename(f), lon, lat)]
    dv = sample_files(dd, lon, lat); cv = sample_files(cp, lon, lat)
    v = np.where((np.isnan(dv) & (cv > 10)) | (cv > 30), cv, dv)
    src = np.where(np.isnan(v), "none", np.where(v == cv, "copernicus", "deltadtm"))
    return v, src, cv

# ---------- coastline distance & on-land ----------
def coast_and_land(polys, lon, lat, wrap):
    if wrap:
        lon = np.where(lon < 0, lon+360, lon)
        polys = [[np.c_[np.where(r[:, 0] < 0, r[:, 0]+360, r[:, 0]), r[:, 1]] for r in p] for p in polys]
    lat0 = np.nanmean(lat); kx = 111320*np.cos(np.radians(lat0)); ky = 110574.0
    pts = []
    for p in polys:
        for r in p:
            x, y = r[:, 0]*kx, r[:, 1]*ky
            seg = np.hypot(np.diff(x), np.diff(y)); n = np.maximum(np.ceil(seg/5.0).astype(int), 1)
            for i in np.flatnonzero(n > 0):
                f = np.arange(n[i])/n[i]
                pts.append(np.c_[x[i]+f*(x[i+1]-x[i]), y[i]+f*(y[i+1]-y[i])])
    tree = cKDTree(np.vstack(pts))
    dist, _ = tree.query(np.c_[lon*kx, lat*ky], workers=-1)
    land = np.zeros(lon.shape, bool)
    for p in polys:
        ext = p[0]; x0, y0 = ext.min(0); x1, y1 = ext.max(0)
        cand = np.flatnonzero((lon >= x0) & (lon <= x1) & (lat >= y0) & (lat <= y1) & ~land)
        if not len(cand): continue
        q = np.c_[lon[cand], lat[cand]]; ins = Path(ext).contains_points(q)
        for h in p[1:]: ins &= ~Path(h).contains_points(q)
        land[cand[ins]] = True
    return dist, land

def summarise(isl, s, variant):
    low = s[s.elev_m <= THR]
    r = dict(island=LABEL[isl], variant=variant, buildings_analysed=len(s),
             low_buildings=len(low), low_pct=100*len(low)/len(s),
             low_footprint_pct=100*low.area_m2.sum()/s.area_m2.sum(),
             pct_le_0_5m=100*(s.elev_m <= 0.5).mean(), pct_le_2m=100*(s.elev_m <= 2.0).mean(),
             statutory_setback_m="/".join(map(str, SETBACK[isl])) or "none",
             low_median_dist_m=low.dist_coast_m.median())
    wide = max(SETBACK[isl]) if SETBACK[isl] else 0
    r["low_outside_every_setback_pct"] = 100*(low.dist_coast_m > wide).mean()
    for sb in (100, 25, 20):
        r[f"low_within_{sb}m_pct"] = 100*(low.dist_coast_m <= sb).mean()
    for q in (50, 75, 90, 95):
        r[f"setback_covering_{q}pct_low_m"] = round(low.dist_coast_m.clip(lower=0).quantile(q/100), 0)
    return r, low

if __name__ == "__main__":
    rows, curves, lows = [], [], {}
    for isl in ISLANDS:
        f = os.path.join(D, f"buildings/{isl}_building_points.csv.gz")
        if not os.path.exists(f):
            print(f"{isl}: {f} missing - run download_buildings_overture.py and export_building_points.py first"); continue
        b = pd.read_csv(f)
        lon, lat = b.lon.values, b.lat.values
        polys = polygons(os.path.join(D, f"boundaries_v2/{isl}_islands_v2.gpkg"))
        dist, land = coast_and_land(polys, lon, lat, wrap=(isl == "fiji"))
        b["dist_coast_m"] = np.where(land, dist, -dist).round(1)   # negative = seaward of the shoreline
        b["on_land"] = land
        z, src, cv = elevation(isl, lon, lat)
        b["elev_m"] = np.round(z, 2); b["elev_src"] = src; b["copernicus_m"] = np.round(cv, 2)
        near = land | (dist <= 50)
        s = b[near & np.isfinite(b.elev_m)]
        for variant, sub in (("all", s), ("excl_negative", s[s.elev_m >= 0])):
            r, low = summarise(isl, sub, variant)
            r.update(buildings_total=len(b), excluded_offshore_gt50m=int((~near).sum()),
                     excluded_no_elevation=int((near & ~np.isfinite(b.elev_m)).sum()))
            rows.append(r)
            if variant == "all":
                lows[isl] = low
                for d in (1, 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200, 250, 300, 400, 500, 750, 1000, 1500, 2000, 3000):
                    curves.append(dict(island=LABEL[isl], distance_m=d,
                                       pct_low_buildings_within=100*(low.dist_coast_m <= d).mean(),
                                       pct_all_buildings_within=100*(s.dist_coast_m <= d).mean()))
            print(f"{isl:12s} {variant:14s} low {r['low_pct']:5.2f}%  outside every setback "
                  f"{r['low_outside_every_setback_pct']:5.1f}%  90% cover at {r['setback_covering_90pct_low_m']:.0f} m", flush=True)
        b.to_csv(os.path.join(D, f"buildings/{isl}_buildings_setback.csv.gz"), index=False, compression="gzip")
    if not rows: sys.exit(0)
    cols = ["island", "variant", "buildings_total", "excluded_offshore_gt50m", "excluded_no_elevation"]
    out = pd.DataFrame(rows); out = out[cols + [c for c in out if c not in cols]].round(3)
    out.to_csv(os.path.join(D, "setback_calibration_summary.csv"), index=False)
    pd.DataFrame(curves).round(2).to_csv(os.path.join(D, "setback_coverage_curve.csv"), index=False)

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    os.makedirs(PLOTS, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    grid = np.logspace(0, np.log10(3000), 400)
    for isl in ["maldives", "lakshadweep", "seychelles", "fiji", "canary"]:
        if isl not in lows: continue
        d = np.sort(lows[isl].dist_coast_m.clip(lower=1).values)
        y = 100*np.searchsorted(d, grid, side="right")/len(d)
        ax.plot(grid, y, color=COLOR[isl], lw=2, label=f"{LABEL[isl]} (n = {len(d):,})")
        for sb in SETBACK[isl]:
            v = 100*(d <= sb).mean()
            ax.plot(sb, v, "o", color=COLOR[isl], ms=8, mec="white", mew=1.5, zorder=5)
            off = {("canary", 100): (-118, 4), ("canary", 20): (-108, 4),
                   ("seychelles", 25): (8, -10), ("lakshadweep", 20): (-118, 2)}.get((isl, sb), (6, -12))
            ax.annotate(f"{LABEL[isl]} {sb} m: {v:.0f}%", (sb, v), xytext=off,
                        textcoords="offset points", fontsize=8, color=COLOR[isl], fontweight="bold")
    ax.set_xscale("log"); ax.set_xlim(1, 3000); ax.set_ylim(0, 100)
    ax.set_xticks([1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]); ax.set_xticklabels(["1", "5", "10", "20", "50", "100", "200", "500", "1,000", "2,000"])
    ax.minorticks_off()
    ax.set_xlabel("Distance from shoreline (m, log scale)")
    ax.set_ylabel("% of buildings at or below 1 m within this distance")
    ax.set_title("How much of the low-lying building stock each statutory setback covers", loc="left", fontsize=11)
    ax.grid(alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right", title="No national setback: Maldives, Fiji", title_fontsize=8)
    plt.figtext(0.5, 0.01, "Buildings: Overture Maps 2026-08-19.0. Elevation: DeltaDTM v1.1 (bare earth), heights above EGM2008. "
                "Shoreline: boundaries_v2 polygon edge.", ha="center", fontsize=7, color="gray")
    plt.tight_layout(rect=(0, 0.03, 1, 1))
    plt.savefig(os.path.join(PLOTS, "fig9_setback_calibration.png"), dpi=200); plt.close()
    print("wrote data/setback_calibration_summary.csv, data/setback_coverage_curve.csv, outputs/plots/fig9_setback_calibration.png")
