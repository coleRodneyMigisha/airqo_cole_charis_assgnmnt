# Evidence ledger: Draft 3

Draft 3 keeps every claim from Draft 2. Those claims rest on `research_paper_draft1/evidence_ledger.md`, which still applies, with Draft 2's additions (3,199 rows; Wang and Ogawa; Yang et al.; dashboard time features). This file lists only what is new or changed. Reference numbers are Draft 3's.

Status key: **V** verified in this session; **V-auth** confirmed by an author, but not opened by me; **U** unverified.

| ID | Claim | Evidence | Status | Where |
|---|---|---|---|---|
| L2 | Sserunjogi et al. [3]: 68 monitoring stations, hourly PM2.5 and PM10, 2019–2020 | Europe PMC record for PMID 35990920 (abstract), 15 Nov 2026 | V | §2 |
| L3 | Adong et al. [4]: random forest lowered RMSE from 18.6 to 7.2 µg/m³; rolled out to more than 120 devices | Cole's answer to AQ3 (`ffc65ea`), which points to the Wiley full text; the page returned 403 to me | V-auth | §2 |
| L4 | Lsoto et al. [5]: tracked the BAM at lower concentrations, "dispersed at the higher values"; stronger linear relationship in 24-hour data | Europe PMC abstract, 15 Nov 2026 | V | §1, §2 |
| L7 | Wabinyai et al. [9] found lagged PM2.5 useful | Full text (`sources/1-s2.0-S2590162125001017-main (1).pdf`), 16 Nov 2026: abstract says one-day lagged PM2.5 "significantly improved model accuracy"; lag coefficients positive in all seasons in both cities (Kampala 0.009–0.018); R² 0.575 Kampala, 0.802 Fort Portal | V | §6 |
| L9 | Niyonzima et al. [10]: large AirQo record; MAE of the same order | Full text (`sources/s44163-026-01623-3 (1).pdf`), 16 Nov 2026: attention LSTM, 759,480 hourly observations from 68 AirQo sites, one-hour-ahead with a 72-hour window, MAE 8.7063, R² 0.6820 on 90,638 test predictions at 53 sites; our best hold-out MAE is 8.43 | V | §2, §6 |
| D13 | Data from the AirQo network, provided through a university course | Authors' answer, 15 Nov 2026 | V-auth | §3.1 |
| R3 | Table 3 values | `deployment_outputs/model_validation_comparison.csv`; `train.ipynb` cell 537, re-read 15 Nov 2026 | V | Table 3 |
| A1 | AI assisted with parts of the analysis code | Notebook outputs ran from a Claude Code scratchpad (Draft 1 AQ15); `Co-Authored-By: Claude` trailers on `1c5625e` and `3fdcd6a` (branches `backup-pre-trailer-*`) | V (that it happened); extent U (AQ15) | Declaration |
| H1 | Findings and major decisions are the authors' own | Authorship of the commits that carry each decision (`work_up_to_now.md`, Section 3) | V | Declaration |

## Review round (Mr. Stephen's comments, 17 Nov 2026)

Reference numbers below are those of the renumbered `manuscript_source.txt`. Rerun outputs are in `research_paper_draft3/reruns/results/`.

