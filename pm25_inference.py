
import argparse
from pathlib import Path

import joblib
import pandas as pd


AQI_CATEGORIES = [
    'Good',
    'Moderate',
    'Unhealthy for Sensitive Groups',
    'Unhealthy',
    'Very Unhealthy',
    'Hazardous'
]


def pm25_aqi_category(pm25_value):
    if pd.isna(pm25_value):
        return pd.NA

    if pm25_value < 0:
        return 'Invalid'

    if pm25_value <= 9:
        return 'Good'
    elif pm25_value <= 35.49:
        return 'Moderate'
    elif pm25_value <= 55.49:
        return 'Unhealthy for Sensitive Groups'
    elif pm25_value <= 125.49:
        return 'Unhealthy'
    elif pm25_value <= 225.49:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'


def main():
    parser = argparse.ArgumentParser(
        description='Predict PM2.5 using the saved AirQo model.'
    )

    parser.add_argument(
        '--model',
        required=True,
        help='Path to best_pm25_model.joblib'
    )

    parser.add_argument(
        '--input',
        required=True,
        help='CSV containing model-ready feature columns'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Destination CSV for predictions'
    )

    args = parser.parse_args()

    model_artifact = joblib.load(args.model)
    input_data = pd.read_csv(args.input)

    pipeline = model_artifact['pipeline']
    target_mean = model_artifact['target_scaler_mean']
    target_std = model_artifact['target_scaler_std']

    numeric_features = (
        model_artifact['numeric_feature_columns']
    )

    categorical_features = (
        model_artifact['categorical_feature_columns']
    )

    feature_columns = (
        numeric_features
        + categorical_features
    )

    missing_columns = [
        column
        for column in feature_columns
        if column not in input_data.columns
    ]

    if missing_columns:
        raise ValueError(
            f'Missing required feature columns: {missing_columns}'
        )

    model_input = input_data[feature_columns].copy()

    predicted_zscores = pipeline.predict(model_input)

    predicted_pm25 = (
        predicted_zscores * target_std
        + target_mean
    )

    predictions = input_data.copy()

    predictions['predicted_pm25_ug_m3'] = predicted_pm25

    predictions['aqi_category'] = (
        predictions['predicted_pm25_ug_m3']
        .apply(pm25_aqi_category)
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    predictions.to_csv(
        output_path,
        index=False
    )

    print('Inference completed successfully.')
    print(f'Input rows: {len(input_data)}')
    print(f'Output rows: {len(predictions)}')
    print(f'Output path: {output_path.resolve()}')
    print(
        'Missing predictions: '
        f'{predictions["predicted_pm25_ug_m3"].isna().sum()}'
    )


if __name__ == '__main__':
    main()
