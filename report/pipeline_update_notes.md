# AirQo PM2.5 pipeline: change notes

The full write-up is now in `report/main.tex`. These notes list what changed in each round and the headline numbers of the current run, so the report can be checked against them. All numbers come from the run stored in `train.ipynb` (local machine, Python 3.13, about 56 minutes, 346 code cells, 0 errors, 70 figures). Figures are in `report/figures/`.

## Current headline results

| Model | Hold-out MAE | Hold-out R² | Expanding-window CV MAE | Leave-sensors-out MAE |
|---|---:|---:|---:|---:|
| LightGBM + PM2.5 history (best nowcast) | 8.43 | 0.42 | 12.08 | 9.49 |
| Random Forest + PM2.5 history | 8.50 | 0.41 | 10.25 | 9.03 |
| SVR, tuned (selected forecast model) | 9.34 | 0.34 | 14.68 | 15.09 |
| Random Forest (untuned / tuned) | 9.61 / 9.63 | 0.25 / 0.24 | 27.02 / 26.82 | 14.90 / 14.92 |
| LightGBM | 9.82 | 0.25 | 27.45 | 15.13 |
| KNN | 10.01 | 0.26 | 16.69 | 15.60 |
| LSTM with PM2.5 history | 10.89 | 0.30 | 12.18 | 9.41 |
| LSTM (weather and time) | 12.22 | 0.01 | 20.70 | 15.61 |
| Baseline (training mean) | 17.60 | −0.30 | 24.11 | 20.33 |
| Ridge / Linear / Polynomial | 22.0 / 23.9 / 23.9 | below 0 | 23.9 / 24.7 / 24.7 | 16.4 / 16.4 / 16.7 |

MAE and RMSE are in µg/m³. The full table is in `deployment_outputs/model_validation_comparison.csv`.

## Round 3 (this update)

1. **SMOTE removed from the final models, kept as an experiment.** `USE_SMOTE = False`. The SMOTE section still runs the cross-validation over strengths, the synthetic-row check and a with/without table. All eight models were worse with SMOTE on the hold-out at both strengths (for example LightGBM 9.8 → 28.7 at 0.25; SVR 9.3 → 30.2; Random Forest 9.6 → 10.1). A markdown cell under the table explains the effect and the decision.
2. **PM2.5 history features for the tree models.** Readings 1, 2 and 3 hours earlier, their mean and their count. Random Forest 9.61 → 8.50 (−11.6 %), LightGBM 9.82 → 8.43 (−14.2 %); in the expanding-window CV about 27 → 10.3 and 12.1. These are nowcast models; the best is saved as `best_pm25_nowcast_model.joblib`. In SHAP, 50 % of its attribution is on the history features.
3. **Extreme PM2.5 values replaced by the nearest normal reading.** Rule: above the sensor's Q3 + 3 × IQR. 225 of 14,275 readings (1.5 %) at 59 sensors; 223 replaced by a normal reading of the same sensor at most 5 hours away (median 1 hour), 2 by the sensor median. Maximum 998 → 415 µg/m³. Original values are kept in `pm2_5_original`. Scored against the original readings the hold-out MAEs are 9.79 (LightGBM + history) and 10.62 (SVR).
4. **PM10 stays out.** PM2.5 is the fine fraction of PM10, so PM10 is a same-hour co-measurement of the same particles rather than a driver of PM2.5; the literature points to meteorological drivers (temperature, humidity). PM10 is also not known ahead of time.
5. **EDA sites with data.** A Kampala site must have readings in every month that contains data. The five sites are Nakasero II, Lower Nsooba, Salama Road, Namungona Primary School and Kabusu; the EDA time-series figures now use these five plus the network mean, so no panel is empty.
6. **Effect of the bidirectional LSTM (BRITS-style) imputation.** The imputer now uses LSTM cells. A new section answers three questions:
   - As an imputer it is better than the time-of-day method in all 15 variable-and-gap combinations, by 21 % on average.
   - It fills every real gap (interpolation fills only 5–12 %), but its fills are smoother than real readings (PM2.5 standard deviation 11.9 against 26.8 observed).
   - For training it brings no reliable gain: prediction MAE changed by −0.4 % on average and improved in 7 of 15 cases.
