# Quality-control report: Draft 1

Date: 29 Oct 2026. Status: **Draft 1 is ready for author review. It is not ready for submission.**

## 1. Skills requested in the brief

- `/howtotalk` and `/humanizer` are **not installed**. They are absent from the session's skill list, `~/.claude/skills` and the installed plugins. Neither was loaded.
- Their stated principles were applied by hand:
  - specific rather than generic statements;
  - varied sentence openings;
  - no filler or inflated claims;
  - clear separation of evidence, interpretation and speculation.
- No step was taken to disguise AI involvement. The draft declares it.

## 2. Checks performed

| Check | Method | Result |
|---|---|---|
| Report vs artifacts | Numbers in `report/main.pdf` traced to the CSV, JSON, notebook outputs and Git history (`evidence_ledger.md`) | Main results all match. Discrepancies are listed in §3. |
| Abstract vs paper | All 8 numbers in the abstract searched in the PDF body | Each appears in the body. The abstract is 144 words (limit 100–150). |
| Numerical values | Table 3 and Fig. 1 read from the CSV programmatically; Table 4 from NB cell 436; August values from NB cell 537; percentages recomputed (11.6%, 14.2%) | Match to 2 d.p. |
| Overstated claims | Each novelty and impact sentence checked against the ledger | One fix: "history models are most stable / kept skill in August" was narrowed to the **tree** models with history, because the LSTM with history scored 19.31 µg/m³ in August. Another fix: the extreme-value effect was corrected to "about 1.3 µg/m³". |
| Citations | Each [n] checked against what the source was verified to support (identity, abstract or full text) | Unverified numeric details from 5 papers were removed and flagged (AQ2–AQ7). All 21 references are cited in the text. |
| Reference metadata | Crossref for 16 DOIs; arXiv for BRITS and SHAP; NeurIPS page for LightGBM; JMLR page for scikit-learn | All resolve. Added missing article numbers: [4] e76, [10] 1039. |
| Anonymisation | PDF text searched for author names, institution, registration numbers, ORCID, repository or service URLs, HF user name | None found. `.docx` core properties have blank creator and last-modified-by. The `.doc` header shows no Author or Last-Saved-By field. |
| Template styles | Built from Word's conversion of the official `.dot`, using its style IDs | Confirmed visually on all 10 pages. No explicit bold or italic runs in the body (count 0). |
| Figures and tables | Captions (tables above, figure below), numbering, in-text references, greyscale | Tables 1–4 and Fig. 1 are each referenced. Fig. 1 is checked as an image. Table text is 10 pt. |
| Build validation | Word opened the `.docx`, repaginated, exported PDF, saved `.doc`; PDF re-read with pdftotext and rendered with PyMuPDF | 10 pages. The last page holds reference [21] only. |
| Repository integrity | `git status` | Only `research_paper_draft1/` is new. No existing file was modified, nothing was executed from the project, and nothing was committed. |

## 3. Discrepancies found in the project (preserved, not silently resolved)

1. `report/main.tex`, `report/pipeline_update_notes.md` and `DEPLOYMENT.md` contain **committed, unresolved merge-conflict markers** (AQ11, AQ18).
2. The report says the API derives the time features from a timestamp. `serve_model.py` expects them pre-computed (AQ12).
3. The "39 µg/m³ Kampala annual mean" claim is not in the briefs it is attributed to (AQ17).
4. The run logs say 346 code cells; the notebook has 348 (AQ10).
5. Several "Kaggle" output files record a *local* run. The paper does not claim cloud execution.
6. The source abstract is 248 words, above the 150-word limit. It was rewritten.

## 4. Length

- Body text including the abstract, headings and captions: about **3,980 words**. Tables add about 210, the AI declaration 120 and references about 690.
- Word's total count is 5,090.
- The guidance gives "up to 4,000 words" without defining what counts; the body alone is at that limit.
- Pages: **10 of a maximum of 10**, including references. Author revisions that add text will need equal cuts. The easiest candidates are §5.4 (SMOTE) and the second Related Work paragraph.

## 5. Remaining risks

| Risk | Severity | See |
|---|---|---|
| IST-Africa GenAI policy: "AI-generated papers should not be submitted". The prose of Draft 1 is AI-drafted. | **High; blocks submission** | AQ15 |
| The deadline may be **31 Oct 2026** (CFP) rather than 20 Nov (website) | **High** | AQ20 |
| Authors have not reviewed or approved the draft | **High** | `author_queries.md` §A |
| Public repo, dashboard and HF pages could de-anonymise the paper | Medium | AQ19 |
| Five literature claims rest on the authors' report, not verified full texts | Medium | AQ1–AQ7 |
| No variance or significance testing; 28-hour hold-out | Medium (scientific) | AQ13; stated in §6 |
| Data licence and permission to publish | Medium | AQ8 |
| Page budget is fully used | Low | §4 above |

## 6. Not done, and why

- **The notebook was not re-executed.** Stored outputs were sufficient, and a re-run would take about 56 minutes and could overwrite artifacts.
- **No LaTeX build.** IST-Africa requires its Word template and `.doc` upload.
- **Colour figures from the report were not reused.** The guidelines require black-and-white illustrations.
- **The Render and Vercel services were not contacted.** Their current availability is unverified.
