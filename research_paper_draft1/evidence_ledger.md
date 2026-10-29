# Evidence ledger: Draft 1, IST-Africa 2027

This ledger lists the significant claims in Draft 1 and where each was checked. It is a quality-control tool. A claim's appearance here does not make it safe to publish; the "Status" column says how far it was verified.

**Sources and abbreviations**
- **NB**: `train.ipynb`. Stored outputs were parsed as JSON; the notebook was **not re-executed**. Cell numbers are 0-based indices in the stored file.
- **CSV**: `deployment_outputs/model_validation_comparison.csv`.
- **META / RES / LOG**: `deployment_outputs/deployment_metadata.json`, `run_resource_report.json`, `kaggle_run_log.txt` (the last is a *local* run log despite its name).
- **REP**: `report/main.pdf` (IEEE Access version, 14 pp.). Page numbers are the PDF's printed page numbers.
- **NOTES**: `report/pipeline_update_notes.md`.
- **GIT**: commit history. `245c2e2` is the Phase 1 (PM10) notebook.
- **SRV**: `serve_model.py`.
- **Crossref / S2**: Crossref and Semantic Scholar metadata, used for identity checks only.

**Status values**
- **V**: verified directly against a primary artifact in this session.
- **V-rep**: taken from the authors' report; consistent with the artifacts, but the underlying output was not located in this session.
- **U**: unverified; needs author action.
- **D**: discrepancy found.

## Data and context

| ID | Claim | Category | Evidence (location) | Status | Notes / limits | Paper location |
|---|---|---|---|---|---|---|
| D1 | 14,600 hourly records, 12 fields, 149 devices | method | LOG "Raw rows: 14,600 from 149 sensors"; NB cell 934 column list (August file, same schema); REP p.3 | V | | §3.1, Table 1 |
| D2 | 145 named sites; no duplicate device-hour pairs | method | REP p.3 | V-rep | Not re-checked in NB outputs | §3.1 |
| D3 | Readings only on 1–3 Jan, 1–2 Apr, 1–3 Jun 2026; 147 network-active hours | method | REP p.3, Fig. 1; NB uses 147-hour basis for offline classes | V-rep | Count "147" appears 41 times in NB outputs | §1, §3.1, Table 1 |
| D4 | c. 28.8% of AirQo-device rows have 0 °C and 0% humidity | method | NB output containing "airqo 28.8"; REP p.3 | V | | §3.1, Table 1 |
| D5 | PM2.5 > PM10 in 22.4% of rows | method | REP p.3; NOTES Round 5 | V-rep | Not found in current NB outputs; probably a Phase 1 output (commit 245c2e2) → AQ9 | §3.1 |
| D6 | 14,275 valid PM2.5 readings; train 11,633 / test 2,642 | method | LOG; `kaggle_run_metrics.json` | V | | Table 1, Table 2 |
| D7 | Hold-out is 2 Jun 00:00 to 3 Jun 03:00, 28 hours | method | NB cell 435 "Test period: 02 Jun 00:00 to 03 Jun 03:00 (28 hours, 149 sensors)" | V | | Table 2, §6 |
| D8 | August file: 73,274 rows, 125 sensors, all AirQo, all in main data | method | NB cells 934–960 | V | | §3.1, Table 1 |
| D9 | August c. 14% zero weather readings | method | REP p.9 | V-rep | | Table 1 |
| D10 | Mean PM2.5 32.7 raw; hold-out c. 23; August 35.5 | result | REP pp.3–4, 9; NB cell 537 block ("35.5"); META target mean 33.47 after cleaning (training) | V-rep | The hold-out mean 23.4 appears in NB outputs | Table 1, §5.4–5.5 |
| D11 | WHO annual PM2.5 guideline 5 µg/m³ | background | WHO AQG 2021 [1] | V-rep | Standard, widely known value; full text not in repo | §1 |
| D12 | "Kampala annual mean 39 µg/m³ from a 4-year reference study" (in REP) | background | REP p.1 says "the assignment brief cites…" | **D** | **Not found in either brief PDF.** Omitted from Draft 1 → AQ17 | not used |

## Methods and implementation

