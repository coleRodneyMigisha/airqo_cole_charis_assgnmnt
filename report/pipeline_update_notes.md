# AirQo PM2.5 pipeline: notes for the report

These notes document the changes made to `train.ipynb` in October 2026 so they can be written up in the report. Sections 1 to 9 cover the first round of changes; sections 10 to 17 cover the follow-up (revised plots, BRITS-style imputation, SHAP, sensor maps and the second dataset). Every number comes from the run stored in the notebook (local machine, Python 3.13, about 45 minutes, 0 errors). All figures named below are in `report/figures/`.

`main.tex` has not been edited. It still describes the earlier pipeline (PM10 as a predictor, MAE 3.10, R² 0.90), so its methods, results and figures need updating from these notes.

## 1. What changed, in one paragraph

PM10 was removed from the whole pipeline. Sensors are now profiled by offline time and classed as data-rich or data-poor. Gaps are filled in two steps: windowed linear interpolation for short gaps, then time-of-day imputation for the rest. SMOTE was added and is applied to training rows only. LightGBM and two LSTM variants were added, and every model is scored under three validation setups. The main consequence is that accuracy fell sharply: the best hold-out MAE is now about 11.8 µg/m³ (it was 3.1), because PM10 had been carrying most of the predictive power.

## 2. Methodology pipeline

Figure: `methodology_pipeline.png`.

Raw data → cleaning (drop PM10, drop empty sensors, zeros to missing) → offline-time analysis → windowed interpolation → time-of-day imputation → feature engineering → split (three validation setups) → SMOTE (training rows only) → models (six existing, LightGBM, LSTM) → evaluation → deployment and monitoring.

Leakage rule used throughout: anything that is fitted (hourly weather profiles, target Z-score, feature scalers, SMOTE, early stopping) uses the training rows of the split only.

## 3. Data preparation

### 3.1 The data

- 14,600 hourly rows from 149 sensors.
- Readings exist on only 8 of the 212 days in the study period (1 January to 31 July 2026), in three bursts: 1–3 January, 1–2 April and 1–3 June. That is 147 hours in which at least one sensor reported.

### 3.2 PM10 removed

The PM10 column is dropped straight after loading. The three EDA cells that compared PM2.5 with PM10 were deleted. PM10 no longer appears in any plot, feature list, model or forecast.

### 3.3 Sensors with no data

No sensor is completely empty and none lacks PM2.5, so **0 sensors were dropped**. Nine sensors report PM2.5 but never report temperature or humidity (`aq_46`, `aq_59`, `aq_70`, `aq_79`, `aq_93`, `aq_g4_99`, `aq_g505`, `aq_g518`, `aq_g5_127`). They were kept, because they have valid targets; their weather inputs are entirely imputed. Set `DROP_SENSORS_WITHOUT_WEATHER = True` to remove them.

### 3.4 Offline time

Figure: `sensor_offline_time.png`.

A sensor is offline in an hour when it has no valid PM2.5 reading for it.

| Expected timestamps | Offline percentage |
|---|---|
| Every hour of the study period (5,088 hours) | 97.1 % to 99.6 % for every sensor |
| Network-active hours only (147 hours) | 0 % to 86.4 % |

The study-period figure cannot separate sensors, so the network-active figure is used for classification:

| Class | Rule (offline % of network-active hours) | Sensors | Mean offline % |
|---|---|---:|---:|
| Data-rich | at most 20 % | 61 | 8.6 |
| Intermediate | between 20 % and 50 % | 40 | 34.7 |
| Data-poor | at least 50 % | 48 | 68.3 |

### 3.5 Windowed interpolation

A missing hour is filled by linear interpolation only if the gap is at most 3 hours long, has valid readings on both sides, and the 24-hour window centred on it holds at least 6 real readings. It runs per sensor. Parameters: `INTERPOLATION_WINDOW_HOURS = 24`, `MAX_INTERPOLATION_GAP_HOURS = 3`, `MIN_VALID_IN_WINDOW = 6`.

It filled 555 temperature values, 551 humidity values and 790 PM2.5 values. Longer gaps stay missing. PM2.5 is filled into a separate descriptive column (`pm2_5_cleaned`); the model target is never filled.

### 3.6 Time-of-day imputation

Figures: `diurnal_profiles.png`, `imputation_before_after_density.png`.

