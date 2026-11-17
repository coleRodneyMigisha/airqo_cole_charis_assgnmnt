"""Turn review_extras outputs into small CSV files that pgfplots draws in main.tex.

Usage: python make_figure_data.py <review_extras dir> <output dir>

fig_eda_<k>.csv      (k = 1..4) PM2.5 of four sensors over the 147 network-active hours,
                     NaN where the sensor was offline (pgfplots: unbounded coords=jump).
fig_eda_meta.csv     sensor id, site, data class, offline share, panel title.
fig_eda_bursts.csv   hour index where each observation burst starts, and its label.
fig_obspred_<k>.csv  (k = 1..2) one August week for two sensors: observed, SVR,
                     persistence and LightGBM with PM2.5 history.
fig_obspred_meta.csv sensor id, data class, week shown.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

# ---- EDA: four sensors (the notebook's case-study sensors: one data-rich, three data-poor)
series = pd.read_csv(src / 'eda_sensor_series.csv', parse_dates=['datetime'])
offline = pd.read_csv(src / 'sensor_offline_table.csv', index_col=0)
case = pd.read_csv(src / 'case_sensors.csv')['case_sensor'].tolist()
hours = np.sort(series['datetime'].dt.floor('h').unique())
# network-active hours come from the full table of the chosen sensors; use the union of all
# hours in the file, which holds the case sensors and the six most complete sensors.
index_of = {h: i for i, h in enumerate(hours)}
bursts, labels = [0], []
for i in range(1, len(hours)):
    if (hours[i] - hours[i - 1]) > np.timedelta64(1, 'D'):
        bursts.append(i)
for start in bursts:
    labels.append(pd.Timestamp(hours[start]).strftime('%-d %b'))
pd.DataFrame({'start': bursts, 'label': labels}).to_csv(out / 'fig_eda_bursts.csv', index=False)

meta = []
for k, device in enumerate(case[:4], start=1):
    rows = series[series['device_name'] == device].copy()
    rows['h'] = rows['datetime'].dt.floor('h').map(index_of)
    full = pd.DataFrame({'h': np.arange(len(hours))})
    full = full.merge(rows[['h', 'pm2_5_calibrated_value', 'pm2_5_original']], on='h', how='left')
    full.rename(columns={'pm2_5_calibrated_value': 'pm25', 'pm2_5_original': 'pm25_raw'}) \
        .to_csv(out / f'fig_eda_{k}.csv', index=False, na_rep='nan')
    info = offline.loc[device] if device in offline.index else {}
    site = rows['site_name'].dropna().iloc[0] if 'site_name' in rows and rows['site_name'].notna().any() else ''
    meta.append({'panel': k, 'device': device, 'site': site,
                 'data_class': info.get('data_class', ''),
                 'offline_pct': round(float(info.get('offline_pct_active_hours', np.nan)), 1),
                 'readings': int(rows['pm2_5_calibrated_value'].notna().sum())})
pd.DataFrame(meta).to_csv(out / 'fig_eda_meta.csv', index=False)

# ---- Observed against predicted, August: one data-rich sensor and one other, the week with the
# sensor's highest reading, so the missed peaks are visible.
aug = pd.read_csv(src / 'august_observed_predicted.csv', parse_dates=['datetime'])
aug_offline = pd.read_csv(src / 'august_offline_table.csv', index_col=0)
seen_rich = aug_offline[(aug_offline['data_class'] == 'data-rich') & aug_offline['in_main_dataset']]
counts = aug.groupby('device_name')['actual'].count()
first = counts.reindex(seen_rich.index).idxmax()
others = aug_offline[(aug_offline['data_class'] != 'data-rich') & aug_offline['in_main_dataset']]
second = counts.reindex(others.index).dropna().idxmax() if len(others) else counts.drop(first).idxmax()
columns = {'actual': 'obs', 'Persistence (last reading)': 'persist', 'SVR (tuned)': 'svr',
           'LightGBM + PM2.5 history': 'lgbh'}
meta = []
for k, device in enumerate([first, second], start=1):
    rows = aug[aug['device_name'] == device].sort_values('datetime')
    peak = rows.loc[rows['actual'].idxmax(), 'datetime']
    start = max(rows['datetime'].min(), (peak - pd.Timedelta(days=3)).floor('D'))
    end = start + pd.Timedelta(days=7)
    week = rows[(rows['datetime'] >= start) & (rows['datetime'] < end)]
    grid = pd.DataFrame({'datetime': pd.date_range(start, end, freq='h', inclusive='left')})
    week = grid.merge(week, on='datetime', how='left')
    week['day'] = (week['datetime'] - start) / pd.Timedelta(days=1)
    week[['day'] + list(columns)].rename(columns=columns) \
        .to_csv(out / f'fig_obspred_{k}.csv', index=False, na_rep='nan', float_format='%.3f')
    meta.append({'panel': k, 'device': device, 'data_class': aug_offline.loc[device, 'data_class'],
                 'offline_pct': round(float(aug_offline.loc[device, 'offline_pct_active_hours']), 1),
                 'start': start.strftime('%Y-%m-%d'), 'end': (end - pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
                 'peak': round(float(rows['actual'].max()), 1),
                 'mae_svr_week': round(float((week['SVR (tuned)'] - week['actual']).abs().mean()), 2),
                 'mae_lgbh_week': round(float((week['LightGBM + PM2.5 history'] - week['actual']).abs().mean()), 2),
                 'mae_persist_week': round(float((week['Persistence (last reading)'] - week['actual']).abs().mean()), 2)})
pd.DataFrame(meta).to_csv(out / 'fig_obspred_meta.csv', index=False)
print(pd.read_csv(out / 'fig_eda_meta.csv').to_string())
print(pd.read_csv(out / 'fig_obspred_meta.csv').to_string())
