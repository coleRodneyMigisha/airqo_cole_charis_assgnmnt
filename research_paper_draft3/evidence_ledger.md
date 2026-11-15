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
