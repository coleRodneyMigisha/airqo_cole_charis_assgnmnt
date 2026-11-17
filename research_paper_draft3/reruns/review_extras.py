# Extra analyses asked for in Mr. Stephen's review (Nov 2026).
# These blocks run as cells AFTER train.ipynb, in the same kernel (see reproduce.py),
# so they reuse the notebook's data, splits, folds and tuned models unchanged.
# Each block is wrapped so that one failure is logged to review_extras/errors.txt
# and the other blocks still run. Outputs go to review_extras/.
# Comment numbers refer to the review file (0 = title comment).

import json
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone

REV = Path('review_extras')
REV.mkdir(exist_ok=True)
(REV / 'errors.txt').write_text('')
REVIEW = {}


def guarded(label):
    """Run a block; on error, log it and carry on."""
    def wrap(func):
        try:
            func()
            print(f"[ok] {label}")
        except Exception:
            with open(REV / 'errors.txt', 'a') as handle:
                handle.write(f"### {label}\n{traceback.format_exc()}\n")
            print(f"[FAILED] {label} (see review_extras/errors.txt)")
        return func
    return wrap


PERSIST = 'Persistence (last reading)'
KEY_TABULAR = [name for name in ['SVR (tuned)', 'LightGBM (tuned)', 'Random Forest (untuned baseline)',
                                 'KNN (tuned)', 'Random Forest + PM2.5 history',
                                 'LightGBM + PM2.5 history'] if name in model_results]
NO_MONTH_MODELS = [name for name in ['SVR (tuned)', 'LightGBM (tuned)',
                                     'Random Forest + PM2.5 history',
                                     'LightGBM + PM2.5 history'] if name in model_results]
MONTH_COLUMNS = ['month_sin', 'month_cos']


def persistence(frame, fallback):
    """Last real PM2.5 reading of the same sensor within three hours; else the training mean."""
    predicted = frame['pm25_lag_1h'].astype(float)
    for column in ['pm25_lag_2h', 'pm25_lag_3h']:
        predicted = predicted.fillna(frame[column].astype(float))
    return predicted.fillna(fallback).to_numpy(), frame['pm25_lag_1h'].notna().to_numpy()


def score_dict(actual, predicted):
    scores = regression_scores(actual, predicted)
    return {'MAE': scores['mae'], 'RMSE': scores['rmse'], 'R2': scores['r2'],
            'bias': float(np.mean(np.asarray(predicted, float) - np.asarray(actual, float)))}


holdout_test = chrono_data['test']
holdout_actual = holdout_test[target_column].astype(float).to_numpy()
holdout_persist, holdout_has_lag1 = persistence(holdout_test, chrono_data['target_mean'])

# %%
# Comments 14, 18, 20: persistence baseline under every design and on August.
@guarded('persistence baseline')
def _():
    rows = []
    rows.append({'setup': 'Chronological hold-out', 'fold': 'all', 'model': PERSIST,
                 'n': len(holdout_actual), **score_dict(holdout_actual, holdout_persist)})
    for setup in ['Expanding-window CV', 'Leave-sensors-out']:
        for fold in validation_folds[setup]:
            data = prepare_fold(fold)
            actual = data['test'][target_column].astype(float).to_numpy()
            predicted, _ = persistence(data['test'], data['target_mean'])
            rows.append({'setup': setup, 'fold': fold['label'], 'model': PERSIST,
                         'n': len(actual), **score_dict(actual, predicted)})
    august_persist, august_has_lag1 = persistence(second_rows, target_scaler_mean)
    rows.append({'setup': 'August 2026', 'fold': 'all', 'model': PERSIST,
                 'n': len(second_actual), **score_dict(second_actual, august_persist)})
    table = pd.DataFrame(rows)
    table.to_csv(REV / 'persistence_by_fold.csv', index=False)
    REVIEW['persistence_coverage'] = {
        'holdout_rows': int(len(holdout_actual)),
        'holdout_share_with_lag1': float(holdout_has_lag1.mean()),
        'august_rows': int(len(second_actual)),
        'august_share_with_lag1': float(august_has_lag1.mean()),
    }
    # The same comparison on hold-out rows that have a reading one hour earlier only.
    mask = holdout_has_lag1
    subset = {PERSIST: holdout_persist[mask],
              BASELINE_NAME: np.full(mask.sum(), chrono_data['target_mean'])}
    subset.update({name: np.asarray(model_results[name]['predictions_raw'])[mask]
                   for name in KEY_TABULAR})
    pd.DataFrame({name: score_dict(holdout_actual[mask], pred) for name, pred in subset.items()}).T \
        .to_csv(REV / 'holdout_rows_with_lag1.csv')
    globals()['august_persist'] = august_persist

