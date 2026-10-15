# Deploying the AirQo PM2.5 pipeline

## Where the project is deployed

The deployment changed several times. In order:

1. **RunPod (planned, dropped).** We planned to run the pipeline on an RTX 2000 Ada Pod with a run script and a prediction endpoint. RunPod needs prepaid credit, which was too costly for us, so we dropped it.
2. **Kaggle (cloud execution).** The first, PM10-based notebook was run end to end on Kaggle as evidence of cloud execution (instructions below).
3. **Hugging Face (model and static demo).** The first model and its August forecasts were published on Hugging Face; see [HUGGINGFACE.md](HUGGINGFACE.md). Server-side Spaces need a paid plan (HTTP 402), so the demo only shows stored forecasts.
4. **Render + Vercel (final).** The current forecast model (tuned SVR, `best_pm25_model.joblib`) runs as a web service on Render, and a dashboard on Vercel calls it.
   - Render service: **[ADD LINK]**
   - Vercel dashboard: **[ADD LINK]**

The current model does not use PM10. PM2.5 is the fine fraction of PM10, so PM10 is a co-measurement of the same particles rather than a driver of PM2.5, and it is not known ahead of time. The model predicts PM2.5 from temperature, humidity (which the literature identifies as drivers), the cyclical hour / day-of-week / month features and `device_name`.

## Model service (`serve_model.py`)

`serve_model.py` loads `best_pm25_model.joblib` and serves:

- `GET /health`: model name and feature list
- `POST /predict`: `{"rows": [{feature: value, ...}]}` returns PM2.5 (µg/m³) and the AQI category per row

It reads the port from `PORT` and the model path from `MODEL_PATH`. To run it locally:

```bash
pip install -r requirements-render.txt
python serve_model.py
```

`requirements-render.txt` holds only what is needed to load the model and predict (numpy, pandas, scikit-learn, scipy, joblib). TensorFlow, LightGBM, SHAP and the mapping libraries are needed for training only.

On Render, use `pip install -r requirements-render.txt` as the build command and `python serve_model.py` as the start command. `*.joblib` files are in `.gitignore`, so the model file has to be supplied to the service separately.

The saved nowcast model (`best_pm25_nowcast_model.joblib`, LightGBM with PM2.5 history) is not served, because every request would need the sensor's readings from the previous three hours.

## Run the pipeline on Kaggle

1. **Create the notebook.** On kaggle.com, choose **Create → New Notebook**, then **File → Import Notebook** and upload `train.ipynb`.
2. **Attach the data.** Choose **Add Input → Upload** and upload `Sensor Data Jan - July 2026.csv` and `AirQo_August_2026_hourly_matched.csv` as a dataset. The notebook finds the files under `/kaggle/input/`.
3. **Turn on internet** in the notebook settings (needed to install packages; Kaggle may ask you to verify your phone number first).
4. **Install the tested package versions.** Upload `requirements.txt`, add a cell at the very top with `!pip install -q -r /kaggle/input/<dataset>/requirements.txt`, run it, then restart the session.
5. **Run in the cloud.** Choose **Save Version → Save & Run All (Commit)**. The revised pipeline took about 56 minutes on a 16-core CPU locally; expect it to take longer on Kaggle's CPU.

## Runtime logs and resulting metrics

| Where | What it shows |
| --- | --- |
| **Logs** tab (Kaggle) | Kaggle's runtime log of the whole run |
| Last cell of the notebook | The run log: platform, hardware, start and end time, runtime, peak RAM, rows at each stage, every model's test scores, the selected model's metrics and AQI accuracy, forecasts and monitoring result |
| `deployment_outputs/` | `kaggle_run_log.txt` and `kaggle_run_metrics.json` (the run log as files), `run_resource_report.json`, the forecasts, `model_validation_comparison.csv` |

The files currently in `deployment_outputs/` come from the local run of the revised pipeline (the header of `kaggle_run_log.txt` says "Local machine"), not from Kaggle.

## Local verification

The revised notebook was run end to end locally with the versions in `requirements.txt` (Windows 11, Python 3.13, 16 logical CPUs): 0 errors, about 56 minutes, peak RAM about 1.2 GB. The selected forecast model, a tuned SVR, scored MAE 9.34 µg/m³, RMSE 15.14 and R² 0.34 on the 2–3 June hold-out; the nowcast model (LightGBM + PM2.5 history) scored MAE 8.43 and R² 0.42. The first, PM10-based Random Forest scored MAE 3.10, but that accuracy came from a same-hour co-measurement of the same particles, not from a driver of PM2.5, and the model cannot forecast.

## If something goes wrong

| Problem | Fix |
| --- | --- |
| `StopIteration` when loading the data | The CSV is not attached. Add it with **Add Input** (step 2) |
| Evidently fails to install or errors | The notebook skips the remaining Evidently cells and finishes. To skip Evidently entirely, add `import os; os.environ['AIRQO_SKIP_EVIDENTLY'] = '1'` as the first cell |
| Errors after installing packages | Restart the session after the `pip install` cell so the new versions load |