1. The mean and variance of each variable are computed per hour of day for each sensor, with a fallback to the sensor's network group (AirQo or AirGradient) and then to all sensors when a sensor has fewer than 3 readings for an hour.
2. The sensor's own readings within 12 hours either side of the gap give a local offset from that profile.
3. Missing value = profile value for the hour + local offset.

Only the 147 network-active hours are filled; the months between bursts stay missing. PM2.5 is handled on a log scale and only filled when a local offset exists.

The daily cycle it captures: temperature runs from about 19.6 °C at night to 28.6 °C around midday (UTC), humidity from about 92 % to 65 %, and PM2.5 peaks in the early morning (about 46 µg/m³ at 04:00–05:00 UTC) and evening (about 41 µg/m³ at 18:00–20:00 UTC).

Validation by masking 10 % of known values (mean absolute error):

| Variable | Gap | Time-of-day + offset | Hourly profile only | Sensor mean | Windowed interpolation |
|---|---|---:|---:|---:|---:|
| Temperature (°C) | 1 h | 1.40 | 1.72 | 3.01 | 0.61 |
| Temperature (°C) | 6 h | 1.53 | 1.66 | 3.14 | cannot fill |
| Humidity (%) | 1 h | 5.33 | 6.74 | 10.20 | 2.06 |
| Humidity (%) | 6 h | 6.16 | 6.43 | 10.82 | cannot fill |
| PM2.5 (µg/m³) | 1 h | 12.43 | 19.31 | 18.45 | 8.39 |
| PM2.5 (µg/m³) | 6 h | 13.38 | 19.80 | 18.92 | cannot fill |

Interpolation is best for single hours, so it runs first; the time-of-day method handles what is left and beats both simpler alternatives.

Limits to state: the PM2.5 imputation error is large relative to a mean of about 33 µg/m³, and about 7,000 values per weather variable were filled from the profile alone (no reading from that sensor within 12 hours), which understates the real spread.

### 3.7 Calendars before and after cleaning

Figures: `calendar_pm25_before_cleaning.png`, `calendar_pm25_after_cleaning.png` (before and after stacked) and `eda_calendar_before_after_cleaning.png` for the five Kampala sites. The calendars are now coloured by PM2.5 category (section 10); the separate coverage calendars were removed and the coverage figures are in the notebook's before/after table.

Cleaning fills hours inside the observed days; it does not create new days. On the six full observation days, coverage rises from about 58–70 % of sensor-hours to about 75–86 %, and the daily network mean changes by at most about 1 µg/m³.

## 4. Exploratory analysis

- **Density plots.** All histograms were replaced by kernel-density curves, one panel per variable (`eda_density_raw.png`, `eda_density_by_sensor_group.png`, `eda_zscore_density.png`). PM2.5 uses a log axis because it is right-skewed (mean 32.7, median 20.8 µg/m³).
- **Time series.** One combined figure per site with temperature, humidity and PM2.5 on a shared time axis and three colour-matched y-axes (`eda_timeseries_network_mean.png` and `eda_timeseries_<sensor>.png` for the data-rich and the three data-poor case-study sensors).
- **Correlations.** `eda_correlation_pearson_spearman.png`, `eda_lagged_cross_correlation.png`.

| Pair | Pearson | Spearman |
|---|---:|---:|
| PM2.5 and temperature | −0.12 | −0.16 |
| PM2.5 and humidity | +0.06 | +0.10 |
| Temperature and humidity | −0.81 | −0.81 |

Lagged cross-correlations (within sensor, up to 24 hours each way; `eda_lagged_cross_correlation.png`): temperature vs humidity peaks at lag 0 (r = −0.88); temperature vs PM2.5 is −0.23 at lag 0 and −0.24 at +1 hour (largest value −0.28 at +24 hours, the daily cycle repeating); humidity vs PM2.5 is +0.16 at lag 0 and −0.29 at +9 hours. Positive lag means the first variable comes first. Same-hour and one-hour-earlier weather are the lags worth using; longer lags only repeat the daily cycle that hour-of-day features already carry. Weather is a weak predictor of PM2.5, and these are correlations, not causes.

## 5. SMOTE

Figure: `smote_target_density.png`.

**Before this change the notebook did not use SMOTE.** It is now applied to training rows only. PM2.5 is continuous, so rows are grouped into PM2.5 classes (the assignment AQI bands, two rarest merged), `SMOTENC` oversamples the rare classes, and the target is interpolated together with the features, following the regression use of SMOTE. Hyperparameters are tuned on real rows only; validation and test rows are never resampled.

