# DOUBLE JEOPARDY: The Vulnerability Spiral
### Compound Climate Risk Across 5 Islands

Executive Summary · DOI: 10.5281/zenodo.21739961 · Sakshi D. Maske

## Project Overview

I built DOUBLE JEOPARDY to pressure test an assumption climate adaptation policy makes almost by default: that physical exposure to sea level rise is enough on its own to describe a small island's climate risk. It isn't, and I wanted numbers that could show that instead of just arguing it.

Working across 5 islands spanning 3 ocean basins (Maldives, Lakshadweep, Seychelles, Fiji, and the Canary Islands), I refused to lump mangroves and coral reefs together under one "ecosystem buffer" label. Mangrove decline and coral degradation went in as 2 independent hypotheses, tested separately, then combined with verified physical exposure into a single Compound Vulnerability Score per island.

That framing shaped the project's central result. Seychelles carries the highest overall compound risk once ecosystem degradation is weighted in, and, following a DEM data quality fix made during this project (see below), it also now has the highest physical exposure of any island in the sample on both exposure measures, settlement based and population weighted alike. An earlier version of this project showed a different island (Lakshadweep) as highest by population weighted exposure specifically. That looked at first like exactly the kind of indicator disagreement this project set out to test for, but it turned out instead to be nothing more than an artifact of the same DEM data problem, and it disappeared once that data was fixed. The corrected, fully agreeing picture reads as the sturdier result: the finding no longer depends on which specific exposure metric you pick.

I pushed the same standard onto governance too, testing whether formal protected area coverage actually tracks this empirically verified vulnerability. The answer is a strong correlation that reaches statistical significance despite the tiny sample (r=0.965, p=0.035, n=4; Lakshadweep excluded since no WDPA measurement is available for it). With only 4 data points though, I'm treating this as a strong signal and not yet a fully confirmed relationship.

Getting here also meant catching my own mistakes along the way. Early Canary Islands and Fiji physical exposure figures were inflated by DEM NoData artifacts misread as sea level settlements; corrected, they became the 2 lowest exposure figures in the sample (0.3% and 1.0% of settlements at risk). A larger catch followed: Maldives' and Lakshadweep's original elevation files turned out to have a severe data coverage gap instead of real near sea level terrain, with 99.99% of pixels holding no real data at all. Redownloading the source Copernicus data and recomputing corrected both islands' exposure figures substantially, and a related bug in the population weighted version of the same measure was caught and fixed too (full numbers are in the Limitations section below). Every measure in this project now agrees on the same island ranking as a result.

Together, the compound score result and the governance test are this project's 2 central contributions beyond the individual ecosystem hypotheses. One shows exposure alone is an incomplete measure of risk; the other shows protected area policy doesn't yet reliably track that fuller picture.

## The Question

Small islands face a compounding climate vulnerability: high physical exposure to sea level rise, layered with degrading natural coastal defenses (mangroves and coral reefs). Climate adaptation funding is often allocated using single indicator exposure metrics alone. Is that reliable, or does it systematically misrepresent true risk? And do all ecosystem buffers degrade uniformly, or does that assumption itself need testing?

## The Method

5 islands, 3 ocean basins (Canary Islands, Fiji, Lakshadweep, Maldives, Seychelles), tested against 10+ independently sourced datasets spanning 1996–2024. Physical exposure (settlement level sea level rise risk) and coral thermal stress trend (NOAA Coral Reef Watch Degree Heating Week) were normalized and combined into a single Compound Vulnerability Score. Mangrove extent was tracked separately, across 3 independent time points (1996, 2010, 2020) using Global Mangrove Watch as a distinct hypothesis, not assumed to move in step with coral reefs.

## The Finding

Seychelles is the highest risk island by every measure tested: settlement based exposure (78.3% of settlements at risk), population weighted exposure (17.6% of population), and the overall compound risk score once coral thermal stress is factored in on top of physical exposure. That full agreement is itself notable. An earlier version of this project showed Lakshadweep as the highest exposure island specifically by population weighting, and at the time that looked like the clearest case of exposure alone reasoning misleading you. It turned out to be a DEM data quality artifact instead: no real disagreement between indicators was ever there, and it disappeared once that data was corrected.

| Hypothesis | Result |
|---|---|
| H1: Coral thermal stress is rising | Supported: significant for Maldives (p=0.0046) & Seychelles (p=0.0069) |
| H2: Mangroves are degrading | Not supported: zero net decline across 3 islands, 3 time points |
| H3: Governance tracks vulnerability | Supported (marginally): r=0.965, p=0.035, n=4 (reaches significance, but on a very small sample) |

**Compound Vulnerability Score (top):** Seychelles 1.000 · Maldives 0.242 · Lakshadweep 0.133

