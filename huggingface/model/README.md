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

# AirQo PM2.5 model (tuned Random Forest)

A scikit-learn pipeline that predicts hourly PM2.5 concentration (µg/m³) for AirQo low-cost air-quality sensors in Uganda. It was built for CSC3119 AI Deployment & Scalability, Assignment 4, at Uganda Christian University.

Interactive forecasts: [Kyalis/airqo-pm25-forecasts](https://huggingface.co/spaces/Kyalis/airqo-pm25-forecasts)

## Results on the held-out test period

Chronological split: trained on 1 Jan – 1 Jun 2026, tested on 2–3 Jun 2026 (2,642 hourly readings from 119 sensors).

| Metric | Value |
|---|---|
| MAE | 3.103 µg/m³ |
| RMSE | 7.003 µg/m³ |
| R² | 0.898 |

Converted to AQI categories, 86.2% of the test hours fall in the correct category.

## Inputs

| Column | Meaning |
|---|---|
| `temperature`, `humidity` | Sensor weather readings. Missing readings (sensor dropouts) are encoded as 0 by the pipeline |
| `pm10_calibrated_value` | PM10 from the same sensor at the same hour |
| `hour_sin`, `hour_cos`, `day_of_week_sin`, `day_of_week_cos`, `month_sin`, `month_cos` | Cyclical encodings of the timestamp, e.g. `hour_sin = sin(2π·hour/24)` |
| `device_name` | AirQo device identifier (one-hot encoded; unknown devices are ignored) |

The model was trained on a Z-score of PM2.5. The artifact stores the scaler, so predictions are converted back with `prediction × target_scaler_std + target_scaler_mean`. The included `pm25_inference.py` does this for you.

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

AirQo sensor data, January–June 2026: 14,600 hourly records from 149 sensors at 142 sites. Only 8 days actually contain readings (1–3 January, 1–2 April, 1–3 June). Zero values for temperature, humidity, PM2.5 and PM10 were treated as missing.

## Limitations

- **PM10 must be known at the same hour.** PM10 carries most of the model's predictive power. For real forecasting PM10 is not known in advance; the August 2026 forecasts used each sensor's typical hour-of-day values instead, so they show each site's typical daily pattern rather than reacting to actual conditions.
- **Very little training data.** Eight days in three months; seasonal patterns are not learned.
- **Known sensors only.** Sensors not in the training data lose their site-specific adjustment.

## Files

| File | Contents |
|---|---|
| `best_pm25_model.joblib` | Pipeline, target scaler and feature lists |
| `pm25_inference.py` | Command-line inference script |

AQI categories (µg/m³): Good 0–9 · Moderate 9.1–35.49 · Unhealthy for Sensitive Groups 35.5–55.49 · Unhealthy 55.5–125.49 · Very Unhealthy 125.5–225.49 · Hazardous above 225.49.