The SMOTE strength (the share of the largest class that rare classes are raised to) was chosen by time-series cross-validation inside the training rows from 0, 0.1, 0.25 and 0.5. It chose 0.1, which adds 530 synthetic rows.

**Result: SMOTE made every model worse on the hold-out.**

| Model | Hold-out MAE without SMOTE | With SMOTE at 0.5 | Final model (SMOTE at 0.1) |
|---|---:|---:|---:|
| Random Forest (untuned) | 11.45 | 12.38 | 11.78 |
| Random Forest (tuned) | 11.47 | 12.44 | 11.83 |
| KNN | 11.64 | 13.16 | 12.06 |
| LightGBM | 11.74 | 29.97 | 21.88 |
| SVR | 10.98 | 54.75 | 22.24 |
| Ridge | 24.52 | 42.29 | 31.98 |
| Linear / Polynomial | 26.50 | 36.95 | 32.39 |

Why: oversampling rare high-pollution hours raises the average target. Without PM10 the features cannot tell a model where those hours belong, so it raises its predictions everywhere, and the hold-out days were cleaner than the training period (mean 24.8 against 34.5 µg/m³). The synthetic rows were checked and are valid.

The final models keep the cross-validated choice because the test set should not steer modelling decisions. Setting `SMOTE_RATIO_OVERRIDE = 0` trains without SMOTE.

References:

- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. *Journal of Artificial Intelligence Research*, 16, 321–357. https://doi.org/10.1613/jair.953
- Torgo, L., Ribeiro, R. P., Pfahringer, B., & Branco, P. (2013). SMOTE for Regression. In *Progress in Artificial Intelligence (EPIA 2013)*, LNCS 8154, pp. 378–389. Springer.
- Saminathan, S., & Malathy, C. (2023). Ensemble-based classification approach for PM2.5 concentration forecasting using meteorological data. *Frontiers in Big Data*, 6, 1175259. https://doi.org/10.3389/fdata.2023.1175259

The 2023 paper uses SMOTE for PM2.5 *classification*. The second and third references were checked online (repository listing and publisher page); the Chawla et al. details are the standard citation and were not re-checked against the journal site.

## 6. Models and validation

Features: temperature, humidity, cyclical hour / day-of-week / month, and the sensor name (one-hot).

Models: Ridge, Linear, Polynomial, Random Forest, SVR, KNN (existing), LightGBM (new), and two LSTMs (new).

- **LSTM (weather + time):** sequences of the previous 6 hours of weather and time features. Same information as the tabular models, minus sensor identity.
- **LSTM (weather + time + PM2.5 history):** also sees the PM2.5 reading of the previous hour at each step. This is a one-step-ahead model; it needs recent readings from the sensor and cannot make the August forecast.

LSTM settings: window 6 hours, 32 units, dropout 0.2, Adam, early stopping with patience 8 on the latest 15 % of the training rows, seed 42. Loss curves: `lstm_loss_curves.png`.

Three validation setups (the notebook previously had only the first):

1. **Chronological hold-out (main):** train 1 January–1 June (11,633 rows), test 2–3 June (2,642 rows).
2. **Expanding-window time-series CV:** validate on 1 April, 2 April and 1 June, training on everything earlier each time.
3. **Leave-sensors-out:** three folds, each holding out about 50 sensors entirely.

### Results (mean over folds, µg/m³)

| Model | Hold-out MAE | Hold-out RMSE | Hold-out R² | Expanding CV MAE | Leave-sensors-out MAE | Leave-sensors-out R² |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest (untuned) — selected | 11.78 | 25.21 | −0.32 | 30.57 | 15.73 | 0.19 |
| Random Forest (tuned) | 11.83 | 25.31 | −0.33 | 30.68 | 15.74 | 0.19 |
| KNN | 12.06 | 21.42 | 0.04 | 18.16 | 17.57 | 0.01 |
| LSTM (+ PM2.5 history) | 12.61 | 19.23 | 0.23 | 13.81 | 10.85 | 0.53 |
| LSTM (weather + time) | 13.42 | 21.97 | −0.01 | 23.82 | 16.39 | 0.23 |
| Baseline (training mean) | 19.20 | 23.94 | −0.19 | 25.42 | 21.41 | −0.02 |
| LightGBM | 21.88 | 31.38 | −1.05 | 23.41 | 16.19 | 0.22 |
| SVR | 22.24 | 26.38 | −0.45 | 18.48 | 18.22 | 0.15 |
| Ridge | 31.98 | 36.48 | −1.77 | 26.43 | 18.76 | 0.12 |
| Linear | 32.39 | 38.82 | −2.14 | 26.86 | 17.19 | 0.16 |
| Polynomial | 32.39 | 38.82 | −2.14 | 26.79 | 18.96 | 0.10 |

