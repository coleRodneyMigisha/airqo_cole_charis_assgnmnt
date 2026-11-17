"""Build Table (results) for both papers from reruns/results/*.csv. Standard library only.
Usage: python -I build_results_table.py  (from research_paper_draft3/reruns)
Prints the @TABLE block for manuscript_source.txt and writes results/table_results.tex."""
import csv
from collections import defaultdict

long = defaultdict(dict)
for r in csv.DictReader(open('results/full_comparison_long.csv')):
    long[r['model']][r['setup']] = {k: float(r[k]) for k in ('MAE', 'RMSE', 'R2')}
ci = {}
for name in ('holdout', 'august'):
    for r in csv.DictReader(open(f'results/ci_{name}.csv')):
        ci[(name, r[''])] = (float(r['MAE_lo']), float(r['MAE_hi']))

H, CV, LSO, AUG = 'Chronological hold-out', 'Expanding-window CV', 'Leave-sensors-out', 'August 2026'
groups = [
    ('Baselines', [('Training mean', 'Baseline (training mean)'), ('Persistence (last reading)', 'Persistence (last reading)')]),
    ('Forecast models (weather, time, sensor)', [
        ('SVR, tuned', 'SVR (tuned)'), ('Random forest, untuned', 'Random Forest (untuned baseline)'),
        ('Random forest, tuned', 'Random Forest (tuned)'), ('LightGBM, tuned', 'LightGBM (tuned)'),
        ('KNN, tuned', 'KNN (tuned)'), ('LSTM, weather and time', 'LSTM (weather + time)'),
        ('Ridge regression, tuned', 'Ridge Regression (tuned)'), ('Linear regression', 'Linear Regression (tuned)'),
        ('Polynomial regression', 'Polynomial Regression (tuned)')]),
    ('Nowcast models (with PM2.5 history)', [
        ('Random forest + history', 'Random Forest + PM2.5 history'),
        ('LightGBM + history', 'LightGBM + PM2.5 history'),
        ('LSTM + history', 'LSTM (weather + time + PM2.5 history)')]),
]
cols = [(H, 'MAE', 'holdout'), (H, 'RMSE', None), (H, 'R2', None), (CV, 'MAE', None), (CV, 'R2', None),
        (LSO, 'MAE', None), (LSO, 'R2', None), (AUG, 'MAE', 'august'), (AUG, 'RMSE', None), (AUG, 'R2', None)]
models = [m for _, rows in groups for _, m in rows]
best = {}
for setup, metric, _ in cols:
    values = {m: long[m][setup][metric] for m in models}
    best[(setup, metric)] = (max if metric == 'R2' else min)(values, key=values.get)


def cell(m, setup, metric, ci_key, tex):
    v = long[m][setup][metric]
    text = f'{v:.2f}'.replace('-', '$-$' if tex else '-')
    if best[(setup, metric)] == m:
        text = f'\\textbf{{{text}}}' if tex else f'**{text}**'
    if ci_key:
        lo, hi = ci[(ci_key, m)]
        text += (f' {{\\scriptsize[{lo:.1f}, {hi:.1f}]}}' if tex else f' [{lo:.1f}, {hi:.1f}]')
    return text


# txt (docx) version
lines = ['@TABLE 11', '@TR Model|Hold-out MAE [95% CI]|Hold-out RMSE|Hold-out R²|CV MAE|CV R²|LSO MAE|LSO R²|August MAE [95% CI]|August RMSE|August R²']
for label, rows in groups:
    lines.append(f'@TR {label}||||||||||')
    for name, m in rows:
        lines.append('@TR ' + name + '|' + '|'.join(cell(m, s, k, c, False) for s, k, c in cols))
lines.append('@ENDTABLE')
print('\n'.join(lines))
# tex version
tex = ['\\begin{tabular}{l' + 'c' * 10 + '}', '\\toprule',
       ' & \\multicolumn{3}{c}{Hold-out (2--3 June)} & \\multicolumn{2}{c}{Expanding-window CV} & '
       '\\multicolumn{2}{c}{Leave-sensors-out} & \\multicolumn{3}{c}{August 2026 (new month)} \\\\',
       '\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}\\cmidrule(lr){7-8}\\cmidrule(lr){9-11}',
       'Model & MAE$\\downarrow$ [95\\% CI] & RMSE$\\downarrow$ & $R^2\\uparrow$ & MAE$\\downarrow$ & $R^2\\uparrow$ & '
       'MAE$\\downarrow$ & $R^2\\uparrow$ & MAE$\\downarrow$ [95\\% CI] & RMSE$\\downarrow$ & $R^2\\uparrow$ \\\\', '\\midrule']
for gi, (label, rows) in enumerate(groups):
    if gi:
        tex.append('\\midrule')
    tex.append(f'\\multicolumn{{11}}{{l}}{{\\textit{{{label}}}}} \\\\')
    for name, m in rows:
        tex.append(name + ' & ' + ' & '.join(cell(m, s, k, c, True) for s, k, c in cols) + ' \\\\')
tex += ['\\bottomrule', '\\end{tabular}']
open('results/table_results.tex', 'w').write('\n'.join(tex) + '\n')
