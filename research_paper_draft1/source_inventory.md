# Source inventory and literature synthesis: Draft 1

## 1. Project materials examined

| File / location | Role | How inspected | Status and notes |
|---|---|---|---|
| `report/main.pdf` (14 pp., IEEE Access layout) | Main report of the work | Full text extracted with `pdftotext`; tables cross-checked against CSV and notebook outputs | **Report of record.** Built before merge `5b99f4d`. Table 6 extracts badly (CV column shifted); the CSV is the authority for its values. |
| `report/main.tex` | LaTeX source of the report | Read; HEAD side extracted to scratch | **Contains 10 unresolved, committed merge conflicts** (HEAD = IEEE version, other side = older article version). Not modified. → AQ18 |
| `report/abstract/abstract.tex`, `abstract.pdf` | Intended paper abstract | `.tex` read in full | 248 words, so above IST-Africa's 100–150-word limit. Rewritten for Draft 1. Its numbers all match the artifacts. |
| `report/pipeline_update_notes.md` | Change log, Rounds 1–7 | Read in full | Also contains committed merge-conflict markers. Useful record of which numbers were deliberately excluded (e.g. an unsupported sensitivity table). |
| `report/template/template.tex`, `references.bib` | Generic LaTeX "ML paper" template (commit cce9a1a) | Listed | **Not** the IST-Africa template; not used. |
| `report/figures/*.png` (≈90) | Report figures | Listed; not re-rendered | Almost all are in colour. IST-Africa prints in black and white and asks for no colour → not reused. A new greyscale Fig. 1 was made instead. |
| `train.ipynb` (558 cells, 348 code) | Full pipeline with stored outputs | Parsed as JSON; outputs searched and read by cell. **Not executed.** | 0 error outputs. Stored paths show it ran from a Claude Code scratchpad virtualenv → relevant to the AI declaration (AQ15). |
| `deployment_outputs/model_validation_comparison.csv` | Main results table | Read in full | Primary source for Table 3 and Fig. 1. |
| `deployment_outputs/deployment_metadata.json`, `run_resource_report.json`, `kaggle_run_log.txt`, `kaggle_run_metrics.json` | Run metadata, resources, latency | Read | "Kaggle" files describe a **local** run (`run_platform: Local machine`). |
| `deployment_outputs/test_predictions_standalone.csv` | Standalone inference output | Shape and columns checked | Exact reproduction confirmed in NB cells 502–513. |
| `evidently_*.json/.csv/.html` (root and `deployment_outputs/`) | Drift reports | Summary CSV read; HTML not opened | Values match NB outputs. |
| `serve_model.py` | Deployed API | Read in full | Contradicts the report on where time features are computed (AQ12). No secrets present; CORS origins come from the environment. |
| `DEPLOYMENT.md`, `HUGGINGFACE.md` | Deployment docs | `DEPLOYMENT.md` partly read | `DEPLOYMENT.md` has committed merge conflicts; its two sides disagree on the Kaggle outcome (AQ11). Contains public URLs and a Hugging Face user name, which must not appear in the review version. |
| `Sensor Data Jan - July 2026.csv`, `AirQo_August_2026_hourly_matched*.csv` | Datasets | **Not opened directly.** Schema and counts taken from NB outputs. | No personal data expected (sensor records). Licence and permission to publish not documented (AQ8). |
| `Assignment 4 - AirQo PM2.5 Prediction.pdf`, `AI Model Deployment and Scalability Assignment 4.pdf` | Course briefs | Text extracted and searched | The report's "39 µg/m³ Kampala annual mean" claim is not in either brief (AQ17). The briefs show the work began as coursework (AQ19). |
| `report/slides/*.pptx`, `huggingface/*`, `output.png`, `.joblib` | Slides, HF bundle, models | Listed only | Not needed for the paper. |
| Git history | Provenance | `git log`; `git show 245c2e2:train.ipynb` searched | Phase 1 values confirmed in commit 245c2e2. |

## 2. Official conference sources (retrieved 29 Oct 2026)

Copies are kept outside the repository, in the session scratchpad. See `ist_africa_compliance.md`.

- Submission page, Paper Guidelines page, GenAI Policy, Editorial Policy, Publication Ethics (HTML)
- Call for Papers PDF (2 pp.)
- `IST-AfricaTemplate.dot` (Word 2000 template; no VBA project) and `IST-AfricaGuidelinesforPaperPreparation.doc` (4 pp.; no VBA project). Both opened with macros force-disabled.

## 3. Scholarly sources

Only **one** scholarly paper is present in full text in the repository: Febrian & Permai (2025). The other references are the ones the authors cited in `report/main.pdf`. For each I checked the bibliographic identity (Crossref, Semantic Scholar, arXiv, NeurIPS or JMLR pages); I did **not** read their full texts. No new scholarly source was introduced.