The full table is saved as `deployment_outputs/model_validation_comparison.csv`.

**Which model is best.** The Random Forest has the lowest hold-out MAE and is the model saved for deployment, but its lead is narrow and not robust: its hold-out R² is negative, its RMSE is above the training-mean baseline, and both Random Forests are the worst models in the expanding-window CV. The LSTM with PM2.5 history is the most consistent model (best in two of three setups, only clearly positive hold-out R²) because it sees recent PM2.5, but it needs live readings so it cannot serve the forecast.

## 7. Evaluation extras

AUC is not a regression metric, so the area-under-the-curve comparison and the ROC AUC were removed from the notebook. Models are judged on RMSE, MAE and R² only.

- **AQI category accuracy** of the selected model: 71.9 %, no better than always predicting the training mean (72.9 %).
- **Predicted versus actual:** `eval_predicted_vs_actual_timeseries.png`, `eval_predicted_vs_actual_scatter.png`, `eval_residuals.png` (mean residual −2.1 µg/m³ for the Random Forest, +4.1 for the LSTM with history).
- **Actual and predicted calendars** in PM2.5 category colours (`eval_calendar_actual_vs_predicted.png`, `eval_calendar_actual_vs_predicted_rich_sensor.png`) and the daily absolute error on a separate scale (`eval_calendar_absolute_error.png`). On the five out-of-sample days the predicted category matches on the two hold-out days (2–3 June) and is one or two categories too high on the three cross-validation days; only 36 % of sensor-hours fall in the right category.

### Data-rich versus data-poor sensors

Figure: `eval_data_rich_vs_poor.png`.

Pooled over all hold-out rows (selected Random Forest):

| Sensor class | Sensors | MAE (µg/m³) | MAE as % of mean | RMSE |
|---|---:|---:|---:|---:|
| Data-rich | 61 | 10.1 | 42 % | 17.8 |
| Intermediate | 35 | 12.8 | 49 % | 22.2 |
| Data-poor | 23 | 17.8 | 65 % | 49.2 |

Error grows as a sensor's data gets sparser. The four-sensor case study (one data-rich, three data-poor) does not show this on its own: the data-rich example `airqo_g5282` has the largest error (MAE 19.8) because its hold-out contains two spikes above 150 µg/m³, while the three data-poor examples have MAE near 10.5 on calmer series. Single sensors are an illustration; the pooled table is the evidence.

## 8. Deployment

- `best_pm25_model.joblib` was overwritten because the saved model required PM10 and could no longer be fed. The notebook now only overwrites it when the saved model is unusable or the new one has a lower hold-out MAE.
- `pm25_inference.py` reads its feature list from the saved model, so its logic is unchanged; its header now lists the PM10-free features. `serve_model.py`'s description was updated the same way.
- August forecasts, Evidently reports and the run logs in `deployment_outputs/` were regenerated. Evidently flags 8 of 9 feature columns as drifted between the training and test periods.
- New packages in `requirements.txt`: `lightgbm`, `imbalanced-learn`, `tensorflow`.

## 9. Limitations to state in the report

- Only 8 days of data in three bursts. All validation results rest on very few distinct days, and the three setups disagree on the ranking of models.
- Without PM10, weather, time and sensor identity explain little of hourly PM2.5.
- The hold-out period was cleaner than the training period, which penalises any method that raises predictions, including SMOTE.
- Hyperparameters were tuned once on the chronological training set and reused in the other two validation setups.
- The LSTM with PM2.5 history is a one-step-ahead model and is not comparable to the others as a forecaster.
- LSTM training on CPU is seeded, but small run-to-run differences are possible.

---

# Follow-up changes

## 10. Revisions to the existing plots (Part 0)

