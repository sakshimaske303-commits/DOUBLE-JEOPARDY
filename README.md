# DOUBLE JEOPARDY: The Vulnerability Spiral

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint-B7410E.svg)](https://eartharxiv.org/repository/view/14826/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21739961.svg)](https://doi.org/10.5281/zenodo.21739961)

**How many people on five island groups live at or below 1 m, how reef heat stress has changed around them, and whether protection and coastal building rules follow that risk.**

## Live Dashboard

**[View the interactive dashboard →](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`DJ_Executive_Summary.pdf`](./paper/DJ_Executive_Summary.pdf) / [`.md`](./paper/DJ_Executive_Summary.md) | One page snapshot: project overview, question, method, headline findings, limitations, and links (fastest overview; start here) |
| [`DJ_Research_Paper.md`](./paper/DJ_Research_Paper.md) | Research paper: literature review, methods, results, limitations |
| [`DJ_Development_Log.md`](./paper/DJ_Development_Log.md) | Full technical development log: every bug, debugging session, and methodology iteration |
| [`DJ_Declarations.pdf`](./paper/DJ_Declarations.pdf) / [`.md`](./paper/DJ_Declarations.md) | Declarations: highlights, contributions, funding, data licences, reproducibility, what changed from version 1, AI assistance |

---

DOUBLE JEOPARDY looks at two threats to low islands together: the sea rising, and the reefs and mangroves that hold it back weakening. It measures both across 5 island groups in 3 ocean basins (Maldives, Lakshadweep, Seychelles, Fiji, Canary Islands), tests each ecosystem separately, and shows how much the answer depends on the elevation model, the exposure measure and the weighting.

---

Interactive geospatial maps are hosted separately via GitHub Pages. Sample links:

**Ecosystem Buffer Overview** (Python/folium)
- [Maldives: Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/maldives_ecosystem_buffer_webmap/index.html)
- [Seychelles: Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/seychelles_ecosystem_buffer_webmap/index.html)
- [Fiji: Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/fiji_ecosystem_buffer_webmap/index.html)
- [Canary Islands: Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/canary_ecosystem_buffer_webmap/index.html)
- [Lakshadweep: Ecosystem Buffer](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/lakshadweep_ecosystem_buffer_webmap/index.html)

**Sea Level Rise Exposure** (Python/folium)
- [Maldives: SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/maldives_slr_exposure_webmap/index.html)
- [Seychelles: SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/seychelles_slr_exposure_webmap/index.html)
- [Fiji: SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/fiji_slr_exposure_webmap/index.html)
- [Canary Islands: SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/canary_slr_exposure_webmap/index.html)
- [Lakshadweep: SLR Exposure](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/lakshadweep_slr_exposure_webmap/index.html)

**Settlement Encroachment (NDBI change, 2016→2024)**
- [Maldives: Settlement Encroachment](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/maldives_settlement_encroachment_webmap/index.html)
- [Seychelles: Settlement Encroachment](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/seychelles_settlement_encroachment_webmap/index.html)
- [Fiji: Settlement Encroachment](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/fiji_settlement_encroachment_webmap/index.html)

*(For the full interactive experience with dynamic legends and key observations, visit the [live dashboard](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app/) → Interactive Maps & Plots page)*

**Interactive Plots**
- [Compound Vulnerability Score](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/compound_vulnerability_score.html)
- [Coral Thermal Stress Trends](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/coral_thermal_stress_trends.html)
- [Weighting Sensitivity Curve](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/weighting_sensitivity_curve.html)
- [Coastal Setback Coverage](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/outputs/plots/interactive/setback_coverage_curve.html)

---

## What This Project Does

- Measures **sea-level-rise exposure** as the share of people (WorldPop 2020) living at or below 1 m, on a **bare-earth elevation model** (DeltaDTM v1.1), with the Copernicus GLO-30 surface model kept for comparison. The share of OpenStreetMap named places at or below 1 m (7,647 points with a usable elevation) is a second measure, and 0.5 m and 1.5 m are sensitivity checks
- Tracks **mangrove extent** at 3 time points (1996, 2010, 2020) and **reef heat stress** as mean Degree Heating Weeks over all mapped reef cells, 1996–2020, tested as 2 separate hypotheses instead of one combined assumption
- Combines exposure and the change in reef heat stress into a **compound score**, and sweeps the weighting from 0 to 100% to show where the ranking changes
- Describes whether **protected-area coverage of the 10 km coastal zone** follows that risk (4 island groups; descriptive, not a test)
- Tests whether each government's **statutory coastal setback** reaches the buildings on low land, using about 1.35 million building footprints (Overture Maps) and the setback written in national law
- Adds **built-up change on land** from Sentinel-2 NDBI (2016–2024) as supporting context
- Presents everything in an interactive Streamlit dashboard that reads its numbers directly from the analysis CSVs, with Python (folium) maps and Plotly plots

## Key Findings

All numbers below are written by `python scripts/run_all.py` to the CSVs in `data/`; the dashboard and figures read the same files.

**1. The elevation model changes the answer more than anything else.** On a surface model, roofs and tree canopy are read as ground. On the bare-earth model, the share of people at or below 1 m is:

| Island group | Bare earth (DeltaDTM) | Surface (Copernicus) | People at or below 1 m |
|---|---:|---:|---:|
| Maldives | 11.82% | 8.88% | 57,889 |
| Lakshadweep | 6.40% | 0.79% | 4,238 |
| Seychelles | 2.07% | 0.43% | 1,933 |
| Fiji | 0.28% | 0.21% | 2,460 |
| Canary Islands | 0.19% | 0.15% | 3,946 |

Counting named places instead of people gives a different picture: Maldives 28.8% and Seychelles 24.7% are close, because Seychelles has many small, low coral islets with few residents. People are the main measure.

**2. Reef heat stress rose, but no trend is significant once serial correlation is accounted for.** Mean DHW over mapped reef rose between 1996–2000 and 2016–2020 on every reef island, most in Seychelles (+0.52 °C-weeks). A seasonal Mann-Kendall test corrected for serial correlation (DHW is a 12-week running sum) gives p = 0.14 for Seychelles, 0.31 for the Maldives, 0.55 for Fiji and 0.90 for Lakshadweep. Without the correction Seychelles (p = 0.002) and the Maldives (p = 0.049) would look significant; the first version of this project reported that.

**3. Mangrove extent shows no decline** on any of the 3 islands where it is mapped (Global Mangrove Watch: Fiji 485.7 → 488.4 km²). On the atolls, patches are close to the pixel size, so small losses may not be detectable.

**4. Which island is "most vulnerable" depends on the weighting.** At equal weights the compound score is Seychelles 0.58, Maldives 0.56, Lakshadweep 0.32, Fiji 0.28, Canary Islands 0.00. Exposure points to the Maldives and reef heat stress to Seychelles, so the top island switches to the Maldives once exposure carries 52% or more of the weight. The score is a descriptive ranking within this sample, not an absolute measure.

**5. Protection does not track risk in this sample.** Coastal-zone protection ranges from 1.3% (Maldives) to 71.4% (Seychelles) and is unrelated to the compound score (r = −0.10, 95% interval −0.97 to 0.95, n = 4; Lakshadweep has no WDPA record). Removing Seychelles alone moves r to −0.95, so this is a description of four island groups, not a finding that generalises.

**6. Coastal setbacks miss most low-lying buildings outside the Canary Islands.** For every building footprint, bare-earth elevation and distance to the shoreline were compared with the setback in national law:

| Island group | Buildings at or below 1 m | Statutory setback | Low buildings landward of every setback | Distance covering 90% of them |
|---|---:|---|---:|---:|
| Maldives | 13.4% (15,392) | none for inhabited islands | 99.4% | 225 m |
| Lakshadweep | 4.7% (444) | 20 m | 93.2% | 345 m |
| Seychelles | 4.6% (2,440) | 25 m | 92.0% | 427 m |
| Fiji | 0.5% (1,397) | none | 99.8% | 463 m |
| Canary Islands | 0.02% (192) | 100 m (20 m urban) | 15.1% | 122 m |

The 20 m and 25 m rules reach fewer than one in ten low buildings, which stand a median 80–136 m inland; Spain's 100 m Ley de Costas line covers 85% because low land in the Canaries is a narrow beachfront strip. On atolls low land is most of the island, so a distance rule, however wide, measures the wrong thing (Section 4.8 of the paper).

**What changed from version 1.** Version 1 reported 78.3% of Seychelles settlements at risk, significant coral trends in the Maldives and Seychelles, a ranking that "held at every weighting", and a governance correlation of r = 0.965 (p = 0.035). Each of these came from a measurement choice that did not hold up: NoData elevation values counted as sea level, OSM points that are mostly island names, a surface elevation model, one 5 km DHW cell per island, a trend test that ignored serial correlation, and protected areas counted twice over a land-area denominator. The [Development Log](./paper/DJ_Development_Log.md) records each correction.

## Repository Structure

```text
DOUBLE_JEOPARDY/
├── paper/                           # All formal write-ups, markdown + PDF
│   ├── DJ_Research_Paper.md / .pdf  # Formal academic research paper
│   ├── DJ_Executive_Summary.md / .pdf
│   └── DJ_Development_Log.md / .pdf # Full technical development log
├── scripts/                         # All analysis code, grouped by pipeline stage
│   ├── acquisition/                 # download_*.py + auth_sentinelhub.py: raw data pulled from source APIs
│   ├── processing/                  # clean_*.py, filter_*.py, normalize_*.py, precompute_*.py: raw to analysis-ready
│   ├── analysis/                    # population_weighted_exposure.py, governance_correlation_test.py,
│   │                                 #   coral_trend_test.py, compound_vulnerability_score.py, etc.
│   │                                 #   the scripts that produce the paper's actual reported numbers
│   ├── figures/                     # build_*_map.py, map1_*.py, research_paper_figures.py,
│   │                                 #   build_interactive_plots.py: everything that renders a figure
│   ├── validation/                  # debug_*.py, verify_*.py, test_*.py, validate_*.py: sanity checks, not
│   │                                 #   part of the reported pipeline, kept for audit trail
│   └── local_fixes/                 # One-off local correction scripts (boundary rebuild, coral spatial
│                                     #   average, etc.), each documented in the Development Log
├── dashboard/                       # Streamlit dashboard (10 pages)
│   └── static/                      # Interactive map exports, built in Python (folium) (served via GitHub Pages)
├── data/                            # Processed datasets across 5 islands, 11+ categories
│   ├── settlements/, ecosystem_buffers/, terrain/ (incl. deltadtm/), population/
│   ├── boundaries/, boundaries_v2/, mangroves/, coral_bleaching/
│   ├── settlement_encroachment/
│   └── buildings/                   # Overture building points (not committed; rebuilt by the scripts)
├── outputs/
│   └── plots/                       # Publication quality static figures for the Research Paper
│       └── interactive/             # Plotly interactive HTML charts (compound vulnerability score,
│                                     #  coral thermal stress trends, weighting sensitivity curve,
│                                     #  setback coverage curve)
├── qgis_processing/                 # Superseded QGIS2Web (OpenLayers) webmap exports; the live maps are
│                                     #  the folium maps in dashboard/static/ built by scripts/figures/
├── README.md
├── LICENSE
├── CITATION.cff
└── requirements.txt
```

All scripts under `scripts/` read and write paths (like `data/terrain/...` or `outputs/plots/...`) relative to the repository root, not to the script's own folder — so every script here is still meant to be run from the `DOUBLE_JEOPARDY/` root, e.g. `python scripts/analysis/population_weighted_exposure.py`, not from inside its subfolder.

## Reproducing the Analysis

Large rasters (`*.tif`: Copernicus and DeltaDTM tiles, WorldPop, NDBI) are not committed (see `.gitignore`), and WDPA extracts may not be redistributed (see `DATA_SOURCES_AND_LICENSES.md`). To rebuild everything from the repository root:

```bash
pip install -r requirements.txt
python scripts/acquisition/export_deltadtm_gee.py --project <your-earth-engine-project>   # DeltaDTM tiles to Google Drive
# download the exported tiles into data/terrain/deltadtm/gee/
python scripts/run_all.py --download   # fetch Copernicus DEM tiles + reef-cell DHW, build DeltaDTM VRTs, run every step
python scripts/run_all.py              # re-run analysis, figures, maps and dashboard data only
```

Every reported number is written to a CSV in `data/` (e.g. `slr_exposure_summary.csv`, `population_weighted_exposure.csv`, `coral_trend_results.csv`, `compound_vulnerability_scores.csv`, `governance_alignment_summary.csv`, `ndbi_land_change.csv`, `setback_calibration_summary.csv`), and the figures and dashboard read those files. Elevation sampling for all islands uses one shared rule in `scripts/common/dem_sampling.py`. The setback analysis needs building footprints, which are too large to commit: run `python scripts/acquisition/download_buildings_overture.py` (needs `pip install overturemaps`) and `python scripts/processing/export_building_points.py` once, and `run_all.py` then includes `scripts/analysis/setback_calibration.py`. The DeltaDTM export needs the Earth Engine Python API (`pip install earthengine-api`) and an Earth Engine project; everything else runs without it.

Two checks recompute key results independently: `scripts/validation/coral_trend_check.py` (coral trend p-values without pyMannKendall; they agree to within 0.005) and `scripts/validation/setback_distance_check.py` (setback distances on the WGS84 ellipsoid; fewer than 0.1% of sampled buildings change side of any setback line). `run_all.py` runs both and ends with COMPLETE RUN or PARTIAL RUN.

## Tech Stack

Python · Google Earth Engine · Overture Maps · GeoPandas · Rasterio · Folium · SciPy · PyMannKendall · Plotly · Streamlit · GitHub Pages · Sentinel Hub API · NOAA Coral Reef Watch API · Global Mangrove Watch

## Data Sources

| Dataset | Provider |
|---|---|
| Named places | OpenStreetMap |
| Mangrove Extent (1996/2010/2020) | Global Mangrove Watch |
| Coral Reef Extent | WCMC / OpenStreetMap |
| Coral Thermal Stress | NOAA Coral Reef Watch (Degree Heating Week) |
| Protected Areas | World Database on Protected Areas (WDPA) |
| Bare-earth elevation (main) | DeltaDTM v1.1 (Pronk et al. 2024) |
| Surface elevation (comparison) | Copernicus DEM GLO-30 |
| Population | WorldPop 2020 |
| Building footprints | Overture Maps (OpenStreetMap, Google Open Buildings, Microsoft ML Buildings, Esri, IGN España) |
| Built-up change (supplementary) | Sentinel-2 (NDBI) |

Full citations, licences and attribution requirements: [`DATA_SOURCES_AND_LICENSES.md`](./DATA_SOURCES_AND_LICENSES.md).

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY.git
cd DOUBLE-JEOPARDY
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

Note: The dashboard runs directly on the processed data already included in data/, no API keys required. The raw data acquisition scripts (e.g. download_coral_bleaching_stress.py, auth_sentinelhub.py) require a free Sentinel Hub account; credentials should be placed in a local .env file (see .gitignore; this file is not committed)

## Declarations

Full text: [`paper/DJ_Declarations.pdf`](./paper/DJ_Declarations.pdf).

- **Authorship:** single author; I designed and carried out every stage, from data and code to writing and figures.
- **Funding and interests:** no funding was received, and there are no competing interests.
- **Ethics:** no human participants, animals or personal data, so no approval was needed.
- **Data licences:** my code and text are CC BY 4.0, while third-party data keep their own licences; WDPA extracts are not redistributed (see `DATA_SOURCES_AND_LICENSES.md`).
- **AI assistance:** The questions, the choice of islands and data, the methods, the decision to withdraw the six first-version results and the interpretation are mine. Within that work I used Claude (Anthropic), an AI assistant, in a supporting role. Its main job was cross-checking: comparing the exposure shares, reef heat-stress figures, compound scores and setback coverage quoted in the paper, executive summary, README and dashboard against the CSV files my scripts produce. I also asked it for help when one of my Python scripts broke or gave output I could not account for, and for the layout of the project web pages. The paper and other documents are my own writing; I used the assistant to flag wording that was unclear or overly technical, gaps where something seemed to be missing, and punctuation, and I decided which of those points to act on. It did not acquire or process the elevation, population, building, reef or mangrove data, and it did not run the analysis. I reviewed everything it suggested before using it, and the responsibility for the content is mine.

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](./LICENSE), free to share and adapt, with attribution. See `CITATION.cff` for citation metadata.

---

*This project's full development process, including every debugging session, methodology iteration, and technical decision, is documented in `paper/DJ_Development_Log.md`.*
