"""V-Dem electoral democracy index for the five jurisdictions, via Our World in Data.

Run from the repository root:
    python scripts/acquisition/download_vdem_owid.py
Writes data/regime/vdem_electoral_democracy.csv.
"""
import io, os, urllib.request
import pandas as pd

URL = ("https://ourworldindata.org/grapher/electoral-democracy-index.csv"
       "?v=1&csvType=full&useColumnShortNames=false")
COUNTRIES = {"Spain": "canary", "India": "lakshadweep", "Seychelles": "seychelles",
             "Maldives": "maldives", "Fiji": "fiji"}
OUT = os.path.join("data", "regime", "vdem_electoral_democracy.csv")

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (research script)"})
raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8")
df = pd.read_csv(io.StringIO(raw))
value_col = [c for c in df.columns if c not in ("Entity", "Code", "Year")][0]
df = df[df["Entity"].isin(COUNTRIES) & (df["Year"] >= 1985)].copy()
df = df.rename(columns={"Entity": "country", "Year": "year", value_col: "electoral_democracy_vdem"})
df["jurisdiction"] = df["country"].map(COUNTRIES)
df = df[["jurisdiction", "country", "year", "electoral_democracy_vdem"]].sort_values(["jurisdiction", "year"])
os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Saved {OUT}: {len(df)} rows, column '{value_col}'")
print(df.groupby("country").tail(1).to_string(index=False))