| ID | Claim | Category | Evidence | Status | Notes | Paper |
|---|---|---|---|---|---|---|
| M1 | PM10 dropped; rationale (fine fraction, co-measurement, not known in advance) | method | REP pp.4–5; NOTES Rounds 3 and 6; SRV docstring "PM10 is not used" | V | The rationale is the authors' argument, not a measured result | §3.2 |
| M2 | Extreme rule Q3+3·IQR per sensor; 225/14,275 (1.5%) at 59 sensors; 223 nearest-normal (median 1 h), 2 median; max 998→415 | method | NB outputs ("225", "998", "415" present); REP p.5; NOTES Round 3 | V | | §3.2 |
| M3 | Three imputers: (a) windowed interpolation (≤3 h, ≥6 readings in 24 h); (b) time-of-day + 12 h offset; (c) BRITS-style BiLSTM, consistency weight 0.1, 1–12 h masks, log PM2.5, no classification head | method | REP pp.5–6; NB cells 430–453 | V (structure) / V-rep (hyperparameters) | Code was inspected only at cell level; weight 0.1 not re-read in code | §3.2 |
| M4 | All fitted components fitted on training part of each split only | method | REP p.5; NB markdown cells 434, 446 ("trained on the fold's training cells") | V-rep | Claimed throughout the NB; not audited line by line | §3.2 |
| M5 | Features: temp, humidity, sin/cos hour, dow, month, one-hot device; history = 1, 2, 3 h lags, mean, count | method | META numeric/categorical feature lists; REP p.6 | V | | §3.2 |
| M6 | 12 models + mean baseline; tuning by grid/random search with TimeSeriesSplit (3 splits, 2 for SVR) | method | CSV rows; REP p.6 | V (models) / V-rep (tuning details) | | §3.3 |
| M7 | Three validation designs (Table 2); LSO folds of 50/50/49 sensors | method | NB cell 448 progress output ("50 unseen sensors (group 1)" … "49 … (group 3)") | V | | Table 2 |
| M8 | Masked-gap test: gaps 1/3/6/12/24 h, one per sensor, 3 repeats, hold-out period | method | NB cells 433–436; REP p.7 | V | | §3.3 |
| M9 | Downstream test with 5 models × 3 designs | method | NB cells 445–450 | V | | §3.3, §5.3 |
| M10 | Evidently 0.7.23; normed Wasserstein / Jensen–Shannon; threshold 0.1 | method | requirements.txt (evidently==0.7.23); NB cell ~546 table ("Wasserstein distance (normed)", 0.1) | V | | §3.3 |
| M11 | SHAP on 400 test rows | method | NB cell 550 progress "83/400"; REP p.8 | V | | §3.3 |
| M12 | Local run: Windows 11, Python 3.13, 16 CPUs, no GPU, c. 56 min, peak 1.23 GB, 346 code cells, 0 errors | impl. | RES; LOG; NB has 348 code cells and 0 error outputs | V / **D (minor)** | 346 vs 348 code cells: NOTES Round 4 says 2 figure cells were added after the full run → AQ10 | §4 |
| M13 | Forecast model file 1.2 MB; saved artifact reproduces predictions exactly | impl. | RES file_sizes (1.17 MB); NB cells 502–503 "Maximum absolute difference: 0.000000000000 … PASS" | V | | §4 |
| M14 | Local latency c. 14 ms single row; 3,576 rows c. 1.4 s | impl. | RES prediction_latency (13.85 ms; 1,444 ms) | V | Local only, not on Render | §4 |
| M15 | Deployment chronology: RunPod (credit), Kaggle (did not complete), Hugging Face (402, static), Render + Vercel | impl. | REP pp.10–11; DEPLOYMENT.md (HEAD side) | V-rep | Cannot verify external services from the repo. DEPLOYMENT.md still contains merge-conflict markers whose two sides disagree on Kaggle ("did not complete" vs "run end to end") → AQ11 | §4 |
| M16 | API takes rows of weather + cyclical features + device and returns PM2.5 and AQI category; `/health` and `/predict` | impl. | SRV docstring and `predict()` | V | | §4 |
| M17 | REP claim: "the service derives the cyclical time features from the timestamp" | impl. | REP p.11 vs SRV docstring "Each row needs … hour_sin, hour_cos …" | **D** | SRV does **not** derive them; perhaps the dashboard does. Draft 1 follows the code → AQ12 | §4 |
| M18 | Only the forecast model is served | impl. | SRV loads `best_pm25_model.joblib` (SVR per META) | V | | §4 |

## Results