# %%
# Comment 18: one full table, MAE, RMSE and R2 for every model, design and August.
@guarded('full comparison table with RMSE')
def _():
    persist = pd.read_csv(REV / 'persistence_by_fold.csv')
    persist_mean = persist.groupby(['setup', 'model'])[['MAE', 'RMSE', 'R2']].mean().reset_index()
    august = second_scores.reset_index().rename(columns={'index': 'model'})
    august = august.rename(columns=str.upper).rename(columns={'MODEL': 'model'})
    august['setup'] = 'August 2026'
    august['bias'] = [float(np.mean(second_predictions[m] - second_actual)) for m in august['model']]
    full = pd.concat([validation_summary, persist_mean,
                      august[['setup', 'model', 'MAE', 'RMSE', 'R2', 'bias']]], ignore_index=True)
    full.to_csv(REV / 'full_comparison_long.csv', index=False)
    wide = full.pivot_table(index='model', columns='setup', values=['MAE', 'RMSE', 'R2'])
    wide.to_csv(REV / 'full_comparison_wide.csv')
    # fold-level scores, for spread across folds
    fold_scores = pd.concat([validation_scores, persist.rename(columns={'n': 'validation_rows'})],
                            ignore_index=True)
    fold_scores.to_csv(REV / 'fold_scores.csv', index=False)

# %%
# Comment 18: confidence intervals. Sensor-cluster bootstrap (sensors resampled with
# replacement, all their hours kept), because hours of one sensor are not independent.
@guarded('bootstrap confidence intervals')
def _():
    def cluster_bootstrap(actual, predictions, groups, pairs, draws=1000):
        rng = np.random.default_rng(RANDOM_SEED)
        groups = np.asarray(groups).astype(str)
        unique = np.unique(groups)
        index_of = {g: np.flatnonzero(groups == g) for g in unique}
        mae = {name: np.empty(draws) for name in predictions}
        rmse = {name: np.empty(draws) for name in predictions}
        for b in range(draws):
            rows = np.concatenate([index_of[g] for g in rng.choice(unique, len(unique), replace=True)])
            for name, predicted in predictions.items():
                error = predicted[rows] - actual[rows]
                mae[name][b] = np.abs(error).mean()
                rmse[name][b] = np.sqrt((error ** 2).mean())
        table = pd.DataFrame({
            name: {'MAE': np.abs(predictions[name] - actual).mean(),
                   'MAE_lo': np.percentile(mae[name], 2.5), 'MAE_hi': np.percentile(mae[name], 97.5),
                   'RMSE': np.sqrt(((predictions[name] - actual) ** 2).mean()),
                   'RMSE_lo': np.percentile(rmse[name], 2.5), 'RMSE_hi': np.percentile(rmse[name], 97.5)}
            for name in predictions}).T
        diffs = pd.DataFrame({
            f'{a} minus {b}': {
                'MAE_diff': np.abs(predictions[a] - actual).mean() - np.abs(predictions[b] - actual).mean(),
                'lo': np.percentile(mae[a] - mae[b], 2.5),
                'hi': np.percentile(mae[a] - mae[b], 97.5),
                'share_of_draws_a_better': float(np.mean(mae[a] < mae[b]))}
            for a, b in pairs if a in predictions and b in predictions}).T
        return table, diffs

    pairs = [('Random Forest + PM2.5 history', PERSIST), ('LightGBM + PM2.5 history', PERSIST),
             ('Random Forest + PM2.5 history', 'LightGBM + PM2.5 history'),
             ('SVR (tuned)', BASELINE_NAME), ('SVR (tuned)', PERSIST),
             ('LSTM (weather + time + PM2.5 history)', PERSIST)]
    holdout_predictions = {name: np.asarray(pred, float) for name, pred in chrono_predictions.items()}
    holdout_predictions[PERSIST] = holdout_persist
    table, diffs = cluster_bootstrap(holdout_actual, holdout_predictions,
                                     holdout_test['device_name'], pairs)
    table.to_csv(REV / 'ci_holdout.csv')
    diffs.to_csv(REV / 'ci_holdout_differences.csv')
    august_predictions = {name: np.asarray(pred, float) for name, pred in second_predictions.items()}
    august_predictions[PERSIST] = august_persist
    table, diffs = cluster_bootstrap(second_actual, august_predictions,
                                     second_rows['device_name'], pairs)
    table.to_csv(REV / 'ci_august.csv')
    diffs.to_csv(REV / 'ci_august_differences.csv')
    REVIEW['bootstrap'] = {'draws': 1000, 'unit': 'sensor (cluster bootstrap)',
                           'holdout_sensors': int(holdout_test['device_name'].nunique()),
                           'august_sensors': int(second_rows['device_name'].nunique())}

