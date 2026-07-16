import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/satellite_damage_proxy"

# Fiji bounding box, focused on Winston's landfall area
FIJI_BBOX_GEOMETRY = {
    "type": "Polygon",
    "coordinates": [[
        [177.0, -18.5], [180.0, -18.5], [180.0, -16.0], [177.0, -16.0], [177.0, -18.5]
    ]]
}


def request_ndvi_before_after(access_token, event_name, pre_start, pre_end, post_start, post_end):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["B04", "B08", "dataMask"] }],
        output: [
          { id: "ndvi", bands: 1, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
      return { ndvi: [ndvi], dataMask: [sample.dataMask] };
    }
    """

    results = {}
    for period_name, start, end in [("pre_cyclone", pre_start, pre_end), ("post_cyclone", post_start, post_end)]:
        payload = {
            "input": {
                "bounds": {
                    "geometry": FIJI_BBOX_GEOMETRY,
                    "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {"timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"}}
                }],
            },
            "aggregation": {
                "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
                "aggregationInterval": {"of": "P30D"},
                "evalscript": evalscript,
            },
        }

        response = requests.post(STATISTICAL_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            results[period_name] = response.json()
            print(f"  {period_name}: success")
        else:
            print(f"  {period_name}: FAILED ({response.status_code}) - {response.text[:200]}")

    return results


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Cyclone Winston: 20 Feb 2016
    print("Cyclone Winston (2016)...")
    winston_results = request_ndvi_before_after(
        access_token, "winston",
        pre_start="2016-01-01", pre_end="2016-01-31",
        post_start="2016-03-01", post_end="2016-03-31",
    )
    with open(os.path.join(OUTPUT_DIR, "fiji_winston_ndvi.json"), "w") as f:
        json.dump(winston_results, f, indent=2)
    print("Saved: fiji_winston_ndvi.json")

    # Cyclone Yasa: 17 Dec 2020
    print("\nCyclone Yasa (2020)...")
    yasa_results = request_ndvi_before_after(
        access_token, "yasa",
        pre_start="2020-11-01", pre_end="2020-11-30",
        post_start="2021-01-01", post_end="2021-01-31",
    )
    with open(os.path.join(OUTPUT_DIR, "fiji_yasa_ndvi.json"), "w") as f:
        json.dump(yasa_results, f, indent=2)
    print("Saved: fiji_yasa_ndvi.json")


if __name__ == "__main__":
    main()