| ID | Claim | Category | Evidence | Status | Notes | Paper |
|---|---|---|---|---|---|---|
| R1 | Phase 1 RF: MAE 3.10, RMSE 7.00, R² 0.898, AQI acc. 86.2% | result | GIT 245c2e2 `train.ipynb` contains 3.10313…, 0.898, 86.26…; NOTES Round 5 | V (MAE, R², acc.) / V-rep (RMSE 7.00) | | Abstract, §5.1 |
| R2 | PM10 c. 76% of Phase 1 importance; temp and humidity c. 1% each | result | REP p.4; NOTES Round 5 | V-rep | Not re-checked in the 245c2e2 outputs | §5.1 |
| R3 | Hold-out/CV/LSO MAE, RMSE, R² for all models (Table 3) | result | CSV (exact values) | V | Rounded to 2 d.p. | Table 3, Fig. 1 |
| R4 | History lowers hold-out MAE: RF −11.6%, LightGBM −14.2% | result | CSV: (9.6117−8.5009)/9.6117 = 11.6%; (9.8169−8.4252)/9.8169 = 14.2% | V (recomputed) | | §5.2 |
| R5 | AQI accuracy: SVR 75.2%, mean baseline 74.4% | result | CSV AQI column (0.7517, 0.7438) | V | | §5.2 |
| R6 | MAE vs untouched readings: 9.79 (LGB+H), 10.62 (SVR) | result | NB outputs contain 9.79 and 10.62 | V | | §5.2, §6 |
| R7 | SHAP shares: month 46/32%, sensor 18/27%, temp 8/7%, humidity 5/6%; history 50% for LGB+H | result | REP Table 8 p.7; NOTES Round 3 ("50 %") | V-rep | NB cell 550 gives mean |SHAP| values consistent with month > sensor > hour > weather; percentage table not re-located | §5.2 |
| R8 | MAE by sensor class: SVR 8.73/10.06/10.76; LGB+H 7.66/9.22/10.42 | result | NB outputs contain all six values | V | | §5.2 |
| R9 | Highest test reading 172 predicted as 33 | result | NB output contains "172"; REP p.7 | V-rep | | §5.2 |
| R10 | BiLSTM imputation better in all 15 combinations; mean −20.8% | result | NB cell 453 "Mean change over all variables and gap lengths: -20.8 %" plus table | V | The 15 combinations include PM2.5, but the models only use imputed weather | §5.3, Table 4 |
| R11 | Table 4 imputation MAE values | result | NB cell 436 MAE block | V | | Table 4 |
| R12 | Interpolation filled 618 of 11,423 missing temperature values | result | NB cell 454 | V | | §5.3 |
| R13 | BiLSTM fill SD 11.9 vs 26.8 observed (PM2.5) | result | NB outputs contain 11.9 and 26.8; REP p.7 | V-rep | Pairing not re-read in its cell | §5.3 |
| R14 | Downstream: mean −0.4%, 7 of 15 helped; LSTM+H 10.89→9.48; SVR CV 14.68→16.35 | result | NB cell 456; cells 449–450 (9.476, 16.35) | V | | §5.3 |
| R15 | SMOTE worse for all 8 models; LightGBM 9.82→28.67, RF 9.61→10.10 at 0.25 | result | NB outputs contain 28.67 and 10.10; REP Table 4 p.6 | V (values) / V-rep ("all eight") | | §5.4 |
| R16 | August MAE / R² per model | result | NB cell 537 | V | | Table 3, §5.5 |
| R17 | August daily categories: forecast Moderate on all 31 days, USG on 16, 15 matches; history 17 | result | NB cell 545 "15 of 31"; REP p.9 | V (15) / V-rep (16, 17) | | §5.5 |
| R18 | 76 of 125 August sensors data-rich | result | NB cell ~1067 output ("data-rich 76") | V | | §5.5 |
| R19 | Drift train→August 6 of 9 (month 0.83, dow 0.75 and 0.61, humidity 0.26, sensor 0.25); train→hold-out 8 of 9 | result | NB cells 548 ("6 of 9"), 726–727 ("8 of 9", share 0.889); `evidently_monitoring_summary.csv` | V | | §5.5 |
| R20 | August BiLSTM temperature 1.3 °C at 6 h | result | NOTES "Second dataset"; REP p.9 | V-rep | | §5.5 |
| R21 | Daily Aug 1–14 forecast: 2,082 Moderate, 4 USG of 2,086 | result | NB cell 477 | V | Not used in Draft 1 (space) | – |