# %%
# Comment 13: the month feature. Each model is refitted with its tuned settings twice
# by the same procedure, with month as is and with month set to a constant (which
# removes its information), on the hold-out, both cross-validated designs and August.
@guarded('month feature removed')
def _():
    def without_month(frame):
        frame = frame.copy()
        frame[MONTH_COLUMNS] = 0.0
        return frame

    rows = []
    designs = [('Chronological hold-out', validation_folds['Chronological hold-out'][0])]
    designs += [(setup, fold) for setup in ['Expanding-window CV', 'Leave-sensors-out']
                for fold in validation_folds[setup]]
    for setup, fold in designs:
        data = chrono_data if setup == 'Chronological hold-out' else prepare_fold(fold)
        actual = data['test'][target_column].astype(float).to_numpy()
        for name in NO_MONTH_MODELS:
            columns = columns_of(name)
            for variant, transform in [('with month', lambda f: f), ('without month', without_month)]:
                fitted = clone(tuned_estimators[name]).fit(transform(data['train'][columns]),
                                                           data['y_train_z'])
                predicted = (fitted.predict(transform(data['test'][columns]))
                             * data['target_std'] + data['target_mean'])
                rows.append({'setup': setup, 'fold': fold['label'], 'model': name, 'variant': variant,
                             **score_dict(actual, predicted)})
                if setup == 'Chronological hold-out':
                    august = (fitted.predict(transform(second_rows[columns]))
                              * data['target_std'] + data['target_mean'])
                    rows.append({'setup': 'August 2026', 'fold': 'all', 'model': name,
                                 'variant': variant, **score_dict(second_actual, august)})
    table = pd.DataFrame(rows)
    table.to_csv(REV / 'no_month_by_fold.csv', index=False)
    table.groupby(['setup', 'model', 'variant'])[['MAE', 'RMSE', 'R2']].mean() \
        .unstack('variant').to_csv(REV / 'no_month_summary.csv')

