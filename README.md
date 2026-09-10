# DOUBLE JEOPARDY — The Vulnerability Spiral

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint-B7410E.svg)](https://eartharxiv.org/repository/view/14826/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21739961.svg)](https://doi.org/10.5281/zenodo.21739961)

**Testing whether compound coastal climate vulnerability is real — and whether it affects every ecosystem equally.**

## Live Dashboard

**[View the interactive dashboard →](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`DJ_Executive_Summary.pdf`](./DJ_Executive_Summary.pdf) / [`.md`](./DJ_Executive_Summary.md) | One-page snapshot — project overview, question, method, headline finding, robustness checklist, and links (fastest overview; start here) |
| [`DJ_Research_Paper.md`](./DJ_Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| [`DJ_Development_Log.md`](./DJ_Development_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

DOUBLE JEOPARDY is a geospatial framework that independently tests physical sea-level-rise exposure and ecosystem buffer degradation across five islands spanning three ocean basins. Rather than assuming mangroves and coral reefs degrade together, each ecosystem is tested independently — revealing that climate vulnerability is not the uniform story it is often assumed to be.

Built on a **"Trust, But Verify"** philosophy — every hypothesis in this project is tested rigorously, and every finding is reported honestly, including where the original hypothesis was not supported.

---

Interactive geospatial maps are hosted separately via GitHub Pages. Sample links:

**Ecosystem Buffer Overview** (Python/folium)
- [Maldives — Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/maldives_ecosystem_buffer_webmap/index.html)
- [Seychelles — Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/seychelles_ecosystem_buffer_webmap/index.html)
- [Fiji — Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/fiji_ecosystem_buffer_webmap/index.html)
- [Canary Islands — Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/canary_ecosystem_buffer_webmap/index.html)
- [Lakshadweep — Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/lakshadweep_ecosystem_buffer_webmap/index.html)

**Sea-Level-Rise Exposure** (Python/folium)
- [Maldives — SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/maldives_slr_exposure_webmap/index.html)
- [Seychelles — SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/seychelles_slr_exposure_webmap/index.html)
- [Fiji — SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/fiji_slr_exposure_webmap/index.html)
- [Canary Islands — SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/canary_slr_exposure_webmap/index.html)
- [Lakshadweep — SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/lakshadweep_slr_exposure_webmap/index.html)

**Settlement Encroachment (NDBI change, 2016→2024)**
- [Maldives — Settlement Encroachment](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/maldives_settlement_encroachment_webmap/index.html)
- [Seychelles — Settlement Encroachment](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/seychelles_settlement_encroachment_webmap/index.html)
- [Fiji — Settlement Encroachment](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/fiji_settlement_encroachment_webmap/index.html)

*(For the full interactive experience with dynamic legends and key observations, visit the [live dashboard](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app/) → Interactive Maps & Plots page)*

**Interactive Plots**
- [Compound Vulnerability Score](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/compound_vulnerability_score.html)
- [Coral Thermal Stress Trends](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/coral_thermal_stress_trends.html)
- [Weighting Sensitivity Curve](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/weighting_sensitivity_curve.html)

---

## What This Project Does

- Tests physical sea-level-rise exposure at the settlement level across all five islands, using elevation data intersected with over 6,000 individual settlement points — complemented by a population-weighted recomputation using WorldPop 2020 data
- Independently tracks **mangrove extent** across three time points (1996, 2010, 2020) and **coral reef thermal stress** across a 24-year, monthly-sampled satellite record (1996–2020) — treating them as two separate hypotheses, not one combined assumption
- Combines physical exposure and ecosystem degradation into a single **Compound Vulnerability Score**, checking whether a single exposure measure alone would agree with a composite that also accounts for ecosystem condition
- Tests whether formal protected-area governance is statistically aligned with verified vulnerability, or represents a "paper park" gap between policy and evidence
- Tests whether settlement expansion is rising in the same broad coastal area as each island's ecosystem buffers, using satellite-derived built-up area change (2016–2024)
- Presents all findings through an interactive Streamlit dashboard with live-recalculating features, Python (folium) interactive maps, and Plotly interactive plots

## Key Findings

**Coral thermal stress is rising; mangrove extent shows no measurable decline.** Four of five islands show a measurable, rising coral thermal-stress trend over 24 years — most severely in Seychelles — based on a continuous 24-year Mann-Kendall trend test. Mangrove extent, assessed at three independent time points (a coarser snapshot comparison, not a continuous trend test), shows no measurable decline in any tested island. This asymmetry — rather than a uniform "ecosystems are collapsing" narrative — is the project's central empirical contribution.

**Seychelles is the highest-risk island on every measure tested.** Settlement-based exposure (78.3% of settlements at risk), population-weighted exposure (17.6% of population), and the overall Compound Vulnerability Score all point to Seychelles — a correction from an earlier version of this project, where a DEM data-quality problem in the Maldives and Lakshadweep elevation files made those two islands look far more exposed than they actually are, creating an appearance of disagreement between indicators that turned out not to be real once the underlying data was fixed.

**Governance alignment is positive and reaches statistical significance, on a very small sample.** A strong correlation (r=0.965, n=4 — Lakshadweep excluded, no WDPA measurement available for it) exists between protected-area coverage and verified vulnerability, reaching p=0.035 — though with only four data points, this is read as a stronger signal rather than confirmed proof; a single data point could move both the coefficient and the p-value substantially at this sample size.

**Findings hold up under robustness checks.** The coral thermal-stress trend is confirmed statistically significant via a seasonal Mann-Kendall test for Maldives (p=0.0046) and Seychelles (p=0.0069); the Compound Vulnerability ranking holds across the entire 0–100% physical-exposure weighting range, not just the 50/50 weighting actually used; and physical exposure recomputed on a population-weighted basis agrees with the settlement-based ranking.

Full methodology, including three hypotheses tested — one supported, one not supported, and one suggestive but statistically inconclusive — is documented in the dashboard's Methodology page and in `DJ_Research_Paper.md`.

## Repository Structure

```text
DOUBLE_JEOPARDY/
├── dashboard/                       # Streamlit dashboard (10 pages)
│   └── static/                      # Interactive map exports, built in Python (folium) (served via GitHub Pages)
├── data/                            # Processed datasets across 5 islands, 11 categories
│   ├── settlements/, ecosystem_buffers/, terrain/, population/
│   ├── cyclone_tracks/, boundaries/, mangroves/, coral_bleaching/
│   └── settlement_encroachment/
├── build_interactive_plots.py       # Plotly interactive chart generation
├── outputs/
│   └── plots/                       # Publication-quality static figures for the Research Paper
│       └── interactive/             # Plotly interactive HTML charts
│                                     # (compound vulnerability, physical exposure, population-weighted
│                                     #  comparison, mangrove extent, coral trends, governance alignment,
│                                     #  weighting-sensitivity curve)
├── qgis_processing/                 # Original QGIS2Web webmap exports
├── DJ_Research_Paper.md             # Formal academic research paper
├── DJ_Development_Log.md            # Full technical development log
├── download_*.py                    # Dataset acquisition scripts
├── clean_*.py / filter_*.py         # Data cleaning and filtering scripts
├── map*.py                          # Static visualization scripts
├── research_paper_figures.py        # Generates all Research Paper figures (Figures 2–7) in one run
└── requirements.txt
```

## Tech Stack

Python · GeoPandas · Rasterio · Folium · SciPy · PyMannKendall · Plotly · Streamlit · GitHub Pages · Sentinel Hub API · NOAA Coral Reef Watch API · Global Mangrove Watch

## Data Sources

| Dataset | Provider |
|---|---|
| Settlements, Tourism, Infrastructure | OpenStreetMap |
| Mangrove Extent (1996/2010/2020) | Global Mangrove Watch |
| Coral Reef Extent | WCMC / OpenStreetMap |
| Coral Thermal Stress | NOAA Coral Reef Watch (Degree Heating Week) |
| Protected Areas | World Database on Protected Areas (WDPA) |
| Elevation, Slope | Copernicus DEM GLO-30 |
| Population | WorldPop |
| Cyclone Tracks | IBTrACS v04r01 |
| Settlement Encroachment | Sentinel-2 (NDBI) |

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY.git
cd DOUBLE-JEOPARDY
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

Note: The dashboard runs directly on the processed data already included in data/ — no API keys required. The raw data-acquisition scripts (e.g. download_coral_bleaching_stress.py, auth_sentinelhub.py) require a free Sentinel Hub account; credentials should be placed in a local .env file (see .gitignore — this file is not committed)

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](./LICENSE) — free to share and adapt, with attribution. See `CITATION.cff` for citation metadata.

---

*This project's full development process — including every debugging session, methodology iteration, and technical decision — is documented in `DJ_Development_Log.md` for full transparency and reproducibility.*