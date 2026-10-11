"""Serve the trained PM2.5 model as an HTTP prediction endpoint.

Run after train.ipynb has created best_pm25_model.joblib:

    python serve_model.py            # listens on port 8000

Endpoints:
    GET  /health    -> model name and status
    POST /predict   -> {"rows": [{feature: value, ...}, ...]}
                       returns PM2.5 (ug/m3) and the AQI category per row

Each row needs: temperature, humidity, hour_sin, hour_cos,
day_of_week_sin, day_of_week_cos, month_sin, month_cos, device_name.
The list is read from the saved model, so it always matches the artifact.
PM10 is not used. Missing weather values may be left out; the pipeline
fills them with the training median.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import joblib
import pandas as pd

MODEL_PATH = os.environ.get('MODEL_PATH', 'best_pm25_model.joblib')
PORT = int(os.environ.get('PORT', '8000'))

artifact = joblib.load(MODEL_PATH)
pipeline = artifact['pipeline']
feature_columns = artifact['numeric_feature_columns'] + artifact['categorical_feature_columns']

AQI_BANDS = [
    (9, 'Good'),
    (35.49, 'Moderate'),
    (55.49, 'Unhealthy for Sensitive Groups'),
    (125.49, 'Unhealthy'),
    (225.49, 'Very Unhealthy'),
    (float('inf'), 'Hazardous'),
]


def aqi_category(pm25):
    return next(name for limit, name in AQI_BANDS if pm25 <= limit)


def predict(rows):
    frame = pd.DataFrame(rows).reindex(columns=feature_columns)
    zscores = pipeline.predict(frame)
    pm25 = zscores * artifact['target_scaler_std'] + artifact['target_scaler_mean']
    return [
        {'predicted_pm25_ug_m3': round(float(value), 3), 'aqi_category': aqi_category(value)}
        for value in pm25
    ]


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == '/health':
            self.send_json(200, {'status': 'ok', 'model': artifact['model_name'], 'features': feature_columns})
        else:
            self.send_json(404, {'error': 'Use GET /health or POST /predict'})

    def do_POST(self):
        if self.path != '/predict':
            self.send_json(404, {'error': 'Use POST /predict'})
            return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            self.send_json(200, {'predictions': predict(body['rows'])})
        except Exception as error:
            self.send_json(400, {'error': f'{type(error).__name__}: {error}'})


if __name__ == '__main__':
    print(f"Serving {artifact['model_name']} on port {PORT} (GET /health, POST /predict)")
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