# %%
# Comment 10: rows where PM2.5 exceeded PM10 in the raw file.
@guarded('PM2.5 above PM10 rows')
def _():
    raw = pd.read_csv(data_file)
    raw['datetime'] = pd.to_datetime(raw['datetime'], format='ISO8601', errors='coerce', utc=True)
    both = (raw['pm2_5_calibrated_value'] > 0) & (raw['pm10_calibrated_value'] > 0)
    above = both & (raw['pm2_5_calibrated_value'] > raw['pm10_calibrated_value'])
    ratio = raw.loc[above, 'pm2_5_calibrated_value'] / raw.loc[above, 'pm10_calibrated_value']
    REVIEW['pm25_above_pm10'] = {
        'rows_with_both': int(both.sum()), 'rows_above': int(above.sum()),
        'share_of_rows_with_both': float(above.sum() / both.sum()),
        'share_of_all_rows': float(above.mean()),
        'by_network': raw.loc[above, 'network'].value_counts().to_dict(),
        'rows_by_network': raw['network'].value_counts().to_dict(),
        'sensors_affected': int(raw.loc[above, 'device_name'].nunique()),
        'ratio_median': float(ratio.median()), 'ratio_p90': float(ratio.quantile(0.9)),
        'excess_median_ug_m3': float((raw.loc[above, 'pm2_5_calibrated_value']
                                      - raw.loc[above, 'pm10_calibrated_value']).median()),
    }
    keys = set(zip(raw.loc[above, 'device_name'].astype(str), raw.loc[above, 'datetime'].dt.floor('h')))

    def flagged(frame):
        return np.array([(str(d), t) in keys for d, t in
                         zip(frame['device_name'].astype(str), frame['datetime'])])

    train_flag = flagged(chrono_data['train'])
    test_flag = flagged(holdout_test)
    REVIEW['pm25_above_pm10'].update({
        'holdout_train_rows_flagged': int(train_flag.sum()),
        'holdout_train_rows': int(len(train_flag)),
        'holdout_test_rows_flagged': int(test_flag.sum()),
        'holdout_test_rows': int(len(test_flag))})
    rows = []
    # (a) the trained models, scored with and without the flagged test rows
    keep = ~test_flag
    predictions = dict(chrono_predictions)
    predictions[PERSIST] = holdout_persist
    for name, predicted in predictions.items():
        predicted = np.asarray(predicted, float)
        rows.append({'training': 'all rows', 'test': 'all rows', 'model': name,
                     **score_dict(holdout_actual, predicted)})
        rows.append({'training': 'all rows', 'test': 'flagged rows excluded', 'model': name,
                     **score_dict(holdout_actual[keep], predicted[keep])})
    # (b) key models retrained without the flagged training rows
    train = chrono_data['train'][~train_flag]
    mean = float(train[target_column].mean())
    std = float(train[target_column].std())
    y_z = (train[target_column].astype(float) - mean) / std
    retrained = {BASELINE_NAME: np.full(len(holdout_actual), mean)}
    for name in NO_MONTH_MODELS:
        columns = columns_of(name)
        fitted = clone(tuned_estimators[name]).fit(train[columns], y_z)
        retrained[name] = fitted.predict(holdout_test[columns]) * std + mean
        august = fitted.predict(second_rows[columns]) * std + mean
        rows.append({'training': 'flagged rows excluded', 'test': 'August 2026', 'model': name,
                     **score_dict(second_actual, august)})
    for name, predicted in retrained.items():
        rows.append({'training': 'flagged rows excluded', 'test': 'all rows', 'model': name,
                     **score_dict(holdout_actual, predicted)})
        rows.append({'training': 'flagged rows excluded', 'test': 'flagged rows excluded',
                     'model': name, **score_dict(holdout_actual[keep], predicted[keep])})
    pd.DataFrame(rows).to_csv(REV / 'pm25_above_pm10_check.csv', index=False)

# %%
# Comment 12: were the replaced extreme readings real pollution episodes?
@guarded('extreme readings: episode check')
def _():
    frame = clean_data[['device_name', 'datetime', 'pm2_5_original', 'pm25_is_extreme']].copy()
    frame['hour'] = frame['datetime'].dt.floor('h')
    frame = frame.dropna(subset=['pm2_5_original'])
    extremes = frame[frame['pm25_is_extreme']]
    per_hour = frame.groupby('hour')['pm25_is_extreme'].sum()
    others = extremes['hour'].map(per_hour) - 1
    network_median = frame.groupby('hour')['pm2_5_original'].median()
    high_hours = network_median[network_median > network_median.quantile(0.9)].index
    # run length of consecutive extreme hours at one sensor
    runs = []
    for _, rows in extremes.sort_values('hour').groupby('device_name'):
        hours = rows['hour'].to_numpy()
        length = 1
        for i in range(1, len(hours) + 1):
            if i < len(hours) and hours[i] - hours[i - 1] == np.timedelta64(1, 'h'):
                length += 1
            else:
                runs.append(length)
                length = 1
    runs = np.array(runs)
    REVIEW['extremes_episode_check'] = {
        'extreme_readings': int(len(extremes)),
        'share_with_no_other_sensor_extreme_same_hour': float((others == 0).mean()),
        'share_with_3plus_other_sensors_extreme_same_hour': float((others >= 3).mean()),
        'share_in_top10pct_network_median_hours': float(extremes['hour'].isin(high_hours).mean()),
        'runs': int(len(runs)), 'runs_single_hour': int((runs == 1).sum()),
        'runs_3h_or_longer': int((runs >= 3).sum()), 'longest_run_h': int(runs.max()),
    }

