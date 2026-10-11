"""Draw the monitoring figures of the report from the Evidently outputs.

Run from the project root after train.ipynb has been executed:

    python report/make_monitoring_figures.py

Reads evidently_data_drift_report.json, evidently_monitoring_summary.csv and
the drift table of the second dataset stored in train.ipynb, and writes three
PNG files to report/figures/.
"""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / 'report' / 'figures'
DRIFTED, STABLE, INK, MUTED = '#eb6834', '#2a78d6', '#0b0b0b', '#52514e'


def drift_scores_from_json(path):
    """Column, method and drift score of every ValueDrift metric."""
    rows = []
    for metric in json.loads(Path(path).read_text())['metrics']:
        if metric['metric_name'].startswith('ValueDrift'):
            rows.append({'column': metric['config']['column'],
                         'method': metric['config']['method'],
                         'drift_value': float(metric['value']),
                         'threshold': metric['config']['threshold']})
    return pd.DataFrame(rows)


def second_dataset_drift_scores(notebook_path):
    """The drift table of the second dataset, read from the executed notebook."""
    notebook = json.loads(Path(notebook_path).read_text(encoding='utf-8'))
    pattern = re.compile(r'^\s*\d+\s+(\S+)\s+(.+?)\s+(\d+\.\d+)\s+(\d+\.\d+)')
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code' or 'second_drift_summary' not in ''.join(cell['source']):
            continue
        for output in cell.get('outputs', []):
            text = ''.join(output.get('data', {}).get('text/plain', ''))
            rows = [pattern.match(line) for line in text.splitlines()]
            rows = [match.groups() for match in rows if match]
            if rows:
                table = pd.DataFrame(rows, columns=['column', 'method', 'drift_value', 'threshold'])
                return table.astype({'drift_value': float, 'threshold': float})
    return None


def plot_drift_scores(scores, title, file_name):
    scores = scores.sort_values('drift_value')
    threshold = float(scores['threshold'].iloc[0])
    colors = [DRIFTED if value >= threshold else STABLE for value in scores['drift_value']]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.barh(scores['column'], scores['drift_value'], color=colors, height=0.6)
    for y, value in enumerate(scores['drift_value']):
        ax.text(value + 0.02, y, f'{value:.2f}', va='center', fontsize=9, color=INK)
    ax.axvline(threshold, color=MUTED, linestyle='--', linewidth=1.2)
    ax.text(threshold + 0.01, -0.75, f'drift threshold {threshold:g}', color=MUTED, fontsize=9)
    ax.set_xlabel('Drift score (normed Wasserstein or Jensen-Shannon distance)')
    ax.set_ylabel('Input feature')
    ax.set_title(title)
    ax.set_xlim(0, scores['drift_value'].max() * 1.15)
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=DRIFTED, label='Drift detected'),
                       plt.Rectangle((0, 0), 1, 1, color=STABLE, label='No drift')],
              frameon=False, loc='lower right')
    ax.grid(axis='x', alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / file_name, dpi=150)
    plt.close(fig)


def plot_model_drift(summary, file_name):
    """Reference (training) against current (test) period: MAE, RMSE and R2."""
    metrics = {'Model MAE': 'MAE (µg/m³)', 'Model RMSE': 'RMSE (µg/m³)', 'Model R2': 'R²'}
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2))
    for ax, (component, label) in zip(axes, metrics.items()):
        row = summary[summary['monitoring_component'] == component].iloc[0]
        values = [float(row['reference_value']), float(row['current_value'])]
        bars = ax.bar(['Reference\n(training)', 'Current\n(test)'], values,
                      color=[STABLE, DRIFTED], width=0.55)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value, f'{value:.2f}',
                    ha='center', va='bottom', fontsize=10, color=INK)
        ax.set_title(label)
        ax.set_ylabel(label)
        ax.set_ylim(0, max(values) * 1.18)
        ax.grid(axis='y', alpha=0.25)
    fig.suptitle('Model drift: selected forecast model on the reference and current periods')
    fig.tight_layout()
    fig.savefig(FIGURES / file_name, dpi=150)
    plt.close(fig)


if __name__ == '__main__':
    plot_drift_scores(
        drift_scores_from_json(ROOT / 'evidently_data_drift_report.json'),
        'Data drift: training period against test period (Evidently)',
        'monitoring_drift_scores.png')
    plot_model_drift(pd.read_csv(ROOT / 'evidently_monitoring_summary.csv'),
                     'monitoring_model_drift.png')
    second = second_dataset_drift_scores(ROOT / 'train.ipynb')
    if second is not None:
        plot_drift_scores(
            second, 'Data drift: training data against the August dataset (Evidently)',
            'monitoring_second_dataset_drift.png')
    print('monitoring figures written to', FIGURES)