The Compound Vulnerability ranking holds robustly across the entire 0–100% weighting sensitivity sweep. Seychelles stays highest ranked at every weighting from pure coral thermal stress to pure physical exposure, a stronger result than an earlier version of this project, where Maldives overtook Seychelles beyond about 76.8% physical exposure weighting.

## Validation & Robustness Checklist

- ✓ 2 ecosystems tested independently: no uniform decline assumption
- ✓ Seasonal Mann-Kendall trend test on the full 24-year coral series (not just a period comparison): the seasonal variant accounts for DHW's structural within year seasonality
- ✓ 3 independent time points for mangroves (1996 / 2010 / 2020)
- ✓ Population weighted exposure recomputation as a cross check
- ✓ Full 0–100% weighting sensitivity sweep (compound score robustness)
- ✓ SLR threshold sensitivity check across 0.5m / 1.0m / 1.5m thresholds
- ✓ Null result reported plainly: H2 (mangrove decline) not supported
- ! Governance correlation now reaches statistical significance (r=0.965, p=0.035) but still rests on only 4 data points: treated here as a strong signal, short of a confirmed relationship
- ! Coral thermal stress series sampled from a single representative coordinate per island instead of a reef area spatial average. The underlying NOAA product is only delivered at 5km resolution anyway, so this is a coarser than ideal choice, but a smaller gap than it might sound
- ! Lakshadweep has no coastal WDPA measurement available, so it's excluded from the governance alignment correlation (n=4) instead of being assigned a placeholder value
- ! Population weighted exposure figures still use a simple bounding box instead of each island's real boundary shape. A fixed script was tested against the real rasters, but the island boundary files it needs turned out to be incomplete (missing islands, undersized shapes), so this fix isn't ready yet
- ! Compound Vulnerability Score only combines physical exposure and coral condition. It does not include adaptive capacity (income, relocation options, disaster response), the 3rd leg of the standard IPCC vulnerability framework, so read it as a physical/ecological composite, short of a full socioeconomic vulnerability index

**Limitations, in Full:** The governance alignment test (protected area coverage vs. verified vulnerability) shows a strong positive correlation (r=0.965, n=4) that now reaches statistical significance (p=0.035, 95% CI: 0.05 to 1.00), up from an earlier r=0.862, p=0.138. With only 4 islands in the correlation though, I'm still treating this as a strong signal short of settled proof, since a single data point could move both the coefficient and the p value substantially at this sample size. Lakshadweep is excluded from that correlation entirely instead of being assigned a placeholder value, since I had no protected area dataset for it and a fabricated zero would bias an already tiny sample; its Compound Vulnerability Score (0.133) is reported separately, unpaired with a WDPA measurement. The Compound Vulnerability Score also uses min max normalization, so scores are relative within this 5 island sample instead of absolute: Canary Islands' score of 0.000 reflects the lowest raw values in this sample. It doesn't mean an absence of risk. The coral thermal stress series itself comes from a single representative coordinate per island instead of a spatial average across the full reef area, a coarser sampling choice than area weighted aggregation would give, kept for consistency with how the DHW product is queried.

I also corrected both Canary Islands' and Fiji's physical exposure figures (0.3% and 1.0% of settlements at risk, respectively) during data quality review, excluding DEM NoData artifacts I'd initially misread as sea level settlements. A separate, larger correction applied to Maldives and Lakshadweep: their original elevation files had a severe data coverage gap instead of a small artifact (99.99% of pixels held no real data), so I redownloaded the source Copernicus DEM tiles directly from ESA's public archive and recomputed exposure against the complete data. That brought their settlement based figures down from an artifact inflated 99.1% and 77.8% to a corrected 14.5% and 7.1%. Fixing the population weighted version of the same measure then surfaced a 2nd, independent bug: the script had been silently applying a known incomplete boundary polygon mask on every run instead of the bounding box method this project reports. That undercounted Lakshadweep's population by roughly seven eighths. With both bugs fixed, Maldives' and Lakshadweep's population weighted exposure moved from an artifact inflated 64.5% and 87.5% to a corrected 16.9% and 2.2%. See the Research Paper's Limitations section for the full explanation, including the residual 17.8%/22.2% of settlements still sitting in an unresolved coverage gap in the public Copernicus archive itself.

## Real World Relevance

Climate adaptation funding for small islands is frequently allocated using single indicator exposure metrics. This project's central methodological argument, that exposure and true compound risk are not the same thing and that ecosystem buffers do not degrade uniformly, has direct implications for how conservation and adaptation resources should be prioritized across islands and ecosystem types.

---

GitHub: [github.com/sakshimaske303-commits/DOUBLE-JEOPARDY](https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY) | Live Dashboard: [double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21739961](https://doi.org/10.5281/zenodo.21739961)

**Sakshi D. Maske**, Independent Geospatial Researcher