# %%
# Comment 12: the same extreme-value rule applied to the August file, scored both ways.
@guarded('outlier rule on August')
def _():
    august = second_rows.drop(columns=PM25_HISTORY_COLUMNS).copy()
    values = august['pm2_5_calibrated_value'].astype(float)
    quartiles = values.groupby(august['device_name']).quantile([0.25, 0.75]).unstack()
    limit = quartiles[0.75] + EXTREME_IQR_MULTIPLIER * (quartiles[0.75] - quartiles[0.25])
    extreme = values > august['device_name'].map(limit).astype(float)
    cleaned = values.copy()
    for device in august.loc[extreme, 'device_name'].unique():
        rows = august[august['device_name'] == device]
        normal = rows.loc[~extreme.loc[rows.index], ['datetime']].assign(
            replacement=values.loc[rows.index][~extreme.loc[rows.index]]).sort_values('datetime')
        target = rows.loc[extreme.loc[rows.index], ['datetime']].sort_values('datetime')
        matched = pd.merge_asof(target.reset_index(), normal, on='datetime', direction='nearest',
                                tolerance=pd.Timedelta(hours=EXTREME_MAX_HOURS)).set_index('index')
        cleaned.loc[matched.index] = matched['replacement'].fillna(normal['replacement'].median())
    august['pm2_5_calibrated_value'] = cleaned
    august = add_pm25_history(august)
    actual_clean = cleaned.to_numpy()
    rows = []
    persist_clean, _ = persistence(august, target_scaler_mean)
    predictions = {BASELINE_NAME: np.full(len(august), target_scaler_mean), PERSIST: persist_clean}
    for name, result in model_results.items():
        predictions[name] = np.asarray(from_zscore(result['pipeline'].predict(august[columns_of(name)])))
    for name, predicted in predictions.items():
        rows.append({'target': 'extremes replaced (as training)', 'model': name,
                     **score_dict(actual_clean, predicted)})
        if name in second_predictions or name == PERSIST:
            raw_pred = august_persist if name == PERSIST else second_predictions[name]
            rows.append({'target': 'untouched readings (as in paper)', 'model': name,
                         **score_dict(second_actual, raw_pred)})
    pd.DataFrame(rows).to_csv(REV / 'august_outlier_rule.csv', index=False)
    REVIEW['august_extremes'] = {'readings': int(len(values)), 'extreme': int(extreme.sum()),
                                 'sensors': int(august.loc[extreme, 'device_name'].nunique()),
                                 'max_before': float(values.max()), 'max_after': float(cleaned.max())}

# %%
# Comment 20: per-group MAE in August (data class, seen or new sensor), with persistence.
@guarded('August per-group MAE')
def _():
    classes = second_rows['device_name'].map(second_offline_table['data_class']).to_numpy()
    seen = second_rows['device_name'].isin(sequence_devices).to_numpy()
    models = {BASELINE_NAME: second_predictions[BASELINE_NAME], PERSIST: august_persist,
              best_model_name: second_predictions[best_model_name],
              best_history_name: second_predictions[best_history_name],
              'LSTM (weather + time + PM2.5 history)':
                  second_predictions['LSTM (weather + time + PM2.5 history)']}
    rows = []
    for label, groups in [('data class', classes),
                          ('sensor', np.where(seen, 'seen in training', 'new'))]:
        for group in pd.unique(groups):
            mask = groups == group
            for name, predicted in models.items():
                rows.append({'grouping': label, 'group': group, 'model': name,
                             'rows': int(mask.sum()),
                             'sensors': int(second_rows.loc[mask, 'device_name'].nunique()),
                             'mean_actual': float(second_actual[mask].mean()),
                             **score_dict(second_actual[mask], np.asarray(predicted)[mask])})
    pd.DataFrame(rows).to_csv(REV / 'august_per_group.csv', index=False)