- **Methodology diagram** (`methodology_pipeline.png`): 15 stages in five colour groups (data preparation, EDA, modelling, evaluation and explainability, deployment and monitoring). Each box also carries its group name and a group-specific border, so it reads in grayscale. BRITS-style imputation, SHAP, sensor maps and the second dataset test were added.
- **Calendars:** every calendar is coloured by PM2.5 category using the notebook's own definition (the assignment's AQI bands): Good 0–9, Moderate 9.01–35.49, Unhealthy for Sensitive Groups 35.5–55.49, Unhealthy 55.5–125.49, Very Unhealthy 125.5–225.49, Hazardous above 225.49 µg/m³, with the notebook's colours. Missing days are grey; the legend lists the ranges; no continuous colourbar.
- **Density plots:** one KDE panel per variable (temperature, humidity, PM2.5) with mean and median lines, applied to: raw observed readings; readings by sensor group (data-rich, intermediate, data-poor); before versus after gap filling; main versus second dataset.
- **Time series:** one combined figure per site (see section 4).
- **Lagged cross-correlation:** the PM2.5 autocorrelation was removed; three cross-pairs remain with the peak lag marked (see section 4).
- **AUC removed** everywhere (see section 7).
- **Calendar in the evaluation section:** actual and predicted side by side (see section 7).

## 11. BRITS-style bidirectional imputation

Figure: `brits_loss_curves.png`.

Idea (from Cole): a recurrent model reads each sensor series forwards and backwards, each direction estimates a value before seeing it, and a consistency loss makes the two directions agree. It is supervised learning with an added consistency loss.

It follows BRITS (Cao et al., 2018): one recurrent network per direction with a hidden state that decays with the time since the last reading; a history-based estimate, a feature-based estimate from the other variables and a learned blend; a loss on observed values only; and the forward/backward consistency loss. Differences from the paper: three variables (temperature, humidity, PM2.5 on a log scale) from sensors that report in three short bursts; hour of day (sine and cosine) and the sensor's offline share added as conditioning inputs; blocks of 1 to 12 hours hidden during training; no classification head.

Route used: written in TensorFlow, not PyPOTS. PyPOTS would add PyTorch as a second framework and does not report the consistency term separately or take conditioning inputs.

Settings: 24-hour sliding windows (stride 2), 32 GRU units per direction, consistency weight 0.1, Adam, up to 60 epochs with early stopping (patience 6) on the error of hidden values for 15 % of the training sensors, seed 42. Scalers and the model are fitted on the training period only; each split is imputed separately. On the chronological training split: 2,712 training windows, 496 early-stopping windows, best epoch 57 of 60.

## 12. Masked-gap imputation test

Figures: `imputation_error_vs_gap_length.png`, `imputation_examples_pm25.png`, `imputation_examples_temperature.png`.

Real readings in the hold-out period (2–3 June, 28 hours) were hidden, one gap per sensor at a random position with all three variables hidden, three repeats. A 72-hour gap cannot be tested on the main data (the longest run of consecutive hours is 52); it is tested on the second dataset.

MAE on the hidden values:

| Variable | Method | 1 h | 3 h | 6 h | 12 h | 24 h |
|---|---|---:|---:|---:|---:|---:|
| Temperature (°C) | (a) Windowed interpolation | 0.49 | 0.77 | not filled | not filled | not filled |
| | Linear, no gap limit (reference) | 0.51 | 0.84 | 1.20 | 1.84 | 2.65 |
| | (b) Time-of-day | 1.61 | 1.71 | 1.87 | 2.06 | 2.13 |
| | (c) BRITS-style | 0.76 | 1.13 | 1.43 | 1.83 | 2.00 |
| Humidity (%) | (a) Windowed interpolation | 1.80 | 2.66 | not filled | not filled | not filled |
| | Linear, no gap limit (reference) | 1.88 | 2.92 | 4.47 | 5.85 | 7.97 |
| | (b) Time-of-day | 5.91 | 5.94 | 6.76 | 7.40 | 7.99 |
| | (c) BRITS-style | 2.92 | 4.30 | 5.83 | 7.33 | 7.38 |
| PM2.5 (µg/m³) | (a) Windowed interpolation | 8.98 | 11.09 | not filled | not filled | not filled |
| | Linear, no gap limit (reference) | 8.96 | 11.37 | 13.02 | 14.11 | 12.47 |
| | (b) Time-of-day | 10.53 | 12.53 | 12.52 | 12.33 | 13.71 |
| | (c) BRITS-style | 7.87 | 11.00 | 11.80 | 10.84 | 11.90 |

