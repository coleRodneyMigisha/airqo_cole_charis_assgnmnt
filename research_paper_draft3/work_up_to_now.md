# Work up to now: AirQo PM2.5 project

Compiled 15 Nov 2026 from the repository's full git history (all local and remote branches, including `origin/main` at `ffc65ea`) and the files as they stand. This is the record Draft 3 of the IST-Africa paper was built from. AI (Claude, through Claude Code) compiled it; the work, findings and decisions it describes are Cole's and Charis's, as the commits show.

## 1. Where the project stands

What can two students build from a sensor file that, on inspection, holds only eight days of readings? This repository answers that. Cole Rodney Migisha and Charis Opol built an hourly PM2.5 prediction pipeline on 14,600 AirQo sensor records for CSC3119 Assignment 4, rebuilt it after their presentation feedback showed that the first model's accuracy came from PM10, deployed the forecast model as a Render API with a Vercel dashboard, and wrote it up as an IEEE Access–style report. Their lecturer then asked them to submit the work to a conference, and the project is now a paper for IST-Africa 2027, due **20 November 2026**. The history runs from 16 Sep to 9 Nov 2026: 60 non-merge commits on the collected branches plus one newer commit on `origin/main` (`ffc65ea`), 30 merge commits and 17 pull requests, by two contributors. The most important open issue is the paper's AI declaration and the GenAI rule (AQ15): the text of Drafts 1–3 was compiled by AI from the authors' own work, so both authors must revise it in their own words before submission.

## 2. How we got here

### Phase 1: Setup, cleaning and first EDA (16–24 Sep 2026)

Cole opened the repository with the assignment brief and the raw sensor file (`c7f8db8`), then started `train.ipynb` (`65f0c52`, `c69dad0`). On 23 Sep Charis worked through the cleaning in seven commits: standard data types with zeros first left in place (`4a36d95`), coordinate imputation (`2b7eb86`), resampling each sensor to an hourly grid with an offline flag (`f1b0bfd`), linear and KNN imputation (`d6743db`), choosing the EDA sites (`37a83bc`), distributions (`a520d5d`) and time series compared with the original data (`32edd3e`). That last comparison is where the KNN long-gap fill was caught copying the same few readings into every matching hour. Cole finished the EDA and started training overnight (`6230cdc`).

Key commits: `c7f8db8` data and brief; `f1b0bfd` hourly grid; `d6743db` KNN imputation; `32edd3e` the evidence that led to reversing it.

### Phase 2: First modelling pipeline, with PM10 (24–28 Sep 2026)

Cole fixed dependency breakage (`8c57db0`, `aed4ec3`) and trained the first models (`eea1138`). Charis completed training and committed the first `best_pm25_model.joblib` (`afd5f6b`), then the predictions (`5964c6b`), and asked Cole to check them in PR #2 ("Hey Cole, help check this out"). Cole added the standalone inference script `pm25_inference.py`, the first Evidently drift reports, the August 1–14 forecasts and the Jakarta CNN-LSTM paper (`2b04c2b`), then documented the notebook (`99e027b`).

Key commits: `afd5f6b` first saved model; `2b04c2b` inference, monitoring and forecasts.

### Phase 3: Merging the notebook and fixing its outputs (4 Oct 2026)

