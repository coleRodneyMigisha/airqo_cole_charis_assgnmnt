"""Figure 1 for Draft 1: MAE of five models under four evaluation settings.

Hold-out, expanding-window CV and leave-sensors-out MAE are read from
deployment_outputs/model_validation_comparison.csv. The August 2026 MAE values
are copied from the stored output of train.ipynb cell 537 (no retraining, no
re-execution). Greyscale with hatching because IST-Africa prints in black and white.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root = Path(sys.argv[1])
out = Path(sys.argv[2])

csv = pd.read_csv(root / "deployment_outputs" / "model_validation_comparison.csv", header=[0, 1], index_col=0)
csv = csv[csv.index.notna() & (csv.index != "model")]  # drop the empty "model" row if present

models = {
    "Baseline (training mean)": "Mean baseline",
    "SVR (tuned)": "SVR (forecast)",
    "LightGBM (tuned)": "LightGBM",
    "Random Forest + PM2.5 history": "RF + history",
    "LightGBM + PM2.5 history": "LightGBM + history",
}
august = {  # train.ipynb cell 537, "second dataset (Aug 2026)" MAE
    "Baseline (training mean)": 19.206,
    "SVR (tuned)": 18.323,
    "LightGBM (tuned)": 18.785,
    "Random Forest + PM2.5 history": 13.701,
    "LightGBM + PM2.5 history": 14.019,
}
settings = [
    ("Chronological hold-out", "Hold-out\n(2-3 June)"),
    ("Expanding-window CV", "Expanding-window\nCV"),
    ("Leave-sensors-out", "Leave-sensors-out"),
    ("August", "August 2026\n(new month)"),
]

values = []
for key in models:
    row = [float(csv.loc[key, (s, "MAE")]) for s, _ in settings[:3]] + [august[key]]
    values.append(row)
values = np.array(values)

plt.rcParams.update({"font.family": "Times New Roman", "font.size": 11})
fig, ax = plt.subplots(figsize=(6.5, 3.4), dpi=300)
greys = ["white", "0.85", "0.6", "0.35", "0.1"]
hatches = ["///", "", "..", "", ""]
width = 0.16
x = np.arange(len(settings))
for i, (key, label) in enumerate(models.items()):
    ax.bar(x + (i - 2) * width, values[i], width, label=label, color=greys[i],
           edgecolor="black", linewidth=0.6, hatch=hatches[i])
ax.set_xticks(x)
ax.set_xticklabels([lab for _, lab in settings])
ax.set_ylabel("MAE (µg/m³)")
ax.set_ylim(0, 30)
ax.yaxis.grid(True, color="0.8", linewidth=0.5)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.legend(ncol=3, fontsize=9, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.2))
fig.tight_layout()
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor="white")
print(pd.DataFrame(values, index=list(models.values()), columns=[s for s, _ in settings]).round(2))
