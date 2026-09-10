import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/satellite_damage_proxy"

# Strongest recorded cyclone per island, with approximate bounding box
ISLAND_CYCLONES = {
    "maldives": {
        "date": "2006-01-14",
        "bbox": (72.5, -1.0, 74.0, 7.5),
    },
    "seychelles": {
        "date": "1996-02-14",
        "bbox": (46.0, -10.5, 56.5, -3.5),
    },
    "lakshadweep": {
        "date": "1997-11-09",
        "bbox": (71.5, 8.0, 74.0, 12.5),
    },
}


def make_bbox_geometry(bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    return {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat], [max_lon, min_lat],
            [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]
        ]]
    }


def request_ndvi_before_after(access_token, geometry, pre_start, pre_end, post_start, post_end):
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
                    "geometry": geometry,
                    "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
                        "maxCloudCoverage": 40
                    }
                }],
            },
            "aggregation": {
                "timeRange": {"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"},
                "aggregationInterval": {"of": "P6M"},
                "evalscript": evalscript,
            },
        }

        response = requests.post(STATISTICAL_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            results[period_name] = result
            data_count = len(result.get("data", []))
            print(f"  {period_name}: success ({data_count} data points)")
        else:
            print(f"  {period_name}: FAILED ({response.status_code}) - {response.text[:200]}")

    return results


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for island, info in ISLAND_CYCLONES.items():
        print(f"\nProcessing {island} (cyclone date: {info['date']})...")
        geometry = make_bbox_geometry(info["bbox"])

        cyclone_date = info["date"]
        year = int(cyclone_date[:4])

        # Note: Sentinel-2 launched in 2015, so cyclones before this date
        # cannot have pre-cyclone Sentinel-2 imagery. This is flagged
        # explicitly rather than silently producing empty results.
        if year < 2016:
            print(f"  SKIPPED: Cyclone predates Sentinel-2 availability (launched 2015) - no valid imagery possible")
            continue

        results = request_ndvi_before_after(
            access_token, geometry,
            pre_start=f"{year-1}-06-01", pre_end=f"{year-1}-12-31",
            post_start=f"{year}-06-01", post_end=f"{year}-12-31",
        )

        output_path = os.path.join(OUTPUT_DIR, f"{island}_cyclone_ndvi.json")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Saved: {output_path}")


if __name__ == "__main__":
    main()