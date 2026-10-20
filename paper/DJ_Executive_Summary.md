# DOUBLE JEOPARDY: The Vulnerability Spiral
### Sea-Level Exposure and Reef Heat Stress Across 5 Island Groups

Executive Summary · Version 2.0 · DOI: 10.5281/zenodo.21739961 · Sakshi D. Maske

## Project Overview

Low islands face two threats at once: the sea rising, and the reefs and mangroves that hold it back weakening. I named the project for that double threat. I wanted to measure both, island by island, across 5 island groups in 3 ocean basins (Maldives, Lakshadweep, Seychelles, Fiji and the Canary Islands), and see whether protection follows the risk.

Version 1 gave a clean story: Seychelles most exposed, coral trends significant, the ranking robust, protection tracking risk. When I went back through every measurement choice, most of that story did not survive. Version 2 is what is left, and the main thing it shows is how much the answer depends on choices that are usually made silently: which elevation model, what is counted as exposure, and how the inputs are weighted.

## The Question

How many people on these islands live at or below 1 m? How has heat stress on their reefs changed between 1996 and 2020, and have mangroves declined? When the two are put side by side, which island comes out highest, and does protected-area coverage follow that ranking?

## The Method

- **Exposure:** share of people (WorldPop 2020, 100 m) on land at or below 1 m, on the **DeltaDTM v1.1 bare-earth model** (Pronk et al. 2024). Copernicus GLO-30, a surface model, is kept for comparison. The share of OpenStreetMap named places is a second measure; 0.5 m and 1.5 m are sensitivity checks. Heights are above the EGM2008 geoid, used as an approximation of mean sea level.
- **Reef heat stress:** NOAA Coral Reef Watch Degree Heating Weeks (DHW, 5 km), averaged over all mapped reef cells per island, 1996–2020. Change between 1996–2000 and 2016–2020, and a seasonal Mann-Kendall test on monthly means corrected for serial correlation.
- **Mangroves:** Global Mangrove Watch v3 at 1996, 2010 and 2020.
- **Compound score:** exposure and change in reef heat stress, each scaled 0–1, averaged; weighting swept from 0 to 100%.
- **Governance:** share of the 10 km coastal zone inside a protected area (WDPA, June 2026, overlaps merged). Descriptive only.

## The Findings

**People at or below 1 m**

| Island group | Bare earth (DeltaDTM) | Surface (Copernicus) | People |
|---|---:|---:|---:|
| Maldives | 11.82% | 8.88% | 57,889 |
| Lakshadweep | 6.40% | 0.79% | 4,238 |
| Seychelles | 2.07% | 0.43% | 1,933 |
| Fiji | 0.28% | 0.21% | 2,460 |
| Canary Islands | 0.19% | 0.15% | 3,946 |

| Hypothesis | Result |
|---|---|
| H1: Reef heat stress is rising | **Partly supported.** Mean DHW over reef rose on every reef island (Seychelles +0.52, Fiji +0.29, Maldives +0.07, Lakshadweep +0.05 °C-weeks), but no monotonic trend is significant once serial correlation is accounted for (p = 0.14 to 0.90) |
| H2: Mangroves are declining | **Not supported.** No decline on any of the 3 islands (Fiji 485.7 → 488.4 km²) |
| H3: Protection follows risk | **Not supported.** r = −0.10 (95% interval −0.97 to 0.95, n = 4); coverage from 1.3% (Maldives) to 71.4% (Seychelles) |

**Compound score (equal weights):** Seychelles 0.58 · Maldives 0.56 · Lakshadweep 0.32 · Fiji 0.28 · Canary Islands 0.00. Exposure points to the Maldives and reef heat stress to Seychelles, so the top island switches to the Maldives once exposure carries 52% or more of the weight. I read the top two as a near tie.

## What Changed From Version 1, and Why

- ✗ **"78.3% of Seychelles settlements at risk."** 188 of 244 Seychelles points read the elevation raster's NoData value (−32767 m) and were counted as at risk. And most OSM "settlement" points on these islands are names of islands and islets, some sitting in open water. I now count people, with named places as a second measure (Seychelles 24.7%, Maldives 28.8% on bare earth).
- ✗ **Surface elevation model.** Copernicus measures roofs and canopy on wooded atolls. On bare earth, Lakshadweep goes from 0.8% to 6.4% of people at or below 1 m. Where Copernicus is above 30 m, I do not use DeltaDTM: on small forested granite islands in Seychelles it otherwise reads a hill as sea level.
- ✗ **"Coral trends significant for Maldives (p = 0.0046) and Seychelles (p = 0.0069)."** That used one 5 km cell per island and a test that treats neighbouring months as independent. DHW is a 12-week running sum, so they are not. Without the correction, Seychelles (p = 0.002) and the Maldives (p = 0.049) still look significant; with it, p = 0.14 and 0.31.
- ✗ **"The ranking holds at every weighting."** Seychelles came out top at every weighting because it was highest on both inputs by construction. With people and reef-cell means, the inputs disagree and the ranking depends on the weights.
- ✗ **"Governance correlation r = 0.965, p = 0.035."** Overlapping protected areas were counted twice and coverage was divided by land area. As a share of the coastal zone, the relationship disappears.
- ✗ **Seychelles built-up rise (+0.11 NDBI).** Measured over bounding boxes that were mostly ocean. On land only, Seychelles shows no rise and the Maldives a small one (+0.055).

## Limitations

- These are elevation thresholds, not flood models: no tides, surge, waves or connectivity. DeltaDTM's error against airborne lidar (about 0.4–0.5 m) is large next to a 1 m threshold, so the comparison between models matters more than any single percentage.
- WorldPop is a modelled population surface, not a census.
- Five island groups (four for governance) describe this sample; they cannot establish general relationships.
- The compound score uses min–max scaling, so Canary Islands' 0.00 is the lowest in this sample, not an absence of risk, and it leaves out adaptive capacity entirely.
- Mangrove patches on the atolls are close to Global Mangrove Watch's pixel size, so small losses there may not be detectable.

## Real World Relevance

Adaptation finance for small islands is increasingly tied to vulnerability indices. This project shows that the same islands can rank differently depending on the elevation model, the exposure measure and the weighting, and that a surface model can understate how many people live at or below 1 m by several times on a forested atoll. Any index built on these inputs should report those choices and how sensitive its ranking is to them.

---

GitHub: [github.com/sakshimaske303-commits/DOUBLE-JEOPARDY](https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY) | Live Dashboard: [double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21739961](https://doi.org/10.5281/zenodo.21739961)

**Sakshi D. Maske**, Independent Geospatial Researcher
