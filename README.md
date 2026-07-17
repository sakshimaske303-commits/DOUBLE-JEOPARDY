# 🌊 DOUBLE JEOPARDY — The Vulnerability Spiral

**Testing whether compound coastal climate vulnerability is real — and whether it affects every ecosystem equally.**

## 🔗 Live Dashboard

**[View the interactive dashboard →](https://double-jeopardy-6ev9trz3dwafsb7panbnxg.streamlit.app/)**

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| 📘 [`Project_Journal.md`](./Project_Journal.md) | Polished project summary — methodology, findings, conclusions (start here) |
| 📗 [`Research_Paper.md`](./Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| 📙 [`Devlopment_Log.md`](./Devlopment_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

DOUBLE JEOPARDY is a geospatial framework that independently tests physical sea-level-rise exposure and ecosystem buffer degradation across five island nations spanning three ocean basins. Rather than assuming mangroves and coral reefs degrade together, each ecosystem is tested independently — revealing that climate vulnerability is not the uniform story it is often assumed to be.

Built on the same **"Trust, But Verify"** philosophy as its companion project, GPIE — every hypothesis in this project is tested rigorously, and every finding is reported honestly, including where the original hypothesis was not supported.

---

Interactive geospatial maps are hosted separately via GitHub Pages and embedded live in the dashboard: **[Browse map exports →](https://sakshimaske303-commits.github.io/DOUBLE-JEOPARDY/dashboard/static/)**

---

## 📊 What This Project Does

- Tests physical sea-level-rise exposure at the settlement level across all five islands, using elevation data intersected with over 6,000 individual settlement points
- Independently tracks **mangrove extent** across three time points (1996, 2010, 2020) and **coral reef thermal stress** across a continuous 24-year satellite record — treating them as two separate hypotheses, not one combined assumption
- Combines physical exposure and ecosystem degradation into a single **Compound Vulnerability Score**, revealing that the island with the highest physical exposure is *not* the island with the highest overall risk
- Tests whether formal protected-area governance is statistically aligned with verified vulnerability, or represents a "paper park" gap between policy and evidence
- Tests whether settlement expansion is concentrated near degrading ecosystem buffer zones, using satellite-derived built-up area change (2016–2024)
- Presents all findings through an interactive Streamlit dashboard with live-recalculating features and QGIS-based interactive maps

## 🔬 Key Findings

**Coral reefs are degrading; mangroves are not.** Four of five islands show a measurable, rising coral thermal-stress trend over 24 years — most severely in Seychelles. Mangrove extent, tested with equal rigor across three independent time points, shows no measurable decline in any tested island. This asymmetry — rather than a uniform "ecosystems are collapsing" narrative — is the project's central empirical contribution.

**Physical exposure alone is misleading.** The Maldives has the highest sea-level-rise exposure of any island tested (99.1% of settlements at risk) — yet Seychelles emerges as the highest overall-risk island once ecosystem degradation is factored in, driven by the most severe coral thermal-stress trend recorded across the sample.

**Governance alignment is suggestive, not confirmed.** A moderately strong positive correlation (r=0.727) exists between protected-area coverage and verified vulnerability, but does not reach statistical significance at this sample size (p=0.164) — reported honestly as a limitation of scale, not glossed over.

Full methodology, including two hypotheses tested and one not supported, is documented in the dashboard's Methodology page and in `Project_Journal.md`.

## 🗂️ Repository Structure

```text
DOUBLE_JEOPARDY/
├── dashboard/                       # Streamlit dashboard (9 pages)
│   └── static/                      # QGIS2Web interactive map exports (served via GitHub Pages)
├── data/                            # Processed datasets across 5 islands, 10 categories
│   ├── settlements/, ecosystem_buffers/, terrain/, population/
│   ├── cyclone_tracks/, boundaries/, mangroves/, coral_bleaching/
│   └── settlement_encroachment/
├── outputs/
│   └── plots/                       # Static map exports (mangrove trend, SLR exposure)
├── qgis_processing/                 # Original QGIS2Web webmap exports
├── Project_Journal.md               # Polished project summary and methodology
├── Research_Paper.md                # Formal academic research paper
├── Devlopment_Log.md                # Full technical development log
├── download_*.py                    # Dataset acquisition scripts
├── clean_*.py / filter_*.py         # Data cleaning and filtering scripts
├── map*.py                          # Static visualization scripts
└── requirements.txt
```

## 🛠️ Tech Stack

Python · GeoPandas · Rasterio · Statsmodels · Plotly · Streamlit · QGIS · QGIS2Web · GitHub Pages · Sentinel Hub API · NOAA Coral Reef Watch API · Global Mangrove Watch

## 📚 Data Sources

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

## ▶️ Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/DOUBLE-JEOPARDY.git
cd DOUBLE-JEOPARDY
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

## 👤 Author

**Sakshi D. Maske**

Independent Geospatial Researcher

---

*This project's full development process — including every debugging session, methodology iteration, and technical decision — is documented in `Devlopment_Log.md` for full transparency and reproducibility.*