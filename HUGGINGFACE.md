# Publishing on Hugging Face

Two repos, one folder each:

| Folder | Hugging Face repo | Contents |
| --- | --- | --- |
| `huggingface/model/` | [Kyalis/airqo-pm25-random-forest](https://huggingface.co/Kyalis/airqo-pm25-random-forest) (model) | The trained model, its model card and the inference script |
| `huggingface/space/` | [Kyalis/airqo-pm25-forecasts](https://huggingface.co/spaces/Kyalis/airqo-pm25-forecasts) (static Space) | A web page showing the August 2026 forecasts for all 149 sensors |

The page is static: it shows the forecasts saved in `forecasts.json` and does not run the model.

## Deploy

Run these from the project folder, after `train.ipynb` has run.

### 1. Prepare the folders

```bash
python huggingface/prepare.py
```

This writes `huggingface/space/forecasts.json` and copies `best_pm25_model.joblib` and `pm25_inference.py` into `huggingface/model/`.

### 2. Log in

Use a write token for the Kyalis account, from <https://huggingface.co/settings/tokens>:

```bash
hf auth login
```

### 3. Upload the model

```bash
hf repos create Kyalis/airqo-pm25-random-forest --type model
hf upload Kyalis/airqo-pm25-random-forest huggingface/model . --type model
```

### 4. Upload the page

```bash
python -c "from huggingface_hub import HfApi; HfApi().upload_folder(repo_id='Kyalis/airqo-pm25-forecasts', repo_type='space', folder_path='huggingface/space')"
```

Don't use `hf upload` for the Space: it first tries to create the repo as a Gradio Space, which Hugging Face refuses on a free account (`402 Payment Required`), even though this Space already exists and is static. `upload_folder` uploads to the existing Space directly.

The page is live straight away at <https://huggingface.co/spaces/Kyalis/airqo-pm25-forecasts>.

## After a new training run

Run step 1 again, then the upload commands from steps 3 and 4. `hf repos create` is only needed the first time.

The test scores (MAE, R², AQI accuracy) are written into `huggingface/model/README.md` and the bottom of `huggingface/space/index.html`. Update them by hand if a new run changes them.

## Preview the page locally

```bash
python -m http.server 8000 -d huggingface/space
```

Then open <http://localhost:8000>.
