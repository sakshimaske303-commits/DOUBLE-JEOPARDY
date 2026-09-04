# DOUBLE JEOPARDY — The Vulnerability Spiral
### Compound Climate Risk Across Five Island Nations

Executive Summary · DOI: 10.5281/zenodo.21739961 · Sakshi D. Maske

## Project Overview

I built DOUBLE JEOPARDY to pressure-test an assumption climate adaptation policy makes almost by default: that physical exposure to sea-level rise is enough on its own to describe a small island nation's climate risk. It isn't, and I wanted numbers that could show that rather than just argue it.

Working across five island nations spanning three ocean basins — Maldives, Lakshadweep, Seychelles, Fiji, and the Canary Islands — I refused to lump mangroves and coral reefs together under one "ecosystem buffer" label. Mangrove decline and coral degradation went in as two independent hypotheses, tested separately, then combined with verified physical exposure into a single Compound Vulnerability Score per island.

That framing is what produced the project's central result: Seychelles, not the higher-exposure Maldives, comes out as the highest-overall-risk island once ecosystem degradation is properly weighted in. It's a finding that only shows up once you model compound risk — look at exposure alone and you'd miss it entirely.

I pushed the same standard onto governance, too, testing whether formal protected-area coverage actually tracks this empirically verified vulnerability. The answer is a moderately strong but not statistically significant correlation (r=0.718, p=0.172) — a genuine limit of a five-island sample, and I've reported it as suggestive rather than dressed it up as confirmed.

Getting here also meant catching my own mistake along the way: an early version of the Canary Islands' physical-exposure figure was inflated by DEM NoData artifacts I'd misread as sea-level settlements. The corrected number — 0.3% of settlements at risk, the lowest in the sample — is what now appears everywhere in this project's outputs.

Together, the compound-score result and the governance test are this project's two central contributions beyond the individual ecosystem hypotheses: one shows exposure alone is an incomplete measure of risk, the other shows protected-area policy doesn't yet reliably track that fuller picture.

## The Question

Small island nations face a compounding climate vulnerability — high physical exposure to sea-level rise, layered with degrading natural coastal defenses (mangroves and coral reefs). Climate adaptation funding is often allocated using single-indicator exposure metrics alone. Is that reliable, or does it systematically misrepresent true risk? And do all ecosystem buffers degrade uniformly, or does that assumption itself need testing?

## The Method

Five island nations, three ocean basins — Canary Islands, Fiji, Lakshadweep, Maldives, Seychelles — tested against 10+ independently-sourced datasets spanning 1996–2024. Physical exposure (settlement-level sea-level-rise risk) and coral thermal-stress trend (NOAA Coral Reef Watch Degree Heating Week) were normalized and combined into a single Compound Vulnerability Score. Mangrove extent I tracked separately, across three independent time points (1996, 2010, 2020) using Global Mangrove Watch — a distinct hypothesis, not assumed to move in step with coral reefs.

## The Finding

Physical exposure alone is misleading. The Maldives has the highest sea-level-rise exposure of any island tested (99.1% of settlements at risk) — yet Seychelles emerges as the highest overall-risk island once ecosystem degradation is factored in, driven by the most severe coral thermal-stress trend recorded across the sample.

| Hypothesis | Result |
|---|---|
| H1 — Coral reefs are degrading | Supported — significant for Maldives (p=0.011) & Seychelles (p=0.025) |
| H2 — Mangroves are degrading | Not supported — zero net decline across 3 islands, 3 time points |
| H3 — Governance tracks vulnerability | Suggestive only — r=0.718, p=0.172 (not significant) |

**Compound Vulnerability Score (top):** Seychelles 0.895 · Maldives 0.651 · Lakshadweep 0.481

The Compound Vulnerability ranking holds robustly across most of the 0–100% weighting-sensitivity sweep — Seychelles stays highest-ranked from 0% up to ~76.8% physical-exposure weighting, well past the 50/50 weighting actually used, with Maldives overtaking only beyond that point.

## Validation & Robustness Checklist

- ✓ Two ecosystems tested independently — no uniform-decline assumption
- ✓ Mann-Kendall trend test on the full 24-year coral series (not just period comparison)
- ✓ 3 independent time points for mangroves (1996 / 2010 / 2020)
- ✓ Population-weighted exposure recomputation as a cross-check
- ✓ Full 0–100% weighting-sensitivity sweep (compound score robustness)
- ✓ SLR-threshold sensitivity check across 0.5m / 1.0m / 1.5m thresholds
- ✓ Honest null result reported — H2 (mangrove decline) not supported
- ! Governance correlation flagged as not statistically significant (suggestive only)

**Honest Limitation:** The governance-alignment test (protected-area coverage vs. verified vulnerability) shows a moderately strong positive correlation (r=0.718) but doesn't reach statistical significance at this sample size (p=0.172, 95% CI: -0.45 to 0.98) — a genuine limitation of testing only five islands, which I'm reporting as suggestive rather than confirmed. The Compound Vulnerability Score also uses min-max normalization, so scores are relative within this five-island sample rather than absolute — Canary Islands' score of 0.000 reflects the lowest raw values in this sample, not the absence of risk. I also corrected Canary Islands' physical-exposure figure (0.3% of settlements at risk) during data-quality review, to exclude DEM NoData artifacts I'd initially misread as sea-level settlements — see the Research Paper's Limitations section for the full explanation.

## Real-World Relevance

Climate adaptation funding for small island nations is frequently allocated using single-indicator exposure metrics. This project's central methodological argument — that exposure and true compound risk are not the same thing, and that ecosystem buffers do not degrade uniformly — has direct implications for how conservation and adaptation resources should be prioritized across islands and ecosystem types.

---

GitHub: [github.com/sakshimaske303-commits/DOUBLE-JEOPARDY](https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY) | Live Dashboard: [double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app) | Zenodo DOI: [10.5281/zenodo.21739961](https://doi.org/10.5281/zenodo.21739961)

**Sakshi D. Maske** — Independent Geospatial Researcher
