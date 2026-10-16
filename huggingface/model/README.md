---
library_name: sklearn
pipeline_tag: tabular-regression
tags:
  - scikit-learn
  - tabular-regression
  - air-quality
  - pm2.5
  - airqo
  - uganda
---

# AirQo PM2.5 forecast model (tuned SVR)

A scikit-learn pipeline that predicts hourly PM2.5 concentration (µg/m³) for AirQo low-cost air-quality sensors in Uganda from temperature, humidity, time and sensor identity. It was built for CSC3119 AI Model Deployment and Scalability, Assignment 4, at Uganda Christian University, by Charis Opol and Cole Rodney Migisha.

Forecast demo: [Kyalis/airqo-pm25-forecasts](https://huggingface.co/spaces/Kyalis/airqo-pm25-forecasts)

**Note on the repository name.** The first version of this repository held a Random Forest that used PM10 as an input (test MAE 3.10 µg/m³). PM2.5 is the fine fraction of PM10, so PM10 is a co-measurement of the same particles rather than a driver of PM2.5, and it is measured in the same hour, so it is not known in advance and that model could not forecast. The current model uses temperature and humidity, which the literature identifies as drivers of PM2.5, together with time and sensor identity. It was replaced by the model described here, which does not use PM10. The repository name was kept.

## Results on the held-out test period

Chronological split: trained on 1 Jan – 1 Jun 2026, tested on 2–3 Jun 2026 (2,642 hourly readings).

| Metric | Value |
|---|---|
| MAE | 9.34 µg/m³ |
| RMSE | 15.14 µg/m³ |
| R² | 0.34 |
| Baseline (training mean), MAE | 17.60 µg/m³ |

Converted to AQI categories, 75.2% of the test hours fall in the correct category (always predicting the training mean scores 74.4%, because most hours are Moderate).

On an external test covering all of August 2026 (73,274 rows, 125 sensors) the model is barely better than the baseline (MAE 18.32 against 19.21 µg/m³): it predicts each sensor's typical daily pattern and does not anticipate pollution episodes.

## Inputs

| Column | Meaning |
|---|---|
| `temperature`, `humidity` | Sensor weather readings. Missing values may be left empty; the pipeline fills them with the training median |
| `hour_sin`, `hour_cos`, `day_of_week_sin`, `day_of_week_cos`, `month_sin`, `month_cos` | Cyclical encodings of the UTC timestamp, e.g. `hour_sin = sin(2π·hour/24)` |
| `device_name` | AirQo device identifier (one-hot encoded; unknown devices are ignored) |

PM10 is not used. The model was trained on a Z-score of PM2.5. The artifact stores the scaler, so predictions are converted back with `prediction × target_scaler_std + target_scaler_mean`. The included `pm25_inference.py` does this for you.

## How to use

The artifact needs **scikit-learn 1.7.2** to load reliably.

```python
import joblib
from huggingface_hub import hf_hub_download

path = hf_hub_download("Kyalis/airqo-pm25-random-forest", "best_pm25_model.joblib")
artifact = joblib.load(path)

columns = artifact["numeric_feature_columns"] + artifact["categorical_feature_columns"]
z = artifact["pipeline"].predict(features[columns])          # features: a pandas DataFrame
pm25 = z * artifact["target_scaler_std"] + artifact["target_scaler_mean"]
```

Or from the command line:

```bash
python pm25_inference.py --model best_pm25_model.joblib --input features.csv --output predictions.csv
```

`best_pm25_model.joblib` is a pickle. Loading a pickle can run code, so only load it from this repository or another source you trust.

## Training data

AirQo sensor data, January–June 2026: 14,600 hourly records from 149 sensors at 145 sites. Only 8 days contain readings (1–3 January, 1–2 April, 1–3 June). Zero values were treated as missing; extreme PM2.5 readings (above the sensor's Q3 + 3 × IQR, 1.5% of readings) were replaced by the nearest normal reading of the same sensor; weather gaps were filled by windowed interpolation and time-of-day imputation fitted on training rows only.

## Limitations

- **Very little training data.** Eight days in three months; seasonal patterns are not learned, and the model does not transfer well to a new month.
- **No recent PM2.5.** A model that also uses the last three hours of PM2.5 (LightGBM, MAE 8.43 µg/m³) is more accurate but needs recent readings with every request, so it is not published here.
- **Known sensors only.** Sensors not in the training data lose their site-specific adjustment.

## Files

| File | Contents |
|---|---|
| `best_pm25_model.joblib` | Pipeline, target scaler and feature lists |
| `pm25_inference.py` | Command-line inference script |

AQI categories (µg/m³): Good 0–9 · Moderate 9.1–35.49 · Unhealthy for Sensitive Groups 35.5–55.49 · Unhealthy 55.5–125.49 · Very Unhealthy 125.5–225.49 · Hazardous above 225.49.