| ID | Claim | Evidence | Status | Where |
|---|---|---|---|---|
| N1 | Kampala: 7,257 deaths 2018-2021, 17.9-19.8% per year, annual mean 39 µg/m³ [2] | `sources/Atuyambe2024_Kampala_mortality.pdf`, abstract: "there were 7257 air pollution-related deaths in Kampala city" | V | §1 |
| N2 | SDG indicators 3.9.1 and 11.6.2 [3], [4] | `sources/SDG_3.9.1_metadata.pdf`, `sources/SDG_11.6.2_metadata.pdf` | V | §1 |
| N3 | Le et al. [10]: 27 monitors; RMSE 20.37 to 3.83 µg/m³ | `sources/Calibration of low-cost sensor data ...pdf`, abstract | V | §2 |
| N4 | Gahungu [15], Stoddart [16], Pandey [17], Gupta [18] as described | arXiv PDFs in `sources/`; Gupta "19.34% improvement over the baselines"; Pandey "511 locations ... one year"; Stoddart "We demonstrate the advantage of removing outliers" | V | §2, §3.2 |
| N5 | Alaran et al. [28]: meteorology explains about 18% (Kampala) and 7% (Jinja); predictors precipitation, humidity, temperature, wind (no PM10) | `sources/Alaran2024_PM25_meteorology_Kampala_Jinja.pdf`: "meteorological factors could explain about 18% of the variation of PM2.5 in Kampala and 7% in Jinja" | V | §3.2, §6 |
| N6 | Niyonzima et al. [14]: MAE 8.71, R² 0.68, 759,480 hourly observations, 68 sites, one hour ahead | `sources/s44163-026-01623-3 (1).pdf`: "RMSE = 14.5667, MAE = 8.7063, and R² = 0.6820" | V | §6 |
| N7 | AirQo data CC BY 4.0; credit AirQo and originating provider; data indicative [26], [27] | `sources/AirQo_AirQoDataPage_source_2026-11-17.tsx`, `sources/AirQo_TOSPage_source_2026-11-17.tsx` (live site down; GitHub source, commit f9fdbc4) | V | §3.1 |
| N8 | Render free tier: 512 MB, spins down after 15 min, about one minute to spin up; USD 7/month smallest paid; Vercel Hobby free [34]-[36] | `sources/Render_free_tier_docs_2026-11-17.txt`, `sources/Render_pricing_page_2026-11-17.txt`; Vercel docs page read 17 Nov 2026 | V | §4.3 |
| N9 | Persistence MAE 8.58 (hold-out), 15.17 (August); history models 8.43-8.50 and 13.70-14.02 | `results/full_comparison_long.csv`, `results/persistence_by_fold.csv` | V | §5.1, §5.3, abstract |
| N10 | 95% CIs and differences (e.g. LightGBM+history minus persistence -0.15 [-0.53, 0.24]; RF+history minus persistence in August -1.47 [-1.76, -1.16]) | `results/ci_holdout*.csv`, `results/ci_august*.csv` (1,000 sensor-cluster draws) | V | §5.1, §5.3 |
| N11 | Removing the month: SVR August 18.32 to 20.51, hold-out 9.34 to 11.23; history models within about 1% | `results/no_month_summary.csv` | V | §5.3 |
| N12 | PM2.5 > PM10: 3,199 of 14,170 rows (22.6%), median excess 4.2 µg/m³; retrained without them SVR 10.51, RF+history 9.25, August 18.22 and 13.84 | `results/review_summary.json`, `results/pm25_above_pm10_check.csv` | V | §3.1, §3.2, §5.5 |
| N13 | Extremes: 52% in hours with 3+ other extreme sensors; August rule replaced 661 readings at 96 sensors; RF+history 13.70 to 12.96, persistence 15.17 to 14.20 | `results/review_summary.json`, `results/august_outlier_rule.csv` | V | §3.2, §5.3 |
| N14 | August per-group MAE (SVR 18.7/18.1/14.3; LightGBM+history 14.0/14.4/12.5); all 125 sensors seen | `results/august_per_group.csv` | V | §5.3 |
| N15 | Downstream BRITS effect +1.1%, 3 of 15 (rerun) against -0.4%, 7 of 15 (first run) | `results/downstream_by_model_design_imputer.csv`; first run: Draft 3 text and committed notebook outputs | V | §5.2 |
| N16 | Rerun reproduced all hold-out MAEs within 0.01 except KNN (k 5 against 10, CV 0.594 against 0.595) | `results/reproduction_report.csv`; committed notebook cell 265 output; `results/hyperparameters.json` | V | §4.1 |
| N17 | Hosted service: cold start 41.9 s; medians 0.56/0.70/2.51 s; 2,642 of 2,642 rows within 0.0005 µg/m³; model 1.17 MB | `reruns/deployment/hosted_latency.json`, `reruns/deployment/cold_start_time.txt`; `results/review_summary.json` | V | §5.4 |
| N18 | Settings in Table 3 and the LSTM/BRITS text | `results/hyperparameters.json`; `train.ipynb` `build_lstm` | V | §3.3 |
| N19 | Tukey's far-out limit [29] | Standard reference (Tukey, 1977); not opened in this session | U (book) | §3.2 |
| N20 | AirQo devices reported in about 72% of expected hours, April-June 2025; AirQo pipeline on Kubernetes/GCP with Airflow and Kafka (Sserunjogi et al. 2025) | Read the arXiv preprint `sources/Design_and_Evaluation_of_a_Scalable_Data_Pipeline_for AI-Driven_Air_quality_Monitoring_in_Low-Resource_Settings.pdf` (2508.14451v1): "AirQo devices consistently maintained high availability, averaging above 70%, with a slight decline from 72.81% in April to 72.08% in June"; section 3.3 for the stack. Cited as the published CCIS version (Crossref: doi:10.1007/978-3-032-08649-5_14, pp. 212-231); published text not opened | V (preprint) | §1, §4.3 |
