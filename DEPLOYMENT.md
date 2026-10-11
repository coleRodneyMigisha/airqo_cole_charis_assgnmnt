# Deploying the AirQo PM2.5 pipeline on Kaggle

The pipeline is deployed by running `train.ipynb` end to end on Kaggle's cloud notebook service. Kaggle provides free CPU and GPU notebooks, runs a saved notebook as a batch job in the cloud, and keeps the run's log and output files with each saved version.

The trained model and a forecast demo page are published on Hugging Face; see [HUGGINGFACE.md](HUGGINGFACE.md).

## Run the pipeline on Kaggle

1. **Create the notebook.** On kaggle.com, choose **Create → New Notebook**, then **File → Import Notebook** and upload `train.ipynb`.
2. **Attach the data.** Choose **Add Input → Upload** and upload `Sensor Data Jan - July 2026.csv` as a dataset. The notebook finds the file under `/kaggle/input/` automatically.
3. **Turn on internet** in the notebook settings (needed to install packages; Kaggle may ask you to verify your phone number first).
4. **Install the tested package versions.** Add a cell at the very top, run it, then restart the session:

   ```python
   !pip install -q pandas==2.3.3 numpy==2.1.3 scikit-learn==1.7.2 scipy==1.16.1 matplotlib==3.10.5 joblib==1.4.2 evidently==0.7.23
   ```

5. **Run in the cloud.** Choose **Save Version → Save & Run All (Commit)**. Kaggle runs the whole notebook as a batch job; the pipeline takes about 11–15 minutes.

## Runtime logs and resulting metrics

When the version finishes, open it:

| Where | What it shows |
| --- | --- |
| **Logs** tab | Kaggle's runtime log of the whole run |
| Last cell of the notebook (section 18) | The run log: platform, hardware, start and end time, runtime, peak RAM, rows at each stage, every model's test scores, the selected model's metrics and AQI accuracy, forecasts and monitoring result |
| **Output** tab | `deployment_outputs/kaggle_run_log.txt` and `kaggle_run_metrics.json` (the run log as files), `run_resource_report.json`, the forecasts, the Evidently reports and `best_pm25_model.joblib` |

Download the Output files and take screenshots of the Logs tab and the final cell for the report.

## Local verification

The notebook was run end to end locally with the versions in `requirements.txt` before deploying: all cells executed with 0 errors, the selected tuned Random Forest scored MAE 3.103 µg/m³, RMSE 7.003 and R² 0.898 on the test set, and the run took about 11 minutes with about 1 GB of RAM.

## If something goes wrong

| Problem | Fix |
| --- | --- |
| `StopIteration` when loading the data | The CSV is not attached. Add it with **Add Input** (step 2) |
| Evidently fails to install or errors | The notebook skips the remaining Evidently cells and finishes. To skip Evidently entirely, add `import os; os.environ['AIRQO_SKIP_EVIDENTLY'] = '1'` as the first cell |
| Errors after installing packages | Restart the session after the `pip install` cell so the new versions load |
