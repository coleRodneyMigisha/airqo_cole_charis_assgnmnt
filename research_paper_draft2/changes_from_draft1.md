# Changes from Draft 1

Date: 31 Oct 2026. Status: **Draft 2 is ready for author review. It is not ready for submission** (see `author_queries.md`).

`research_paper_draft1/` is unchanged. This folder adds to it.

## What changed

- **Voice.** Rewritten in Cole's voice, following `cole_s_tongue.md` and its addendum in the honours package: question before claim, reasoning shown before conclusions, everyday analogies, sections that end on the next question, no em dashes, no contractions, no invented experiences.
- **IST format.** Section structure, Tables 1-4, Figure 1 and all 21 references are as in Draft 1. Word template styles are reused, and tables and references match line for line.
- **Evidence added.**
  - 3,199 rows for the PM2.5 > PM10 count (AQ9).
  - Wang and Ogawa [6] and Yang et al. [7] now carry specific findings from their abstracts, read from the PDFs in `sources/`: one year in Nagasaki; 68 cities, 22 months in China; humidity changing sign by region.
  - The dashboard's role in computing time features (AQ12).
- **Claims narrowed.**
  - "Most machine-learning studies ... [8]-[11]" now says only that the study read in full used two years of data (AQ1). The gap statement no longer claims the others use a year or more.
  - The abstract separates the 8.43-8.50 range from "the best" in August, because different tree models hold those two results.
  - "SMOTE made every model worse" is now "all eight models tested".
  - The AI declaration no longer states that the authors reviewed the text.
- **Cut for length.** The random forest SMOTE example (10.10), the training-to-hold-out drift sentence, and repeated limitations and recommendations.

## Checks run on 31 Oct 2026

| Check | Result |
|---|---|
| Numbers compared with Draft 1 | New: 3,199, 22, 68, all sourced. Removed: 10.10 |
| Table 3 against `model_validation_comparison.csv` and notebook cell 537 | Match |
| Tables and references against Draft 1 | 0 lines changed |
| Abstract | 142 words (limit 100-150) |
| Body, abstract, headings and captions | 3,987 words, counted as in Draft 1 |
| Pages | 10 of 10 in LibreOffice |
| Em dashes, ellipses, contractions | None |
| Author names, institution, project URLs in PDF | None found |
| Draft 1 folder | Unchanged |

## Not done

- **Word was not used.** The `.pdf` and `.doc` were built with LibreOffice, not Word, so pagination may differ. Open the `.doc` in Word before upload, and check that it stays within 10 pages and that File > Info > Properties is blank.
- **The notebook was not re-executed.** Numbers carried over from Draft 1 rest on the checks in `research_paper_draft1/evidence_ledger.md`, which stay valid.
- **No author has reviewed this draft.**

## Rebuild

From the repository root:

```sh
python -I research_paper_draft2/build/make_docx.py research_paper_draft1/build/template_base.docx research_paper_draft2/manuscript_source.txt research_paper_draft2/Draft2_IST_Africa_2027.docx
```

Figure 1 is reused from `research_paper_draft1/figures/`.
