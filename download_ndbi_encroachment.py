import os
import json
import requests
from auth_sentinelhub import get_sentinelhub_token

STATISTICAL_API_URL = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
OUTPUT_DIR = "data/settlement_encroachment"

# Smaller, more focused bounding boxes to stay within API resolution limits
ISLAND_BBOX = {
    "maldives": (72.9, 3.0, 73.6, 4.5),  # focused on Male region, smaller extent
    "seychelles": (55.3, -4.8, 55.6, -4.5),
    "fiji": (177.2, -18.3, 178.0, -17.5),  # focused on Viti Levu west coast
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


def request_ndbi(access_token, island, bbox, year):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    geometry = make_bbox_geometry(bbox)

    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["B11", "B08", "dataMask"] }],
        output: [
          { id: "ndbi", bands: 1, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 }
        ]
      };
    }
    function evaluatePixel(sample) {
      let ndbi = (sample.B11 - sample.B08) / (sample.B11 + sample.B08);
      return { ndbi: [ndbi], dataMask: [sample.dataMask] };
    }
    """

    payload = {
        "input": {
            "bounds": {
                "geometry": geometry,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"},
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {"from": f"{year}-01-01T00:00:00Z", "to": f"{year+1}-01-01T00:00:00Z"},
                    "maxCloudCoverage": 30
                }
            }],
        },
        "aggregation": {
            "timeRange": {"from": f"{year}-01-01T00:00:00Z", "to": f"{year+1}-01-01T00:00:00Z"},
            "aggregationInterval": {"of": "P6M"},
            "evalscript": evalscript,
        },
    }

    response = requests.post(STATISTICAL_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if len(result.get("data", [])) == 0:
            print(f"    WARNING: empty data returned, geometryPixelCount={result.get('geometryPixelCount')}")
        return result
    else:
        print(f"  FAILED ({response.status_code}): {response.text[:300]}")
        return None


def main():
    access_token = get_sentinelhub_token()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for island, bbox in ISLAND_BBOX.items():
        print(f"Processing {island}...")
        results = {}

        for year_label, year in [("early_2016", 2016), ("recent_2024", 2024)]:
            print(f"  Requesting {year_label}...")
            result = request_ndbi(access_token, island, bbox, year)
            if result:
                results[year_label] = result
                print(f"    Success")

        output_path = os.path.join(OUTPUT_DIR, f"{island}_ndbi_change.json")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Saved: {output_path}\n")


if __name__ == "__main__":
    main()