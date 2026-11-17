"""Step 1 of the review reruns: check that a clean run of train.ipynb gives the paper's numbers.

Usage (on the Alienware, inside screen):
    ~/airqo_rerun/venv/bin/python reproduce.py ~/airqo_rerun/repo ~/airqo_rerun/run_repro [extra_cells.py]

With extra_cells.py, its blocks (separated by lines '# %%') run as cells after the notebook,
in the same kernel, so they can use every variable the notebook created.

What it does
  1. Copies the repo to a fresh work folder (the repo itself is never written to).
  2. Keeps the committed deployment_outputs/model_validation_comparison.csv as the reference.
  3. Executes train.ipynb top to bottom, as Jupyter would (inline plots, Evidently enabled).
  4. Compares the new model_validation_comparison.csv with the reference, model by model.

Exit code 0 = tree models, SVR, kNN, linear models and the mean baseline match within TOL.
The LSTMs are reported but only warned about, because TensorFlow can differ slightly between machines.
"""
import os
import shutil
import sys
import time
from pathlib import Path

import pandas as pd

TOL = 0.01          # allowed absolute difference in MAE, RMSE, R2 and AQI accuracy
TOL_LSTM = 0.25     # looser bound for the two LSTM rows (warn only)
CELL_TIMEOUT = 4 * 3600   # seconds allowed for one cell (the tuning cells are the slow ones)


def load(path):
    df = pd.read_csv(path, header=[0, 1], index_col=0)
    df.index.name = "model"
    return df.apply(pd.to_numeric, errors="coerce")


def main(repo, work, extras=None):
    repo, work = Path(repo).expanduser().resolve(), Path(work).expanduser().resolve()
    extras = Path(extras).expanduser().resolve() if extras else None
    if work.exists():
        sys.exit(f"{work} already exists; remove it or pick another folder.")
    shutil.copytree(repo, work, ignore=shutil.ignore_patterns(".git"))
    ref_csv = work / "reference_model_validation_comparison.csv"
    shutil.copy(work / "deployment_outputs" / "model_validation_comparison.csv", ref_csv)

    # Do not set MPLBACKEND: the kernel's inline backend closes each figure after its cell,
    # as in Jupyter. With Agg, figures leak between cells and the SHAP cells fail (first attempt).
    # Evidently stays enabled so the drift figures quoted in the paper are reproduced too.
    os.environ.pop("MPLBACKEND", None)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    os.chdir(work)

    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read("train.ipynb", as_version=4)
    if extras:   # extra analysis cells appended after the notebook, split on lines "# %%"
        for block in Path(extras).read_text(encoding="utf-8").split("\n# %%"):
            if block.strip():
                nb.cells.append(nbformat.v4.new_code_cell(block.strip()))
    start = time.time()
    client = NotebookClient(nb, timeout=CELL_TIMEOUT, kernel_name="python3",
                            resources={"metadata": {"path": str(work)}}, allow_errors=False)
    try:
        client.execute()
    finally:
        nbformat.write(nb, work / "train_executed.ipynb")   # keep whatever ran, even on failure
    print(f"Notebook finished in {(time.time() - start) / 60:.1f} minutes.")

    new = load(work / "deployment_outputs" / "model_validation_comparison.csv")
    ref = load(ref_csv)
    only_one = set(new.index) ^ set(ref.index)
    if only_one:
        print("Models present in only one table:", sorted(only_one))
    common = [m for m in ref.index if m in new.index]
    diff = (new.loc[common] - ref.loc[common]).abs()
    worst = diff.max(axis=1)
    report = pd.DataFrame({"max_abs_diff": worst.round(4),
                           "holdout_MAE_new": new.loc[common].iloc[:, 0].round(4),
                           "holdout_MAE_ref": ref.loc[common].iloc[:, 0].round(4)})
    report.to_csv(work / "reproduction_report.csv")
    print(report.to_string())

    failed = [m for m in common if worst[m] > (TOL_LSTM if "LSTM" in m else TOL)
              and "LSTM" not in m]
    lstm_warn = [m for m in common if "LSTM" in m and worst[m] > TOL]
    for m in lstm_warn:
        print(f"WARNING: {m} differs by {worst[m]:.4f} (LSTM, not a failure)")
    if failed or only_one - {m for m in only_one if "LSTM" in m}:
        print("REPRODUCTION FAILED for:", failed or sorted(only_one))
        sys.exit(1)
    print("REPRODUCTION OK: all non-LSTM models match the committed table within", TOL)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(*sys.argv[1:4])
