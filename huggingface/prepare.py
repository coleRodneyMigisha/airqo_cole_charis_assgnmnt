"""Get the Hugging Face folders ready to upload. Run after train.ipynb:

    python huggingface/prepare.py

- huggingface/space/forecasts.json  <- the August forecasts shown by the page
- huggingface/model/                <- gets a copy of the model and inference script
"""

import json
import shutil
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

daily = pd.read_csv(ROOT / 'deployment_outputs/daily_pm25_predictions_august_1_to_14.csv')
hourly = pd.read_csv(ROOT / 'deployment_outputs/hourly_pm25_predictions_august_1.csv')

daily = daily.sort_values(['device_name', 'date'])
hourly = hourly.sort_values(['device_name', 'datetime'])

sensors = []
for device, rows in daily.groupby('device_name'):
    hours = hourly[hourly['device_name'] == device]
    sensors.append({
        'id': device,
        'site': rows['site_name'].iloc[0],
        'daily': rows['predicted_pm25_ug_m3'].round(1).tolist(),
        'hourly': hours['predicted_pm25_ug_m3'].round(1).tolist(),
    })

sensors.sort(key=lambda sensor: sensor['site'].lower())

forecasts = {
    'dates': sorted(daily['date'].str[:10].unique()),
    'sensors': sensors,
}

(ROOT / 'huggingface/space/forecasts.json').write_text(json.dumps(forecasts))

shutil.copy(ROOT / 'best_pm25_model.joblib', ROOT / 'huggingface/model/')
shutil.copy(ROOT / 'pm25_inference.py', ROOT / 'huggingface/model/')

print(f'forecasts.json written for {len(sensors)} sensors')
print('Model files copied to huggingface/model/')
