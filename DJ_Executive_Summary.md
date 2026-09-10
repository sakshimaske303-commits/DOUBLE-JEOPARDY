# DOUBLE JEOPARDY — The Vulnerability Spiral
### Compound Climate Risk Across Five Islands

Executive Summary · DOI: 10.5281/zenodo.21739961 · Sakshi D. Maske

## Project Overview

I built DOUBLE JEOPARDY to pressure-test an assumption climate adaptation policy makes almost by default: that physical exposure to sea-level rise is enough on its own to describe a small island's climate risk. It isn't, and I wanted numbers that could show that rather than just argue it.

Working across five islands spanning three ocean basins — Maldives, Lakshadweep, Seychelles, Fiji, and the Canary Islands — I refused to lump mangroves and coral reefs together under one "ecosystem buffer" label. Mangrove decline and coral degradation went in as two independent hypotheses, tested separately, then combined with verified physical exposure into a single Compound Vulnerability Score per island.

That framing is what shaped the project's central result: Seychelles carries the highest overall compound risk once ecosystem degradation is weighted in — and, following a DEM data-quality fix made during this project (see below), it also now has the highest physical exposure of any island in the sample on BOTH exposure measures, settlement-based and population-weighted alike. An earlier version of this project showed a different island (Lakshadweep) as highest by population-weighted exposure specifically, which looked like exactly the kind of indicator-disagreement this project set out to test for — it turned out instead to be an artifact of the same DEM data problem, not a real finding, and disappeared once that data was fixed. I read the corrected, fully-agreeing picture as the more robust result, not a weaker one: the finding no longer depends on which specific exposure metric you pick.

I pushed the same standard onto governance, too, testing whether formal protected-area coverage actually tracks this empirically verified vulnerability. The answer is a strong correlation that reaches statistical significance despite the tiny sample (r=0.965, p=0.035, n=4 — Lakshadweep excluded, no WDPA measurement available for it) — though with only four data points, I'm reading this as a stronger signal rather than a fully confirmed relationship.

Getting here also meant catching my own mistakes along the way: early versions of both the Canary Islands' and Fiji's physical-exposure figures were inflated by DEM NoData artifacts I'd misread as sea-level settlements. The corrected numbers — 0.3% and 1.0% of settlements at risk respectively, the two lowest in the sample — are what now appear everywhere in this project's outputs. A separate, bigger catch turned up later: Maldives' and Lakshadweep's original elevation files had a severe data coverage gap, not genuine near-sea-level terrain (99.99% of pixels held no real data at all). Re-downloading the source data directly from ESA's Copernicus archive and recomputing brought their settlement-based exposure figures down from an artifact-inflated 99.1% and 77.8% to a corrected 14.5% and 7.1%. Fixing the population-weighted version of the same measure surfaced a second, unrelated bug on top of that: the script was silently applying a known-incomplete boundary-polygon mask on every run instead of the bounding-box method this project actually reports, undercounting Lakshadweep's population by roughly seven-eighths in the process. With both bugs fixed, Maldives' and Lakshadweep's population-weighted exposure moved from an artifact-inflated 64.5% and 87.5% to a corrected 16.9% and 2.2% — and every measure in this project (settlement count, population weighting, compound score) now agrees on the same island ranking, which is what appears throughout this project's outputs.

Together, the compound-score result and the governance test are this project's two central contributions beyond the individual ecosystem hypotheses: one shows exposure alone is an incomplete measure of risk, the other shows protected-area policy doesn't yet reliably track that fuller picture.

## The Question

Small islands face a compounding climate vulnerability — high physical exposure to sea-level rise, layered with degrading natural coastal defenses (mangroves and coral reefs). Climate adaptation funding is often allocated using single-indicator exposure metrics alone. Is that reliable, or does it systematically misrepresent true risk? And do all ecosystem buffers degrade uniformly, or does that assumption itself need testing?

## The Method

Five islands, three ocean basins — Canary Islands, Fiji, Lakshadweep, Maldives, Seychelles — tested against 10+ independently-sourced datasets spanning 1996–2024. Physical exposure (settlement-level sea-level-rise risk) and coral thermal-stress trend (NOAA Coral Reef Watch Degree Heating Week) were normalized and combined into a single Compound Vulnerability Score. Mangrove extent I tracked separately, across three independent time points (1996, 2010, 2020) using Global Mangrove Watch — a distinct hypothesis, not assumed to move in step with coral reefs.

## The Finding

Seychelles is the highest-risk island by every measure tested — settlement-based exposure (78.3% of settlements at risk), population-weighted exposure (17.6% of population), and the overall compound-risk score once coral thermal stress is factored in on top of physical exposure. That full agreement is itself notable: an earlier version of this project showed Lakshadweep as the highest-exposure island specifically by population weighting, which looked at the time like the clearest case of exposure-alone reasoning misleading you. It turned out to be a DEM data-quality artifact, not a real disagreement between indicators, and disappeared once that data was corrected.

| Hypothesis | Result |
|---|---|
| H1 — Coral thermal stress is rising | Supported — significant for Maldives (p=0.0046) & Seychelles (p=0.0069) |
| H2 — Mangroves are degrading | Not supported — zero net decline across 3 islands, 3 time points |
| H3 — Governance tracks vulnerability | Supported (marginally) — r=0.965, p=0.035, n=4 (reaches significance, but on a very small sample) |

