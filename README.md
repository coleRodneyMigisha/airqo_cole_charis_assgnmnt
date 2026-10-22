# AirQo PM2.5 Prediction and Deployment

A reproducible machine-learning pipeline for estimating and forecasting fine particulate matter (PM2.5) concentrations from AirQo sensor data. The project includes data preparation, imputation, feature engineering, model comparison, validation, monitoring, standalone inference, and a lightweight HTTP prediction service.

> **Current deployment model:** the served forecast model is a tuned Support Vector Regressor (`SVR (tuned)`) that uses weather, calendar, and sensor-identity features. PM10 is deliberately excluded because it is a co-measurement of the same particulate matter and is not available in advance for a genuine forecast.

## Project links

- GitHub repository: <https://github.com/coleRodneyMigisha/airqo_cole_charis_assgnmnt>
- Backend deployment: <https://airqo-cole-charis-assgnmnt.onrender.com/> (`/health`)
- Frontend dashboard: <https://airqo-model.vercel.app/>
- Hugging Face documentation: [HUGGINGFACE.md](HUGGINGFACE.md)
- Detailed deployment notes: [DEPLOYMENT.md](DEPLOYMENT.md)

## What the project does

The main workflow in [`train.ipynb`](train.ipynb) performs the following steps:

1. Loads the January–July 2026 hourly sensor dataset.
2. Cleans timestamps and sensor records, removes PM10 from the modeling inputs, and treats invalid zero weather measurements as missing where required.
3. Resamples sensor observations to an hourly grid and imputes missing weather and PM2.5 values using the methods implemented in the notebook.
4. Creates cyclical time features for hour, day of week, and month.
5. Compares classical machine-learning models, tree-based models, and LSTM variants.
6. Evaluates models with chronological, expanding-window, and leave-sensors-out validation setups.
7. Selects and serializes the deployment forecast model as `best_pm25_model.joblib`.
8. Produces August forecasts, AQI categories, runtime/resource reports, and optional Evidently monitoring reports.
9. Validates that the serialized artifact reproduces notebook predictions and that the standalone inference path works in a fresh process.

A separate nowcast model using recent PM2.5 history is also evaluated in the notebook. It is not the model exposed by [`serve_model.py`](serve_model.py), because serving it would require the previous three hours of sensor readings for every request.

## Repository structure

| Path | Purpose |
| --- | --- |
| `train.ipynb` | End-to-end data preparation, training, evaluation, forecasting, monitoring, and artifact validation pipeline |
| `pm25_inference.py` | Command-line inference against a saved Joblib artifact |
| `serve_model.py` | Dependency-light HTTP service with `/health` and `/predict` endpoints |
| `requirements.txt` | Full training and analysis environment |
| `requirements-render.txt` | Smaller runtime environment for the HTTP service |
| `DEPLOYMENT.md` | Deployment history and Kaggle/Render instructions |
| `HUGGINGFACE.md` | Hugging Face packaging and publishing instructions |
| `huggingface/` | Model-card and static forecast-space files |
| `data/uganda_adm1_boundaries.geojson` | Uganda administrative boundaries used by map visualizations |
| `deployment_outputs/` | Forecasts, validation tables, monitoring summaries, metrics, and resource reports |
| `report/` | LaTeX report source, compiled report, and report-generation utilities |
| `sources/` | Supporting literature and source list |
| `Sensor Data Jan - July 2026.csv` | Main historical training dataset |
| `AirQo_August_2026_hourly_matched.csv` | Later dataset used for external/generalization testing |

The generated model files (`*.joblib`) are excluded from Git because of GitHub's file-size limit. Run the notebook or obtain the artifact separately before running inference or the server.

## Requirements

- Python 3.11 or newer; the recorded full pipeline run used Python 3.13.7.
- For the complete notebook: the packages pinned in [`requirements.txt`](requirements.txt).
- For serving only: the packages pinned in [`requirements-render.txt`](requirements-render.txt).
- Approximately 1–2 GB of RAM was sufficient for the recorded local run; training took about 56 minutes on a 16-logical-CPU Windows machine. Runtime will vary by hardware and package versions.

## Installation

Create an isolated environment and install the full pipeline dependencies:

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

To install only the serving dependencies:

```bash
python -m pip install -r requirements-render.txt
```

## Run the training and forecasting pipeline

Open and run [`train.ipynb`](train.ipynb) from the repository root:

```bash
jupyter notebook train.ipynb
```

The notebook expects the CSV files to be available in the working directory. It writes or refreshes the following important artifacts:

- `best_pm25_model.joblib` — serialized forecast model and preprocessing pipeline.
- `best_pm25_nowcast_model.joblib` — history-based nowcast artifact, when produced by the notebook.
- `deployment_outputs/daily_pm25_predictions_august_1_to_14.csv` — daily predictions for 149 sensors over 14 days.
- `deployment_outputs/hourly_pm25_predictions_august_1.csv` — hourly predictions for 1 August.
- `deployment_outputs/deployment_metadata.json` — model, feature, forecast, and validation metadata.
- `deployment_outputs/kaggle_run_metrics.json` — recorded runtime, resource, model, and monitoring metrics.
- `evidently_*.html` and `evidently_*.json` — data/model drift reports when Evidently completes successfully.