Reading: interpolation is best for 1–3 hours for weather; the BRITS-style model is best or joint best for PM2.5 at every length and is the best method that fills everything from 6 hours up; at 24 hours it is close to the time-of-day method because it reverts to the typical daily pattern. Unlimited linear interpolation fills only 36–42 % of 24-hour gaps and its R² turns negative. PM2.5 R² never exceeds 0.46. RMSE and R² tables are in the notebook.

## 13. Downstream effect of the imputation method

The selected Random Forest, LightGBM and the LSTM with PM2.5 history were retrained with weather cleaned by (a) windowed interpolation only, (b) time-of-day imputation, (c) BRITS-style imputation, under all three validation setups. The imputer is fitted on each fold's training cells only; PM2.5 is withheld from the imputer when it fills weather; scores use real PM2.5 readings only.

MAE (µg/m³, mean over folds):

| Setup | Model | (a) | (b) | (c) |
|---|---|---:|---:|---:|
| Hold-out | Random Forest (untuned) | 11.72 | 11.78 | 11.98 |
| Hold-out | LightGBM | 23.37 | 21.88 | 21.76 |
| Hold-out | LSTM with history | 13.71 | 12.61 | 13.31 |
| Expanding CV | Random Forest (untuned) | 29.19 | 30.57 | 32.35 |
| Expanding CV | LightGBM | 22.40 | 23.41 | 23.59 |
| Expanding CV | LSTM with history | 13.67 | 13.81 | 13.52 |
| Leave-sensors-out | Random Forest (untuned) | 15.74 | 15.73 | 15.66 |
| Leave-sensors-out | LightGBM | 16.17 | 16.19 | 16.21 |
| Leave-sensors-out | LSTM with history | 10.91 | 10.85 | 10.93 |

Conclusion: the differences are small and no method is consistently best ((a) best 4 times, (c) 3, (b) 2). Weather carries only about 13–14 % of what the tree models rely on, so better weather imputation cannot change the prediction much. The pipeline keeps (b).

## 14. SHAP explainability

Figures: `shap_bar_*.png`, `shap_beeswarm_*.png`, `shap_dependence_*.png`, `shap_lstm_feature_and_lag.png`, `shap_waterfall_case_1..3.png`, `shap_waterfall_sensor_1..2.png`.

SHAP values (Lundberg & Lee, 2017; TreeExplainer, Lundberg et al., 2020) were computed on 400 test rows of the hold-out with 100 training rows as background, in µg/m³, with the 149 sensor columns grouped into 'sensor identity'. The LSTM was explained with `shap.GradientExplainer`, which worked on TensorFlow 2.21, so the permutation fallback was not needed.

Share of mean |SHAP| by feature group:

| Feature group | Random Forest (selected) | LightGBM |
|---|---:|---:|
| Month | 45 % | 13 % |
| Hour of day | 19 % | 18 % |
| Sensor identity | 18 % | 23 % |
| Day of week | 5 % | 32 % |
| Temperature | 7 % | 8 % |
| Humidity | 5 % | 6 % |

- The trees rely on calendar and sensor identity far more than on weather. The weight on month and day of week mostly identifies which observation burst a row came from, which does not transfer to other dates.
- LSTM: the previous hour's PM2.5 is the top input (12.3 µg/m³, about twice the next channel) and most attribution is in the last step of the 6-hour window (8.0 at the predicted hour, 2.7 one hour before, about 1 for older steps).
- Local cases: the largest error (560 predicted, 43 actual) comes almost entirely from sensor identity (+436); the high episode (246 actual) is under-predicted (87).
- Imputed inputs: offline % and an imputed flag are not model inputs; weather carries 12–15 % of attribution whether measured or imputed, so imputed values do not drive predictions.
- SHAP shows what a model relies on, not what causes PM2.5.

## 15. Sensor maps

Figures: `map_sensor_network.png`, `map_coverage_voronoi_buffers.png`, `map_model_and_imputation_error.png`, `map_error_vs_neighbour_distance.png`.

