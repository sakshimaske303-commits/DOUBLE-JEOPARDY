import json

ISLANDS = ["maldives", "seychelles", "fiji"]


def analyze_island(island):
    with open(f"data/settlement_encroachment/{island}_ndbi_change.json") as f:
        data = json.load(f)

    early_entries = data["early_2016"]["data"]
    recent_entries = data["recent_2024"]["data"]

    early_avg = sum(e["outputs"]["ndbi"]["bands"]["B0"]["stats"]["mean"] for e in early_entries) / len(early_entries)
    recent_avg = sum(e["outputs"]["ndbi"]["bands"]["B0"]["stats"]["mean"] for e in recent_entries) / len(recent_entries)

    change = recent_avg - early_avg

    print(f"{island.upper()}:")
    print(f"  2016 NDBI (built-up index): {early_avg:.4f}")
    print(f"  2024 NDBI (built-up index): {recent_avg:.4f}")
    print(f"  Change: {change:+.4f}")
    print()


def main():
    for island in ISLANDS:
        try:
            analyze_island(island)
        except Exception as e:
            print(f"{island.upper()}: ERROR - {e}\n")


if __name__ == "__main__":
    main()