7. **Report** (`report/main.tex`) rewritten for the current pipeline, with the UCU logo on the title page (`report/figures/ucu_logo.png`).

## Round 4: training-effect figures and the imputation decision

- Two figures added to the notebook (cells `effect-01` to `effect-03`, after the "Does the bidirectional LSTM imputation add value?" checks) and to the report: `brits_training_effect_mae.png` (MAE by imputation method, model and validation setup) and `brits_training_effect_change.png` (% change in MAE, bidirectional imputer against time-of-day).
- Decision cell (`decision-01`) and report subsection "Decision: which imputed data the final models are trained on": the final models use windowed interpolation plus time-of-day imputation and are not retrained on the bidirectional imputer's values.
- The two figure cells were run on the downstream table stored in the notebook, not as part of a full top-to-bottom run, so they have no execution number until the notebook is next run in full.
- Slides: `report/slides/bilstm_imputation_effect_slides.pptx` (three slides on the UCU template).

## Second dataset (full August file)

The external test now uses `AirQo_August_2026_hourly_matched.csv`: 73,274 rows, 125 sensors (all in the main dataset, all in Uganda), 1-31 August 2026. No retraining.

- Forecast models: SVR 18.3, KNN 18.6, LightGBM 18.8, Random Forest 19.0 MAE; baseline (training mean) 19.2. All R² below zero.
- Models with PM2.5 history: Random Forest 13.7 (R² 0.30), LightGBM 14.0 (R² 0.27).
- Calendar: forecast model predicts Moderate on all 31 days; actual is Unhealthy for Sensitive Groups on 16; 15 days match (17 with the history model).
- Sensor classes in August: 76 data-rich, 31 intermediate, 18 data-poor.
- Evidently: 6 of 9 features drifted (month 0.83, day of week 0.75 and 0.61, humidity 0.26, sensors 0.25).
- Imputation (fitted imputers, MAE): bidirectional model temperature 1.3 °C at 6 h, 1.8 at 24 h, 2.0 at 72 h; PM2.5 13.9 to 16.7 µg/m³ from 6 to 72 h (time-of-day 15.7 to 18.4).

## Round 5: full project story, literature and documentation

- **Report.** New subsection "Project evolution and key decisions" (Phase 1 with PM10 and why it was abandoned; rejected ideas with evidence; Phase 2; the BiLSTM decision) with a decision-log table. The Data section gained a missing/zero table, gap counts, the 28.8 % weather-dropout share, sensor data-quality flags and AQI counts before and after the extreme-value replacement. The EDA correlation discussion now gives the per-site ranges and the temperature/humidity mechanisms (Wang & Ogawa 2015; Yang et al. 2017). Results cite Febrian & Permai (history is enough) and Gürtepe et al. 2025 (station-blinded validation). Monitoring adds the Phase 1 Evidently result. Deployment is now a chronology: RunPod (dropped, cost) → Kaggle → Hugging Face (static, 402 for server Spaces) → Render + Vercel. Limitations and future work extended (short test window, calibration, untested models for the BiLSTM decision, GCP/Azure, ONNX). "The group" and "a team member" replaced.
- **Checked against the notebook and git history.** Phase 1 numbers come from the pre-feedback notebook (commit `245c2e2`): tuned Random Forest MAE 3.103, RMSE 7.003, R² 0.898, AQI accuracy 86.2 %, untuned Random Forest MAE 3.272, PM10 importance 76 %, Evidently 6 of 7 columns. KNN long-gap filling: 96.0–97.7 % imputed, 11.1–12.5 % distinct values (commit `32edd3e`).
- **Not used because no run output supports them:** the feature-set sensitivity table (MAE 11.20 / 11.12 / 13.56, 3.54 without weather) and an untuned Random Forest MAE of 3.221.
- **Docs.** `DEPLOYMENT.md` rewritten around the current SVR and the deployment chronology. `HUGGINGFACE.md`, `huggingface/model/README.md`, `huggingface/space/README.md` and the footer of `huggingface/space/index.html` now describe the SVR; `huggingface/prepare.py` was re-run, so `forecasts.json` and the local model copy are the current ones. The online Hugging Face repos are unchanged until they are uploaded again.
- **One-page abstract** in `report/abstract/abstract.tex` / `abstract.pdf`.

