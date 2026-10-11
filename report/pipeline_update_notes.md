# AirQo PM2.5 pipeline: change notes

The full write-up is now in `report/main.tex`. These notes list what changed in each round and the headline numbers of the current run, so the report can be checked against them. All numbers come from the run stored in `train.ipynb` (local machine, Python 3.13, about 65 minutes, 346 code cells, 0 errors, 70 figures). Figures are in `report/figures/`.

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
4. **PM10 stays out.**
5. **EDA sites with data.** A Kampala site must have readings in every month that contains data. The five sites are Nakasero II, Lower Nsooba, Salama Road, Namungona Primary School and Kabusu; the EDA time-series figures now use these five plus the network mean, so no panel is empty.
6. **Effect of the bidirectional LSTM (BRITS-style) imputation.** The imputer now uses LSTM cells. A new section answers three questions:
   - As an imputer it is better than the time-of-day method in all 15 variable-and-gap combinations, by 21 % on average.
   - It fills every real gap (interpolation fills only 5–12 %), but its fills are smoother than real readings (PM2.5 standard deviation 11.9 against 26.8 observed).
   - For training it brings no reliable gain: prediction MAE changed by −0.4 % on average and improved in 7 of 15 cases.
7. **Report** (`report/main.tex`) rewritten for the current pipeline, with the UCU logo on the title page (`report/figures/ucu_logo.png`).

## Still to do by hand

- Compile `main.tex` (no LaTeX compiler was available on this machine, so it has not been compiled here) and rebuild `airqo_report_overleaf.zip`.
- Re-run the notebook on Kaggle and fill in the red placeholders in the Kaggle table of the report.
- Update the Hugging Face model card, demo and `DEPLOYMENT.md` / `HUGGINGFACE.md`, which still describe the PM10-based Random Forest.

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
