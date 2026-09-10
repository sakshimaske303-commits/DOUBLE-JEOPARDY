import json

with open("data/settlement_encroachment/maldives_ndbi_change.json") as f:
    data = json.load(f)

print(json.dumps(data["early_2016"], indent=2)[:1500])