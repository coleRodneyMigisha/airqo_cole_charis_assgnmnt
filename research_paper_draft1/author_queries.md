# Author queries: Draft 1

These queries are for Charis and Cole. Markers such as `[AQ5]` in the manuscript are highlighted in yellow and refer to the numbered items below. Remove each marker and its highlighting once the item is resolved.

## A. Blocking: resolve before any submission

**AQ20 – Deadline conflict.** The website (Submission and Paper Guidelines pages) gives the extended deadline as **20 November 2026**. The Call for Papers PDF gives **31 October 2026**, two days from now. Please confirm with the IST-Africa Secretariat which date applies. Do not rely on 20 November until it is confirmed.

**AQ15 – AI declaration, and the "AI-generated papers" rule.** The GenAI Policy says *"AI-generated papers should not be submitted"*. It also requires that analysis, interpretation of findings and conclusions be developed independently by the authors.
- The research, the analysis and every decision in Draft 1 come from your report and notebook. The *wording* of Draft 1, however, was drafted by Claude (Anthropic) through Claude Code.
- Before submission, please (i) rewrite the paper in your own words, especially the Introduction, Discussion and Conclusions; (ii) check that every interpretation is one you hold; and (iii) complete the declaration in the Acknowledgements truthfully.
- The stored notebook outputs show the pipeline ran from a Claude Code scratchpad environment. If AI tools helped write the analysis code, the report or the figures, the declaration must say so, naming the tool and what it did.

**AQ19 – Originality, course rules and anonymity.**
- (a) The work began as CSC3119 Assignment 4. Do the course or university rules allow submitting it to a conference? Should the course be acknowledged in the final, non-anonymous version?
- (b) Has any part of it been published or submitted elsewhere?
- (c) The public GitHub repository, the Vercel dashboard, the Render service and the Hugging Face model and Space all carry your names or user names and the same content. Reviewers could find them. Consider making them private, or removing identifying details, during review. Add links only in the camera-ready version.

**Approval.** Neither of you has reviewed or approved Draft 1. IST-Africa requires that every author approves the submitted version.

## B. Facts to confirm or supply (they affect claims in the text)

**AQ1 – Data spans of prior forecasting studies.** The text says the forecasting studies "work with one or more years of continuous data [8]–[11]". This is verified only for [9] (two years). Please check [8], [10] and [11], then keep or soften the sentence.

**AQ2 – Sserunjogi et al. [3].** Your report says "68 monitoring stations, 2019–2020". I could not verify this, so Draft 1 omits it. Add it back if the paper confirms it.

**AQ3 – Adong et al. [4].** Your report says that a Random Forest lowered RMSE from 18.6 to 7.2 µg/m³, and that the calibration was rolled out to more than 120 devices. Unverified, so omitted. Restore it if the paper confirms it.

**AQ4 – Lsoto et al. [5].** The abstract confirms 11 low-cost sensors compared with a BAM over 13 months, at hourly and daily resolution. Draft 1 §1 also says sensors "agree less well at high concentrations and at hourly resolution". That comes from your report and is not in the part of the abstract I could read. Please confirm it against the full text.

**AQ5 – Wabinyai et al. [8].** Your report says their models explained up to 57% and 80% of daily variability and that lagged PM2.5 improved accuracy significantly. Draft 1 states only that lagged pollution was modelled (§2) and that lagged PM2.5 was found useful (§6). Please confirm the second point and decide whether to restore the numbers.

**AQ6 – Niyonzima et al. [10].** Your report says 759,480 hourly AirQo observations, 68 sites, MAE 8.71 µg/m³, R² 0.68, and testing on held-out stations. Unverified (no abstract was available). Draft 1 says only "a large AirQo record" and "of the same order". Confirm these numbers before making any quantitative comparison.

**AQ7 – Gürtepe et al. [11].** The report's figures (station-blinded RMSE 9.21 vs temporal 8.28 µg/m³) are unverified and omitted. Please confirm that the paper uses station-withheld validation and that it was harder than temporal validation.

**AQ8 – Data provenance and permission.** Who supplied the two CSV files (AirQo directly, or through the course)? Under what licence or terms? Is permission needed to publish results from them? Also confirm the field list in §3.1.

**AQ9 – "PM2.5 exceeded PM10 in 22.4% of rows".** This appears in your report but not in the current notebook outputs; it is probably from the Phase 1 notebook (commit 245c2e2). Please confirm the figure and the cell it comes from.

**AQ10 – Cell count.** The run logs say 346 code cells; the stored notebook has 348. Your notes (Round 4) say two figure cells were added after the full run. Should the paper say "346 cells in the recorded run", or should the notebook be re-run in full first?

**AQ11 – Deployment history.** `DEPLOYMENT.md` contains unresolved merge-conflict markers, and its two sides disagree. HEAD says the Kaggle attempt "did not complete"; the other side says the notebook "was run end to end on Kaggle". The report and Draft 1 follow HEAD ("did not complete"). Please confirm. Please also confirm that the Render service and Vercel dashboard are currently live.

**AQ12 – Where the time features are computed.** The report (p. 11) says the Render service "derives the cyclical time features from the timestamp exactly as in training". The current `serve_model.py` expects `hour_sin` … `month_cos` to arrive already computed in each request row. Draft 1 follows the code. If the dashboard computes them, say so. If a different server version is deployed, tell us which one.

**AQ13 – Variance and significance.** No repeated runs with different seeds, confidence intervals or significance tests were found. Can you add any? If not, the limitation stays as written. (Reviewers may ask whether a 0.07 µg/m³ gap between the RF and LightGBM history models means anything. With the current evidence, it does not.)

**AQ16 – The LSTM with history in August.** It did well under all three validation designs (LSO MAE 9.41) but scored 19.31 µg/m³ in August, no better than the baseline. Do you know why? Possibilities include its one-hour lag only, a six-hour window with sparse coverage, or different August preprocessing. The paper currently says the cause is unknown.

**AQ17 – Kampala annual mean of 39 µg/m³.** Your report attributes this to "a four-year reference-grade study cited in the assignment brief". It is not in either brief PDF in the repository. Draft 1 leaves it out. If you have the original study, it could be cited directly; it would be a new source, so please add it yourselves.

**AQ18 – `report/main.tex` is in a conflicted state.** It contains 10 unresolved merge conflicts, committed in `5b99f4d`, and will not compile as is. This does not affect Draft 1, but you may want to resolve it. I did not modify it.

## C. Editorial decisions (handled conservatively; change if you disagree)

- **Title.** It was changed from the report's title to stress the "sparse record" lessons. Revert if you prefer.
- **Sections cut for length.** The EDA (five Kampala sites), the maps and the August 1–14 forecast were omitted to stay within the page and word budget.
- **Saminathan & Malathy (2023)** was dropped as not needed.
- **Hugging Face / RunPod / Kaggle** are described generically ("a GPU rental service", "a free hosted notebook platform", "a model-hosting platform") to reduce identifying detail. Render and Vercel are named because they are generic providers. Decide whether to name all of them.
- **AQ14 – Acknowledgements** (no inline marker; removed to save space). The section is left empty apart from the AI declaration. Any thanks to AirQo, the course or supervisors should go in the camera-ready version only.
