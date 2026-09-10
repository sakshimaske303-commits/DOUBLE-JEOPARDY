
import os
import time
import requests
import pandas as pd

OUTPUT_DIR = "data/coral_bleaching_v2"
ORIGINAL_DIR = "data/coral_bleaching"

ISLAND_POINTS = {
    "maldives": (73.5, 3.5),
    "seychelles": (55.5, -4.5),
    "fiji": (178.5, -17.5),
    "canary": (-15.5, 28.0),
    "lakshadweep": (72.6, 10.5),
}

BOX_HALF_DEG = 0.15
GRID_STRIDE = 1

ERDDAP_BASE = "https://coastwatch.noaa.gov/erddap/griddap/noaacrwdhwDaily"


def download_dhw_area_avg(island, lon, lat, start_date="1996-01-01", end_date="2020-12-31"):
    lat_min, lat_max = lat - BOX_HALF_DEG, lat + BOX_HALF_DEG
    lon_min, lon_max = lon - BOX_HALF_DEG, lon + BOX_HALF_DEG

    url = (
        f"{ERDDAP_BASE}.csv?degree_heating_week"
        f"[({start_date}):30:({end_date})]"
        f"[({lat_min}):{GRID_STRIDE}:({lat_max})]"
        f"[({lon_min}):{GRID_STRIDE}:({lon_max})]"
    )

    print(f"Requesting {island} (box {lat_min:.2f}-{lat_max:.2f}N, {lon_min:.2f}-{lon_max:.2f}E)...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers, timeout=120)

    if response.status_code != 200:
        print(f"  FAILED ({response.status_code}): {response.text[:300]}")
        return None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    raw_path = os.path.join(OUTPUT_DIR, f"{island}_dhw_raw_grid.csv")
    with open(raw_path, "w") as f:
        f.write(response.text)

    df = pd.read_csv(raw_path, skiprows=[1])
    df.columns = [c.strip().lower() for c in df.columns]

    dhw_col = [c for c in df.columns if "degree_heating_week" in c][0]

    grouped = df.groupby("time")[dhw_col].agg(
        dhw_mean="mean",
        dhw_std="std",
        valid_pixel_count="count",
    ).reset_index()
    total_pixels = df.groupby("time")[dhw_col].size().iloc[0] if len(df) else 0
    grouped["total_pixel_count"] = df.groupby("time").size().values
    grouped["coverage_pct"] = (grouped["valid_pixel_count"] / grouped["total_pixel_count"] * 100).round(1)

    out_path = os.path.join(OUTPUT_DIR, f"{island}_dhw_timeseries_areaavg.csv")
    grouped.to_csv(out_path, index=False)
    print(f"  Saved: {out_path}  ({len(grouped)} time steps, "
          f"median coverage {grouped['coverage_pct'].median():.0f}%)")
    return grouped


def compare_to_original(island, area_avg_df):
    orig_path = os.path.join(ORIGINAL_DIR, f"{island}_dhw_timeseries.csv")
    if not os.path.exists(orig_path) or area_avg_df is None:
        return
    try:
        orig = pd.read_csv(orig_path, skiprows=[1])
        orig.columns = [c.strip().lower() for c in orig.columns]
        dhw_col = [c for c in orig.columns if "degree_heating_week" in c][0]
        orig_mean = orig[dhw_col].mean()
        new_mean = area_avg_df["dhw_mean"].mean()
        print(f"  [{island}] original single-point mean: {orig_mean:.4f}   "
              f"area-avg mean: {new_mean:.4f}   diff: {new_mean - orig_mean:+.4f}")
    except Exception as e:
        print(f"  [{island}] could not compare to original: {e}")


def main():
    for island, (lon, lat) in ISLAND_POINTS.items():
        result = download_dhw_area_avg(island, lon, lat)
        compare_to_original(island, result)
        time.sleep(1)

    print("\nDone. Zip up data/coral_bleaching_v2/ and send it back along with")
    print("this console output -- the Mann-Kendall trend test and Section 4.3")
    print("figures can then be re-run against the area-averaged series to see")
    print("whether the trend/p-values change at all before touching the paper.")


if __name__ == "__main__":
    main()

