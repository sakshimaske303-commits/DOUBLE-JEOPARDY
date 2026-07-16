import requests
import pandas as pd
import os

OUTPUT_DIR = "data/coral_bleaching"

# Approximate coordinate (single representative point) per island for DHW time series
ISLAND_POINTS = {
    "maldives": (73.5, 3.5),
    "seychelles": (55.5, -4.5),
    "fiji": (178.5, -17.5),
    "canary": (-15.5, 28.0),
    "lakshadweep": (72.6, 10.5),
}

ERDDAP_BASE = "https://coastwatch.noaa.gov/erddap/griddap/noaacrwdhwDaily"


def download_dhw_timeseries(island, lon, lat, start_date="1996-01-01", end_date="2020-12-31"):
    # Annual max composite would be more useful, but let's start with a
    # coarse monthly-stride daily query to keep the request manageable
    url = f"{ERDDAP_BASE}.csv?degree_heating_week[({start_date}):30:({end_date})][({lat}):1:({lat})][({lon}):1:({lon})]"

    print(f"Requesting {island}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"{island}_dhw_timeseries.csv")
        with open(output_path, "w") as f:
            f.write(response.text)
        print(f"  Saved: {output_path}")
    else:
        print(f"  FAILED ({response.status_code}): {response.text[:300]}")


def main():
    for island, (lon, lat) in ISLAND_POINTS.items():
        download_dhw_timeseries(island, lon, lat)


if __name__ == "__main__":
    main()