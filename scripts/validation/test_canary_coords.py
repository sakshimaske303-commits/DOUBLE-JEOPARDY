import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
ERDDAP_BASE = "https://coastwatch.noaa.gov/erddap/griddap/noaacrwdhwDaily"

test_points = [
    ("south_of_gc", -15.4, 27.7),
    ("west_tenerife", -16.8, 28.2),
    ("north_lanzarote", -13.6, 29.3),
]

for name, lon, lat in test_points:
    url = f"{ERDDAP_BASE}.csv?degree_heating_week[(2020-01-01):1:(2020-01-31)][({lat}):1:({lat})][({lon}):1:({lon})]"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        lines = r.text.strip().split("\n")
        result_line = lines[2] if len(lines) > 2 else "no data row"
        print(f"{name} ({lon}, {lat}): {result_line}")
    else:
        print(f"{name}: FAILED {r.status_code}")