**Compound Vulnerability Score (top):** Seychelles 1.000 · Maldives 0.242 · Lakshadweep 0.133

The Compound Vulnerability ranking holds robustly across the entire 0–100% weighting-sensitivity sweep — Seychelles stays highest-ranked at every weighting from pure coral-thermal-stress to pure physical-exposure, a stronger result than an earlier version of this project, where Maldives overtook Seychelles beyond ~76.8% physical-exposure weighting.

## Validation & Robustness Checklist

- ✓ Two ecosystems tested independently — no uniform-decline assumption
- ✓ Seasonal Mann-Kendall trend test on the full 24-year coral series (not just period comparison) — the seasonal variant accounts for DHW's structural within-year seasonality
- ✓ 3 independent time points for mangroves (1996 / 2010 / 2020)
- ✓ Population-weighted exposure recomputation as a cross-check
- ✓ Full 0–100% weighting-sensitivity sweep (compound score robustness)
- ✓ SLR-threshold sensitivity check across 0.5m / 1.0m / 1.5m thresholds
- ✓ Honest null result reported — H2 (mangrove decline) not supported
- ! Governance correlation now reaches statistical significance (r=0.965, p=0.035) but still rests on only 4 data points — read as a stronger signal, not a confirmed relationship
- ! Coral thermal-stress series sampled from a single representative coordinate per island, not a reef-area spatial average — the underlying NOAA product is only delivered at 5km resolution anyway, so this is a coarser-than-ideal choice, not as big a gap as it sounds
- ! Lakshadweep has no coastal WDPA measurement available, so it's excluded from the governance-alignment correlation (n=4) rather than assigned a placeholder value
- ! Population-weighted exposure figures still use a simple bounding box, not each island's real boundary shape. A fixed script was tested against the real rasters, but the island boundary files it needs turned out to be incomplete (missing islands, undersized shapes), so this fix is not ready yet
- ! Compound Vulnerability Score only combines physical exposure and coral condition — it does not include adaptive capacity (income, relocation options, disaster response), the third leg of the standard IPCC vulnerability framework. Read it as a physical/ecological composite, not a full socioeconomic vulnerability index

**Honest Limitation:** The governance-alignment test (protected-area coverage vs. verified vulnerability) shows a strong positive correlation (r=0.965, n=4) that now reaches statistical significance (p=0.035, 95% CI: 0.05 to 1.00) — up from an earlier r=0.862, p=0.138 — but with only four islands in the correlation, I'm still reading this as a stronger signal rather than settled proof, since a single data point could move both the coefficient and the p-value substantially at this sample size. Lakshadweep is excluded from that correlation entirely rather than assigned a placeholder value, since I had no protected-area dataset for it and a fabricated zero would bias an already-tiny sample; its Compound Vulnerability Score (0.133) is reported separately, unpaired with a WDPA measurement. The Compound Vulnerability Score also uses min-max normalization, so scores are relative within this five-island sample rather than absolute — Canary Islands' score of 0.000 reflects the lowest raw values in this sample, not the absence of risk. The coral thermal-stress series itself comes from a single representative coordinate per island rather than a spatial average across the full reef area — a coarser sampling choice than area-weighted aggregation would give, kept for consistency with how the DHW product is queried. I also corrected both Canary Islands' and Fiji's physical-exposure figures (0.3% and 1.0% of settlements at risk, respectively) during data-quality review, to exclude DEM NoData artifacts I'd initially misread as sea-level settlements. A separate, larger correction applied to Maldives and Lakshadweep: their original elevation files had a severe data coverage gap rather than a small artifact (99.99% of pixels held no real data), so I re-downloaded the source Copernicus DEM tiles directly from ESA's public archive and recomputed exposure against the complete data, bringing their settlement-based figures down from an artifact-inflated 99.1% and 77.8% to a corrected 14.5% and 7.1%. Fixing the population-weighted version of the same measure then surfaced a second, independent bug: the script had been silently applying a known-incomplete boundary-polygon mask on every run instead of the bounding-box method this project reports, which undercounted Lakshadweep's population by roughly seven-eighths. With both fixed, Maldives' and Lakshadweep's population-weighted exposure moved from an artifact-inflated 64.5% and 87.5% to a corrected 16.9% and 2.2% — see the Research Paper's Limitations section for the full explanation, including the residual 17.8%/22.2% of settlements still sitting in an unresolved coverage gap in the public Copernicus archive itself.

## Real-World Relevance

Climate adaptation funding for small islands is frequently allocated using single-indicator exposure metrics. This project's central methodological argument — that exposure and true compound risk are not the same thing, and that ecosystem buffers do not degrade uniformly — has direct implications for how conservation and adaptation resources should be prioritized across islands and ecosystem types.

---

GitHub: [github.com/sakshimaske303-commits/DOUBLE-JEOPARDY](https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY) | Live Dashboard: [double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21739961](https://doi.org/10.5281/zenodo.21739961)

**Sakshi D. Maske** — Independent Geospatial Researcher