- Coordinates come from the `latitude` and `longitude` columns (median per sensor). 143 of 149 sensors have coordinates; six have none and are left off the maps. Nothing was invented.
- Geometry: shapely points in a geopandas GeoDataFrame, EPSG:4326, reprojected to UTM 36N (EPSG:32636) for distances; 139 of 143 sensors are inside the zone and the rest are 0.06° west of its edge.
- Boundary layer: `data/uganda_adm1_boundaries.geojson` (geoBoundaries gbOpen, UGA ADM1, OpenStreetMap/Wambacher, ODbL). No web tiles.
- Coverage: 140 distinct locations; 41 have data-poor sensors only. Convex hull 82,796 km²; Voronoi area served by data-poor locations only 7,366 km²; area within 1 km of any sensor 297 km², of which 60 km² is within 1 km of data-poor sensors only.
- Error and location: Spearman correlation of prediction error and imputation error with offline time is 0.31 and 0.30; with nearest-neighbour distance −0.12 and −0.08; with neighbours within 5 km 0.10 and 0.07. Error follows offline time weakly and does not follow location or sensor density.

## 16. Second dataset test

File used: `AirQo_August_2026_hourly_matched_partial.csv` (in the project folder, not tracked in git; the only new data file found). 8,958 hourly rows, 17 sensors, 1–30 August 2026, same columns and units as the main file; the PM10 column is empty. Nine sensors are in the main data, eight are new, and five of the new ones are outside Uganda (four in Maputo province, Mozambique; one in Pretoria, South Africa). It was used as an external test set with no retraining.

Figures: `second_density_comparison.png`, `second_imputation_error_vs_gap_length.png`, `second_data_rich_vs_poor.png`, `second_calendar_actual_vs_predicted.png`, `second_calendar_absolute_error.png`, `second_timeseries_*.png`, `second_shap_beeswarm.png`, `second_map_*.png`.

PM2.5 prediction (µg/m³):

| Model | August MAE | August RMSE | August R² | Main hold-out MAE |
|---|---:|---:|---:|---:|
| LightGBM | 19.05 | 26.87 | 0.00 | 21.88 |
| Baseline (training mean) | 19.75 | 26.83 | 0.00 | 19.20 |
| Random Forest (untuned, selected) | 19.77 | 29.85 | −0.24 | 11.78 |
| Random Forest (tuned) | 19.81 | 29.87 | −0.24 | 11.83 |
| LSTM (weather + time) | 20.53 | 27.86 | −0.08 | 13.42 |
| LSTM with PM2.5 history | 21.14 | 28.61 | −0.14 | 12.61 |
| KNN | 21.32 | 31.79 | −0.41 | 12.06 |
| SVR | 41.49 | 49.82 | −2.45 | 22.24 |

- No model is meaningfully better than the training-mean baseline on August.
- Calendar: predicted 'Moderate' on all 30 days; actual 'Unhealthy for Sensitive Groups' on 18 days; 12 of 30 days match.
- Seen versus new sensors (Random Forest): MAE 21.9 on the nine known sensors and 16.4 on the eight new ones, which are cleaner sites.
- Data-rich versus data-poor: 10 data-rich, 4 intermediate, 3 data-poor sensors; with only 166 rows from data-poor sensors the comparison is not reliable.
- Imputation with the fitted imputers (MAE): temperature BRITS-style 1.49 °C at 6 h, 2.11 at 24 h, 2.38 at 72 h (time-of-day 1.81, 2.33, 2.45); humidity time-of-day 6.2 % at 6 h and 10.9 % at 72 h (BRITS-style 7.0 and 11.8); PM2.5 about 18–21 µg/m³ for every method.
- Evidently: 7 of 9 input features drifted between the main training data and August (`evidently_second_dataset_drift_report.html`).
- SHAP: same ordering of drivers; the sensor-identity contribution halves (Random Forest 4.6 to 2.2 µg/m³).

Reasons for the drop: an unseen month (the largest SHAP driver), eight unseen sensors, five sensors in another country and season, and a more polluted, less humid period. Missingness is not a cause; the August sensors are more complete. Weather imputation transfers to the new data; PM2.5 prediction does not.

## 17. References

- Cao, W., Wang, D., Li, J., Zhou, H., Li, L., & Li, Y. (2018). BRITS: Bidirectional Recurrent Imputation for Time Series. *NeurIPS 31*, pp. 6776–6786. arXiv:1805.10572.
- Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 30*, pp. 4765–4774.
- Lundberg, S. M., et al. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2, 56–67.
- Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. *JAIR*, 16, 321–357.