# %%
# Comment 14: hyperparameters, search spaces, LSTM and BRITS settings, seeds, SMOTE.
@guarded('hyperparameters and settings')
def _():
    def plain(value):
        if isinstance(value, (bool, int, float, str)) or value is None:
            return value
        if isinstance(value, (np.integer, np.floating)):
            return value.item()
        if isinstance(value, (list, tuple)):
            return [plain(v) for v in value]
        if isinstance(value, dict):
            return {str(k): plain(v) for k, v in value.items()}
        return str(value)

    def final_step(estimator):
        estimator = getattr(estimator, 'best_estimator_', estimator)
        return estimator.steps[-1][1] if hasattr(estimator, 'steps') else estimator

    settings = {'random_seed': RANDOM_SEED, 'models': {}, 'searches': {}, 'constants': {}}
    for name, result in model_results.items():
        step = final_step(result['tuned_estimator'])
        settings['models'][name] = {'class': type(step).__name__,
                                    'params': plain(step.get_params())}
    for name, value in list(globals().items()):
        if hasattr(value, 'best_params_') and hasattr(value, 'cv'):
            settings['searches'][name] = {
                'best_params': plain(value.best_params_),
                'space': plain(getattr(value, 'param_grid', None) or
                               getattr(value, 'param_distributions', None)),
                'cv': str(value.cv), 'n_iter': plain(getattr(value, 'n_iter', None)),
                'scoring': plain(value.scoring)}
        if name.isupper() and isinstance(value, (bool, int, float, str, list, tuple)) \
                and name.split('_')[0] in {'LSTM', 'BRITS', 'SMOTE', 'EXTREME', 'GAP', 'TS', 'SPATIAL',
                                           'MIN', 'INTERPOLATION', 'SHAP', 'DATA', 'USE', 'PM25'}:
            settings['constants'][name] = plain(value)
    for table in ['smote_cv_table', 'smote_ablation']:
        if table in globals():
            globals()[table].to_csv(REV / f'{table}.csv')
    (REV / 'hyperparameters.json').write_text(json.dumps(settings, indent=1))

# %%
# Comment 19: imputation tables (all gap lengths, one row per method) and downstream MAE.
@guarded('imputation tables')
def _():
    for metric in ['MAE', 'RMSE']:
        gap_test_table(gap_test, metric).to_csv(REV / f'imputation_{metric.lower()}_by_gap.csv')
    gap_test_table(gap_test, 'filled_pct').to_csv(REV / 'imputation_filled_pct_by_gap.csv')
    downstream_summary.to_csv(REV / 'downstream_by_model_design_imputer.csv')
    downstream_scores.to_csv(REV / 'downstream_by_fold.csv', index=False)

# %%
# Comments 16 and 18: data for the new figures (EDA time series and observed vs predicted).
@guarded('figure data')
def _():
    columns = ['device_name', 'site_name', 'datetime', 'temperature', 'humidity',
               'pm2_5_original', 'pm2_5_calibrated_value']
    counts = clean_data.groupby('device_name')['pm2_5_original'].count().sort_values(ascending=False)
    pick = list(dict.fromkeys(list(case_sensors) + counts.index[:6].tolist()))
    clean_data.loc[clean_data['device_name'].isin(pick),
                   [c for c in columns if c in clean_data.columns]].to_csv(REV / 'eda_sensor_series.csv',
                                                                           index=False)
    pd.Series(case_sensors, name='case_sensor').to_csv(REV / 'case_sensors.csv', index=False)
    sensor_offline_table.to_csv(REV / 'sensor_offline_table.csv')
    keep = [best_model_name, best_history_name, 'LightGBM + PM2.5 history',
            'LSTM (weather + time + PM2.5 history)']
    august = second_rows[['device_name', 'datetime']].copy()
    august['actual'] = second_actual
    august[PERSIST] = august_persist
    for name in dict.fromkeys(keep):
        august[name] = second_predictions[name]
    august.to_csv(REV / 'august_observed_predicted.csv', index=False)
    second_offline_table.to_csv(REV / 'august_offline_table.csv')
    holdout = holdout_test[['device_name', 'datetime']].copy()
    holdout['actual'] = holdout_actual
    holdout[PERSIST] = holdout_persist
    for name, predicted in chrono_predictions.items():
        holdout[name] = np.asarray(predicted, float)
    holdout.to_csv(REV / 'holdout_observed_predicted.csv', index=False)

# %%
# Comment 17: deployment numbers that come from the run itself.
@guarded('deployment facts')
def _():
    facts = {}
    for path in ['best_pm25_model.joblib', 'best_pm25_nowcast_model.joblib']:
        if p(path).exists():
            facts[path] = {'size_mb': round(p(path).stat().st_size / 1024 ** 2, 3)}
    if 'resource_report' in globals():
        facts['resource_report'] = json.loads(json.dumps(resource_report, default=str))
    REVIEW['deployment'] = facts

# %%
(REV / 'review_summary.json').write_text(json.dumps(REVIEW, indent=1, default=str))
print(open(REV / 'errors.txt').read() or 'No errors in the review extras.')