## Literature claims

| ID | Claim in Draft 1 | Source | Evidence inspected | Status | Paper |
|---|---|---|---|---|---|
| L1 | Okure et al. characterised ambient air quality in Ugandan urban areas with low-cost sensing | [2] | Crossref title/authors/venue | V (identity only) | §1, §2 |
| L2 | Sserunjogi et al. published an hourly PM2.5/PM10 dataset from the AirQo network | [3] | Crossref title | V (identity). The "68 stations, 2019–2020" detail from REP is omitted → AQ2 | §2 |
| L3 | Adong et al.: ML field calibration of AirQo sensors against a reference | [4] | Crossref title | V (identity). REP's "RMSE 18.6→7.2, >120 devices" omitted → AQ3 | §1, §2 |
| L4 | Lsoto et al.: 11 LCS vs BAM in Kampala, 13 months, hourly and daily | [5] | S2 abstract (Jan 2022–Jan 2023, 11 LCS, BAM, hourly and daily) | V (abstract). "Agree less well at high concentrations / hourly" is from REP; the abstract was truncated → AQ4 | §1, §2 |
| L5 | Wang & Ogawa: meteorological effects on PM2.5 in Nagasaki | [6] | Crossref metadata (abstract available, not read in full) | V (identity) | §2 |
| L6 | Yang et al.: relationships vary by season and region in China | [7] | Crossref title states "Seasonal and Regional Variations" | V (title-level) | §2 |
| L7 | Wabinyai et al.: daily PM2.5, Kampala and Fort Portal, meteorology + lagged pollution | [8] | Crossref/S2 title | V (identity). REP's "57%/80% variance, lag improved significantly" not verified → AQ5 | §2, §6 |
| L8 | Febrian & Permai: daily, 7 days ahead, Central Jakarta, 2023–2024 (731 samples), CNN/LSTM/CNN-LSTM, pollutant-only vs +met; LSTM pollutant-only most consistent; history sufficient, meteorology limited | [9] | **Full text in repo, read** (abstract, §3.1, §3.4, §4, §5) | V | §2, §6 |
| L9 | Niyonzima et al.: one-hour-ahead PM2.5 with RNNs on a large AirQo record | [10] | Crossref title/venue/article no. 1039 | V (identity). REP's "759,480 obs, 68 sites, MAE 8.71, R² 0.68" not verified → AQ6 | §2, §6 |
| L10 | Gürtepe et al.: regional ML prediction; evaluation at withheld stations | [11] | Crossref title ("bridging spatial data gaps") | V (identity). REP's "station-blinded RMSE 9.21 vs 8.28" not verified → AQ7 | §2, §6 |
| L11 | BRITS; LSTM; SMOTE; SMOTE for regression; SHAP; RF; LightGBM; scikit-learn; Evidently | [12]–[21] | arXiv titles (BRITS, SHAP); NeurIPS proceedings page (LightGBM); JMLR page (scikit-learn); Crossref (others) | V (identity) | §2–§3 |
| L12 | Forecasting studies examined use ≥1 year of data | [8]–[11] | Verified for [9] only (2 years) | U → AQ1 | §1, §2 |

## Interpretation, novelty, impact

| ID | Claim | Basis | Status | Notes |
|---|---|---|---|---|
| I1 | Forecast models learn burst/sensor level; month acts as a burst label | SHAP shares (R7) + CV collapse (R3) + August (R16) | Interpretation, supported | Stated as interpretation in §6 |
| I2 | Tree models with history are the most stable across designs | R3, R16 | Supported for RF+H and LGB+H; **not** for LSTM+H in August | Draft 1 qualifies this → AQ16 |
| I3 | Contribution is empirical, not a new method | Methods are all existing (L11) | Supported | §1.1 |
| I4 | Gap: no examined study evaluates a few-day record | Limited to the 11 domain papers examined | Qualified as "among the studies we examined" | §2 |
| I5 | Demonstrated impact limited to working pipeline and free-tier service; no user evaluation | M15–M18; no user-study artefacts found | Supported | §6 |
| I6 | Recommendations for practitioners | Derived from R1, R3, R14, R16 | Interpretation; authors should own this | §6, §7 |