| Ref | Source | Full text? | Identity verified via | What Draft 1 uses it for | Detail withheld pending author check |
|---|---|---|---|---|---|
| [1] | WHO Global Air Quality Guidelines (2021) | No | ISBN in report | 5 µg/m³ annual guideline | – |
| [2] | Okure et al., ES&T 56(6) 2022 | No | Crossref | AirQo low-cost sensing context | – |
| [3] | Sserunjogi et al., Data in Brief 44, 2022 | No | Crossref | AirQo dataset | "68 stations, 2019–2020" (AQ2) |
| [4] | Adong et al., Applied AI Letters 3(3) e76, 2022 | No | Crossref | Calibration of AirQo sensors | RMSE 18.6→7.2; >120 devices (AQ3) |
| [5] | Lsoto et al., JAWMA 76(6) 2026 | No (abstract only) | Crossref, S2 abstract | 11 LCS vs BAM, 13 months, Kampala | "agree less well at high values / hourly" (AQ4) |
| [6] | Wang & Ogawa, IJERPH 12(8) 2015 | No | Crossref | Meteorology–PM2.5 | Specific findings omitted |
| [7] | Yang et al., IJERPH 14(12) 1510, 2017 | No | Crossref | Seasonal and regional variation | – |
| [8] | Wabinyai et al., Atmos. Environ. X 29, 2026 | No | Crossref, S2 | Kampala/Fort Portal, meteorology + lagged PM2.5 | 57%/80% explained; lag effect (AQ5) |
| [9] | Febrian & Permai, E3S Web Conf. 680, 2025 | **Yes, read** | Crossref + PDF | Pollutant history sufficient; meteorology limited | – |
| [10] | Niyonzima et al., Discover AI 6, art. 1039, 2026 | No | Crossref | One-hour-ahead RNN forecasting on AirQo | 759,480 obs; 68 sites; MAE 8.71; R² 0.68 (AQ6) |
| [11] | Gürtepe et al., EMS 192, 106586, 2025 | No | Crossref | Station-withheld validation | RMSE 9.21 vs 8.28 (AQ7) |
| [12] | Cao et al., BRITS, NeurIPS 2018 | No | arXiv 1805.10572 | Imputer design | – |
| [13] | Hochreiter & Schmidhuber 1997 | No | Crossref | LSTM | – |
| [14] | Chawla et al. 2002 | No | Crossref | SMOTE | – |
| [15] | Torgo et al. 2013 | No | Crossref | SMOTE for regression | – |
| [16] | Lundberg & Lee 2017 | No | arXiv 1705.07874 | SHAP | – |
| [17] | Lundberg et al. 2020 | No | Crossref | TreeExplainer | – |
| [18] | Breiman 2001 | No | Crossref | Random forest | – |
| [19] | Ke et al. 2017 | No | NeurIPS proceedings page | LightGBM | – |
| [20] | Pedregosa et al. 2011 | No | JMLR page | scikit-learn | – |
| [21] | Evidently 0.7.23 | n/a | requirements.txt | Drift monitoring | – |

The report also cited Saminathan & Malathy (2023). Draft 1 leaves it out because the paper does not need it.

**Corrections to the report's bibliography:**
- [10] needs article number 1039.
- [4] needs article number e76.
- [15] needs LNCS volume 8154 (from the authors' notes; this is consistent with the DOI prefix but was not checked separately).

## 4. Thematic synthesis

**Theme A: data quality is the binding constraint in low-cost networks.** The AirQo literature [2]–[5] treats calibration and intermittent availability as properties of the network, not incidental noise. Our record shows the same problems in extreme form: eight days of data, 28.8% weather dropouts, and PM2.5 > PM10 in 22.4% of rows. The literature supplies the context. It does not settle how calibration error affects our models.

**Theme B: weather matters, but its effect is place- and season-dependent.** Two of the sources [6], [7] report meteorological effects that vary by threshold, season and region, and [8] adds a Kampala-specific analysis. Read together, they imply that a model needs records spanning conditions to learn those effects. Our SHAP results (weather at 5–8% of attribution) fit that implication, but they do not test it. The papers agree on the existence of weather effects. They differ on direction (humidity in [7]) and use daily or longer aggregates, while we work hourly.

**Theme C: pollutant history carries most short-term skill.** Febrian & Permai [9] (read in full) found that pollutant-only inputs gave the most consistent LSTM forecasts, with meteorology adding limited benefit. They worked with two years of daily data in one city, and seven-day horizons. According to the authors' report, [8] and [10] also benefit from lagged PM2.5; this needs checking against those papers. Our result reaches the same direction at an hourly horizon from a far shorter record. Because horizons and data differ, these papers support the direction of our finding, not its size.

**Theme D: validation design changes conclusions.** The emphasis in [11] on station-withheld evaluation parallels our leave-sensors-out design. None of the sources we examined combines time-aware cross-validation, sensor-withheld evaluation and an out-of-period test on a record this short. That is the gap claimed in Draft 1, and it is limited explicitly to the literature examined.

**Theme E: methods borrowed.** BRITS [12], SMOTE/SMOTER [14], [15] and SHAP [16], [17] are used as tools, not studied. Our downstream imputation test is an application-level check, not a contribution to imputation methods.

**What the folder cannot support:** any statement about how common very short records are among African networks, or that "no study" has addressed short records. Draft 1 avoids both.