## Still to do by hand

- Add the Render and Vercel links where the report shows the red `[ADD LINK: ...]` markers, and in `DEPLOYMENT.md`.
- Complete the Wang et al. 2019 reference (title, authors, DOI); it is marked in red in the bibliography.
- Re-upload the Hugging Face model and Space (HUGGINGFACE.md steps 3 and 4) if the online versions should show the current model.

## Earlier rounds, in brief

- **Round 1:** PM10 removed; empty-sensor check (none dropped); offline-time table and classes (61 data-rich, 40 intermediate, 48 data-poor); windowed interpolation; time-of-day imputation with masked validation; SMOTE added on the training split; LightGBM and LSTM added; three validation setups.
- **Round 2:** methodology diagram recoloured; calendars in PM2.5 category colours; one density panel per variable; one combined time-series figure per site; cross-pair lagged correlations; AUC removed; BRITS-style imputer; masked-gap test; downstream comparison; SHAP; sensor maps; second-dataset test.

## References used

- Cao, W., Wang, D., Li, J., Zhou, H., Li, L., & Li, Y. (2018). BRITS: Bidirectional Recurrent Imputation for Time Series. *NeurIPS 31*, pp. 6776–6786. arXiv:1805.10572.
- Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 30*, pp. 4765–4774.
- Lundberg, S. M., et al. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2, 56–67.
- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. *JAIR*, 16, 321–357.
- Torgo, L., Ribeiro, R. P., Pfahringer, B., & Branco, P. (2013). SMOTE for Regression. *EPIA 2013*, LNCS 8154, pp. 378–389.
- Saminathan, S., & Malathy, C. (2023). Ensemble-based classification approach for PM2.5 concentration forecasting using meteorological data. *Frontiers in Big Data*, 6, 1175259.
- Febrian, S., & Permai, S. D. (2025). PM2.5 Index Prediction in Central Jakarta Using Pollution and Meteorological Data with CNN-LSTM. *E3S Web of Conferences*, 680, 00067.
- Gürtepe, I. C., Senkal, I. T., Ünal, A., Güllü, G., Aslanoğlu, S. Y., & Marshall, J. D. (2025). Machine learning driven regional prediction of PM2.5 concentrations in the Eastern Mediterranean: bridging spatial data gaps in air quality monitoring. *Environmental Modelling & Software*, 192, 106586. doi:10.1016/j.envsoft.2025.106586
- Wang, J., & Ogawa, S. (2015). Effects of Meteorological Conditions on PM2.5 Concentrations in Nagasaki, Japan. *IJERPH*, 12(8), 9089–9101. doi:10.3390/ijerph120809089
- Yang, Q., Yuan, Q., Li, T., Shen, H., & Zhang, L. (2017). The Relationships between PM2.5 and Meteorological Factors in China: Seasonal and Regional Variations. *IJERPH*, 14(12), 1510. doi:10.3390/ijerph14121510
- Wang et al. (2019). *Environment International*, 124, 371–379. Title, authors and DOI still to be completed.

## Round 6: reason for removing PM10

The stated reason is now scientific first: PM2.5 is the fine fraction of PM10, so PM10 is a co-measurement of the same particles rather than a driver, and the literature (Wang & Ogawa 2015; Yang et al. 2017) points to meteorological conditions as drivers. Not being known ahead of time is the second reason. Updated in `main.tex` (abstract, change list, Phase 1, decision log, cleaning, limitations), `abstract.tex`, `DEPLOYMENT.md`, the Hugging Face model card and the notebook markdown cells `pm10-01` and the model summary.