Cole updated the Evidently section and retrained (`378ad79`). Charis merged both versions into a final notebook (`ca0bd59`, PR #3), re-ran it end to end with Evidently 0.7.23 so that every report matched the selected tuned random forest, test MAE 3.103 µg/m³ (`f83e9a3`), and stopped tracking the model file because it had grown to about 120 MB (`8fbffd6`).

### Phase 4: First deployment and report (10 Oct 2026)

Charis added the deployment work in one large commit (`b138bdb`): `serve_model.py`, `DEPLOYMENT.md`, `HUGGINGFACE.md` with the Hugging Face model card and static Space, the run logs, and the first LaTeX report with its figures. This snapshot is still the Phase 1 pipeline with PM10. An earlier copy of the same commit, `245c2e2`, survives on the `backup-pre-trailer-*` branches, and earlier drafts cite that copy as "the Phase 1 notebook".

### Phase 5: The rebuild after feedback (11–12 Oct 2026)

The presentation feedback changed the project. The commit `83a7e43`, "Changes to the work from the feedback of the presentation", rebuilt the notebook without PM10 (35,351 changed lines in `train.ipynb`): extreme-value replacement, three imputers including a BRITS-style bidirectional LSTM, PM2.5-history nowcast models, three validation designs, SHAP, maps, the first August test file and `report/pipeline_update_notes.md`. The same evening Charis untracked the model file again after the merge (`2006484`, `2051102`) and applied the lecturer's feedback with a slim `requirements-render.txt` for the server (`35d1c12`). Overnight came the full August file (73,274 rows) with the rewritten report and its PDF (`94f40bb`), then a retraining run that added the imputation-effect figures and slides (`16f7c62`).

Around these commits the history was rewritten: the `backup-pre-trailer-main` and `backup-pre-trailer-charis` branches hold the earlier versions, whose only difference is that two 4 Oct commits carried a `Co-Authored-By: Claude` trailer (`1c5625e`, `3fdcd6a`, now `f83e9a3` and `8fbffd6`). This is why commits from 24 Sep to 12 Oct appear twice with identical content (the pairs are listed in Section 6).

Key commits: `83a7e43` the rebuild; `35d1c12` lecturer feedback; `94f40bb` August data and report; `16f7c62` retraining and the imputation decision.

### Phase 6: Report, abstract and serving (15–22 Oct 2026)

Charis finished the report and a one-page abstract (`2e576c7`, `7674654`), moved the report to the IEEE Access template and added a paper template (`cce9a1a`), rewrote `serve_model.py` for the Render backend (`a272af7`, `f767391`) and resolved the merge conflicts that a branch merge had committed into `main.tex`, `DEPLOYMENT.md` and the notes (`cfd25e6`). Cole added the literature PDFs in `sources/` (`05a83c5`) and the project README (`a1f5a3d`).

### Phase 7: The conference paper (29 Oct–9 Nov 2026)

Charis committed Draft 1 of the IST-Africa 2027 paper with its evidence ledger, compliance checklist, quality-control record and author queries (`965562b`). Cole committed Draft 2, rewritten in his voice (`0914567`), and on 9 Nov answered the Draft 1 author queries (`ffc65ea`): deadline 20 November, the lecturer asked for the submission, nothing published elsewhere, keep anonymity with links only in the camera-ready version, remove citation [11], and the Sserunjogi and Adong details confirmed.

## 3. Decisions

| # | Decision | When | Who | Reason | Evidence |
|---|---|---|---|---|---|
| 1 | Treat zeros as missing, after first keeping them | 23 Sep | Charis | stated | `4a36d95`; `report/main.tex` decision table |
| 2 | Leave six sites without coordinates, not KNN-filled | 23 Sep | Charis | stated | `2b7eb86`; `main.tex` line 166 |
| 3 | Hourly grid; interpolate predictors only, at most 3 h; never PM2.5 | 23 Sep | Charis | stated | `f1b0bfd`, `d6743db`; `main.tex` line 168 |
| 4 | Reverse KNN filling of long gaps | 23 Sep | Charis | stated | `32edd3e`; `main.tex` line 170 |
| 5 | Chronological split and Z-scored target from training statistics | 24–26 Sep | Cole, Charis | stated | `6230cdc`, `afd5f6b`; `main.tex` "Modelling" |
| 6 | Select the tuned random forest (Phase 1) | 4 Oct | Charis | stated | `f83e9a3` message |
| 7 | Monitor drift with Evidently, pinned to 0.7.23 | 27 Sep–4 Oct | Cole, Charis | inferred | `2b04c2b`, `f83e9a3` |
| 8 | Stop tracking `*.joblib` | 4 Oct | Charis | stated | `8fbffd6` message |
| 9 | Remove PM10 and rebuild the pipeline | 11 Oct | Charis (committer), both | stated | `83a7e43`; `main.tex` lines 180–188 |
| 10 | Replace extreme PM2.5 with the nearest normal reading | 11 Oct | Charis | stated | notes Round 3 item 3 |
| 11 | Reject SMOTE (`USE_SMOTE = False`) | 11 Oct | Charis | stated | notes Round 3 item 1 |
| 12 | Add PM2.5-history nowcast models; save two models | 11 Oct | Charis | stated | notes Round 3 item 2; decision table |
| 13 | Use three validation designs | 11 Oct | Charis | stated | notes Round 1; `main.tex` limitations |
| 14 | Use the August file as a test set only | 12 Oct | Charis | inferred | `94f40bb`; `main.tex` line 420 |
| 15 | Keep time-of-day imputation for training, not the BiLSTM | 12 Oct | Charis | stated | `16f7c62`; notes Round 4; `main.tex` line 383 |
| 16 | Deploy on Render and Vercel after RunPod, Kaggle and Hugging Face | 10–21 Oct | Charis | stated | `b138bdb`, `35d1c12`, `a272af7`; `DEPLOYMENT.md` |
| 17 | Serve only the forecast model | 11–21 Oct | Charis | stated | `main.tex` line 488 |
| 18 | Rewrite history to drop two AI co-author trailers | 11–12 Oct | not recorded | not recorded | `backup-pre-trailer-*` branches |
| 19 | Move the report to the IEEE Access template | 21 Oct | Charis | not recorded | `cce9a1a`; notes Round 7 |
| 20 | Submit to IST-Africa 2027 | 29 Oct | both | stated | `965562b`; `ffc65ea` AQ19 answer |
| 21 | Draft 2 in Cole's voice | 31 Oct | Cole | stated | `0914567` |
| 22 | Anonymity, deadline and dropping [11] | 9–15 Nov | Cole, Charis | stated | `ffc65ea`; answers given 15 Nov |

**Decision 1: Zeros become missing.** The first pass standardised types and kept zeros. The project then followed the brief, which defines 0 as missing (stated, decision table). The 0 °C / 0 % blocks come as long runs in about 28.8 % of AirQo rows, so they are dropouts, not weather. Consequence: the weather inputs need imputation everywhere downstream.

**Decision 2: No invented coordinates.** KNN on weather and pollution profiles was tried for the six sites that never report a location, then dropped: "two sites can have similar air without being close together" (stated, `main.tex` line 166).

**Decision 3: An hourly grid with limited interpolation.** Resampling made every missing hour explicit (149 sensors × 5,088 hours). Straight-line fills were allowed only for predictors and only across gaps of at most three hours; PM2.5 was never interpolated "because it is the value being predicted" (stated).

**Decision 4: Long gaps stay missing.** KNN filling made 96–98 % of each EDA sensor's series imputed, with only about 12 % distinct values and a sawtooth in the daily means (stated; notes Round 5 cites `32edd3e`). Alternative tried: the KNN fill itself.

**Decision 5: Time-ordered evaluation.** Training on earlier hours and testing on later ones, with the target scaled by training statistics only, "so that nothing about the test period leaked into training" (stated).

**Decision 6: The Phase 1 model.** The tuned random forest was selected with a test MAE of 3.103 µg/m³ (stated in `f83e9a3`). Decision 9 later overturned what it rested on.

**Decision 7: Evidently.** Evidently reports appear from `2b04c2b` and are pinned to 0.7.23 in `f83e9a3`. The reason is not written in a commit; inferred from the brief's monitoring requirement and from the report's monitoring section.

**Decision 8: Model files out of git.** "The trained model is now about 120 MB, above GitHub's 100 MB file limit, so it is regenerated by train.ipynb" (stated, `8fbffd6`). The current forecast model is 1.2 MB, but `*.joblib` stays ignored.

**Decision 9: PM10 out.** After the presentation feedback, PM10 was removed from every stage. The stated reasons: PM2.5 is the fine fraction of PM10, so PM10 is a same-hour co-measurement rather than a driver; it carried about 76 % of the Phase 1 importance; and it is not known in advance, so the August forecasts had to substitute typical values and only repeated each site's daily pattern (`main.tex` lines 180–188; notes Round 6). The authors "expected, and accepted, a large drop in accuracy". Consequence: everything in the paper is about the rebuilt pipeline.

**Decision 10: Extreme values replaced.** Readings above the sensor's Q3 + 3 × IQR (225 of 14,275, 1.5 %) are replaced by the nearest normal reading within six hours; the originals are kept in `pm2_5_original` and scored too (stated, notes Round 3). Alternatives: keep or delete them.

**Decision 11: SMOTE rejected.** All eight models were worse with SMOTE on the hold-out at both strengths, for example LightGBM 9.8 → 28.7 (stated). The experiment stays in the notebook.

**Decision 12: Nowcast models.** Adding the readings 1–3 hours earlier cut hold-out MAE by 11.6 % (random forest) and 14.2 % (LightGBM) and held up in cross-validation (stated). Both families are saved, because forecasts need no live readings and nowcasts are more accurate (decision table).

**Decision 13: Three validation designs.** A two-day hold-out is short; "the three setups and the August test are needed to judge stability" (stated, `main.tex` limitations).

**Decision 14: August as an external test.** The file was used "purely as a test set, with no retraining" (`main.tex` line 420). The reason is not spelled out; inferred: to test transfer to an unseen month. The extreme-value rule was not applied to it.

**Decision 15: The BiLSTM imputer stays an experiment.** It beat time-of-day filling in all 15 variable-and-gap cases (−20.8 %) but changed prediction MAE by −0.4 % on average. Stated reasons: no reliable gain, weather is a minor input, the best and deployed models would not change, and it must be retrained per split (`main.tex` line 383). Caveat recorded: only five models were retested.

**Decision 16: Render and Vercel.** RunPod needed prepaid credit that was "financially straining"; the Kaggle run "did not complete"; Hugging Face refused server-side Spaces with HTTP 402, so only a static page was possible (stated, `DEPLOYMENT.md`, `main.tex` lines 472–478). The Render server installs only five packages (`requirements-render.txt`, `35d1c12`).

**Decision 17: Forecast model only in production.** The nowcast model "is saved but not served, because every request would need the sensor's readings from the previous three hours" (stated).

**Decision 18: History rewrite.** Two 4 Oct commits originally carried `Co-Authored-By: Claude Opus 5.5`; the rewritten copies on `main` do not. No reason is recorded. This matters for the AI declaration (AQ15): it is evidence that AI helped with the notebook re-run and the artifact clean-up.

**Decision 19: IEEE Access template.** Notes Round 7 records the move and the removal of the UCU cover page. No reason is recorded.

**Decision 20: The conference.** Cole's answer to AQ19: "The assignment ended, and the lecturer asked us to submit it" (stated, `ffc65ea`). Nothing has been published or submitted elsewhere.

**Decision 21: Draft 2's voice.** Draft 2 rewrote Draft 1 to follow Cole's writing profile (stated, `0914567`). Draft 3 blends both authors' voices instead, because the paper is joint.

**Decision 22: Submission settings.** Deadline 20 November 2026; anonymity kept during review, links only in the camera-ready version, everything else private; citation [11] (Gürtepe et al.) removed; data described as AirQo network data provided through the course (stated: `ffc65ea` and the authors' answers on 15 Nov 2026).

## 4. Who did what

**Cole Rodney Migisha** started the project and the notebook (`c7f8db8`, `65f0c52`), finished the EDA and took the first models through training (`6230cdc`, `eea1138`), and kept the environment working (`8c57db0`, `aed4ec3`). He built the deployment outputs of Phase 1: the standalone inference script, the first Evidently reports and the August forecasts (`2b04c2b`, `378ad79`). He gathered the literature (`05a83c5`), wrote the README (`a1f5a3d`), carried the paper into Draft 2 and answered the Draft 1 author queries (`0914567`, `ffc65ea`).

**Charis Opol** led the data cleaning and imputation experiments (the seven commits of 23 Sep), completed training and predictions (`afd5f6b`, `5964c6b`), merged and re-ran the final Phase 1 notebook (`ca0bd59`, `f83e9a3`), and carried the rebuild after the feedback: extreme values, nowcast models, BRITS-style imputation, validation designs, August testing (`83a7e43`, `35d1c12`, `94f40bb`, `16f7c62`). He also did the deployment documents and the server (`b138bdb`, `a272af7`), the report and abstract (`2e576c7`, `cce9a1a`) and Draft 1 of the paper (`965562b`). Most merges are recorded under "Charis Opol", the name GitHub uses for web merges.

## 5. Current state and loose ends

**Works and verified (15 Nov 2026):**
- `deployment_outputs/model_validation_comparison.csv` matches the paper's Table 3 to two decimals; `train.ipynb` cell 537 holds the August results (checked this session).
- The saved forecast model reproduced the notebook's test predictions with zero difference (notebook cells 502–503, checked for Draft 1).
- Merge-conflict markers: none in any `.md`, `.tex` or `.py` file (checked this session).
- Render `/health` and the Vercel dashboard returned 200 on 31 Oct 2026 (Draft 2 check; not re-checked today).

**Exists but unverified:**
- The online Hugging Face model and Space still hold the Phase 1 (PM10) model, according to notes Round 5; not checked online.
- Latency on the hosted Render service was never measured.

**Loose ends:**
1. Local `main` is one commit behind `origin/main` (`ffc65ea`). Run `git pull`.
2. `.idea/` is tracked (`65f0c52`). Untrack it and add it to `.gitignore`.
3. `report/slides/~$bilstm_imputation_effect_slides.pptx` is a PowerPoint lock file committed in `16f7c62`. Delete it.
4. `train.ipynb` has 348 code cells; the recorded run covered 346 (notes Round 4). Re-run in full, or keep the paper's "recorded run" wording.
5. `deployment_outputs/kaggle_run_log.txt` and `kaggle_run_metrics.json` record a local run despite their names. Rename them, or explain this in the README.
6. `README.md` line 100 points to the Kaggle instructions, although the Kaggle run did not complete. Add one line of context.
7. Paper: AQ15 stays open (AQ5 and AQ6 resolved 16 Nov) (see `author_queries.md`), and the `.doc` must be checked in Word before upload.

## 6. Evidence index

Copies created by the 11–12 Oct rewrite are listed together; each pair is one piece of work.

| Hash(es) | Date | Author | Subject | Phase |
|---|---|---|---|---|
| c7f8db8 | 2026-09-16 | Cole | first commit | 1 |
| 65f0c52 | 2026-09-21 | Cole | what I've done so far | 1 |
| c69dad0 | 2026-09-22 | Cole | continue | 1 |
| 4a36d95 | 2026-09-23 | Charis | Implementing standard datatypes and leaving the zero values | 1 |
| 2b7eb86 | 2026-09-23 | Charis | Latitudes and longitudes imputation | 1 |
| f1b0bfd | 2026-09-23 | Charis | Offline resampling | 1 |
| d6743db | 2026-09-23 | Charis | Linear and KNN imputation for missing values | 1 |
| 37a83bc | 2026-09-23 | Charis | Selection of the Data points/sites for the EDA | 1 |
| a520d5d | 2026-09-23 | Charis | Distributions | 1 |
| 32edd3e | 2026-09-23 | Charis | Time series and comparison with original data | 1 |
| 6230cdc, 13bb06f | 2026-09-24 | Cole | finished eda and started training | 1 |
| 8c57db0, 917eb0a | 2026-09-24 | Cole | fixed some cascading dependencies (notebook) | 2 |
| aed4ec3, dc7c2d4 | 2026-09-24 | Cole | fixed some cascading dependencies (requirements) | 2 |
| eea1138, f0c6477 | 2026-09-26 | Cole | training | 2 |
| afd5f6b, b347269 | 2026-09-26 | Charis | Training complete | 2 |
| 5964c6b, 175b134 | 2026-09-26 | Charis | Predictions | 2 |
| 2b04c2b, e301050 | 2026-09-27 | Cole | first commit (inference, Evidently, forecasts) | 2 |
| 99e027b, b99fb3d | 2026-09-28 | Cole | some documentation | 2 |
| 378ad79, 8ed6d94 | 2026-10-04 | Cole | evidently | 3 |
| ca0bd59, 44e3468 | 2026-10-04 | Charis | Final notebook | 3 |
| f83e9a3, d27ee17 | 2026-10-04 | Charis | Re-run merged notebook and regenerate monitoring and deployment outputs | 3 |
| 8fbffd6, 386710d | 2026-10-04 | Charis | Stop tracking the model artifact and ignore *.joblib files | 3 |
| b138bdb, 1b6db99 (pre-rewrite 245c2e2) | 2026-10-10 | Charis | Deployment | 4 |
| 83a7e43, 7909058 | 2026-10-11 | Charis | Changes to the work from the feedback of the presentation | 5 |
| 2006484, 549915b | 2026-10-11 | Charis | Changes from the merge: ignore model artifacts and stop tracking them | 5 |
| 2051102, 085e38b | 2026-10-11 | Charis | gitignore | 5 |
| 35d1c12, 2a1c7bc | 2026-10-11 | Charis | Changes to based on the feedback from the lecturer and the render-requirements.txt | 5 |
| 94f40bb, 417ec7d | 2026-10-12 | Charis | Report | 5 |
| 16f7c62, 1656a70 | 2026-10-12 | Charis | Changes from retraining | 5 |
| 2e576c7, 682f5bc | 2026-10-15 | Charis | Report and abstract | 6 |
| 7674654, 436c02e | 2026-10-16 | Charis | Edits the abstract | 6 |
| cce9a1a | 2026-10-21 | Charis | Update pipeline documentation and add new LaTeX template | 6 |
| a272af7 | 2026-10-21 | Charis | Edited serve_model.py | 6 |
| f767391 | 2026-10-21 | Charis | Edited serve_model.py | 6 |
| cfd25e6 | 2026-10-22 | Charis | Edited files from a merge conflict | 6 |
| 05a83c5 | 2026-10-22 | Cole | adding sources | 6 |
| a1f5a3d | 2026-10-22 | Cole | readme | 6 |
| 965562b | 2026-10-29 | Charis | Draft 1 of the report | 7 |
| 0914567 | 2026-10-31 | Cole | Add Draft 2 of the IST-Africa paper in Cole's voice | 7 |
| ffc65ea (origin/main only) | 2026-11-09 | Cole | Update author queries with responses | 7 |

All 60 collected non-merge commits are placed (18 single commits plus 21 rewrite pairs, 18 + 42 = 60), plus `ffc65ea`. Unplaced: none.