For a cloud notebook run, see the Kaggle instructions in [DEPLOYMENT.md](DEPLOYMENT.md). The notebook contains optional Evidently sections; if Evidently cannot run, the core modeling pipeline can still complete.

## Model inputs

The current forecast artifact expects these nine model-ready columns:

### Numeric features

- `temperature`
- `humidity`
- `hour_sin`, `hour_cos`
- `day_of_week_sin`, `day_of_week_cos`
- `month_sin`, `month_cos`

### Categorical feature

- `device_name`

PM10, latitude, longitude, site name, and network metadata are not direct inputs to the served forecast model. Coordinates and descriptive fields are retained in forecast outputs where useful. Missing weather values are handled by the fitted preprocessing pipeline; input files must still contain the expected feature columns.

## Standalone batch inference

After `best_pm25_model.joblib` has been generated, create a CSV containing the nine model-ready columns and run:

```bash
python pm25_inference.py \
  --model best_pm25_model.joblib \
  --input deployment_outputs/test_features_for_standalone_inference.csv \
  --output predictions.csv
```

The output preserves the input columns and adds:

- `predicted_pm25_ug_m3` — predicted PM2.5 concentration in µg/m³.
- `aqi_category` — category derived from the predicted concentration.

The AQI labels used by the project are `Good`, `Moderate`, `Unhealthy for Sensitive Groups`, `Unhealthy`, `Very Unhealthy`, and `Hazardous`. Negative predictions are labeled `Invalid` by the standalone script.

## Run the HTTP prediction service

The service loads `best_pm25_model.joblib` at startup:

```bash
python serve_model.py
```

The default port is `8000`. Override it with `PORT`, and override the artifact path with `MODEL_PATH`:

```bash
MODEL_PATH=/path/to/best_pm25_model.joblib \
PORT=8000 \
CORS_ALLOWED_ORIGINS=http://localhost:5173 \
python serve_model.py
```

On Windows PowerShell, set the variables using `$env:MODEL_PATH`, `$env:PORT`, and `$env:CORS_ALLOWED_ORIGINS` before running the command.

### Health check

```bash
curl http://localhost:8000/health
```

The response reports the model name and feature list.

### Prediction request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "rows": [{
      "temperature": 21.1,
      "humidity": 84.0,
      "hour_sin": 0.0,
      "hour_cos": 1.0,
      "day_of_week_sin": 0.781831,
      "day_of_week_cos": 0.62349,
      "month_sin": 0.0,
      "month_cos": -1.0,
      "device_name": "ag_588c8125eca4"
    }]
  }'
```

A successful response has this shape:

```json
{
  "predictions": [
    {
      "predicted_pm25_ug_m3": 26.21,
      "aqi_category": "Moderate"
    }
  ]
}
```

For browser clients, configure `CORS_ALLOWED_ORIGINS` as a comma-separated allowlist. Do not use a wildcard in production.

## Recorded results

The selected forecast model was evaluated on a chronological hold-out period. The recorded results are:

| Metric | Value |
| --- | ---: |
| Model | `SVR (tuned)` |
| MAE | 9.341 µg/m³ |
| RMSE | 15.138 µg/m³ |
| R² | 0.338 |
| AQI-category accuracy | 0.752 |

The history-based LightGBM nowcast scored better on the same hold-out (MAE 8.425 µg/m³, R² 0.417), but it requires recent PM2.5 observations and is therefore a different operational task. The repository also records expanding-window and leave-sensors-out results; consult `deployment_outputs/kaggle_run_metrics.json` for the full comparison.

The recorded run processed 14,600 raw rows from 149 sensors, produced 758,112 hourly-grid rows, and used 11,633 training rows plus 2,642 chronological test rows. Forecast outputs contain 2,086 daily rows and 3,576 hourly rows.

## Monitoring and interpretation

The notebook creates Evidently data-drift and model-drift reports and compares missingness, error, and sensor coverage between reference and current data. In the recorded run, 8 of 9 monitored columns were flagged as drifting. This should be interpreted cautiously: much of the observed change came from calendar and sensor-population differences in a short comparison window, not necessarily from a change in the underlying PM2.5 process.

The August dataset is also used as a separate, no-retraining generalization test. It is not used to fit the main model. Review the notebook's second-dataset section and the generated monitoring artifacts when assessing out-of-period performance.

## Limitations and responsible use

- The reported scores are dataset- and split-specific; they are not a guarantee of accuracy for future locations or seasons.
- Sensor identity is a model feature, so performance can differ for sensors not represented during training.
- The forecast model uses typical hour-of-day weather profiles for future weather inputs; it does not consume live numerical weather forecasts.
- The served model is a forecast model, not the stronger history-based nowcast model.
- Predictions should support analysis and operational awareness, not replace calibrated regulatory monitoring or public-health guidance.
- Joblib files are serialized Python objects. Load model artifacts only from sources you trust.

## Further documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) — Render, Vercel, Kaggle, local verification, and troubleshooting.
- [HUGGINGFACE.md](HUGGINGFACE.md) — preparing and publishing the model/static forecast page.
- [`huggingface/model/README.md`](huggingface/model/README.md) — model-card and inference notes.
- [`report/main.pdf`](report/main.pdf) — compiled technical report.
