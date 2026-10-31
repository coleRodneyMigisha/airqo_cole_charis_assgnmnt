# Author queries: Draft 2

For Charis and Cole. Yellow `[AQn]` markers in the manuscript point here. Numbers match Draft 1 so the history stays traceable.

## A. Blocking: resolve before any submission

**AQ15: AI declaration and the "AI-generated papers" rule.** This is still the main blocker, and writing in Cole's voice does not remove it. The GenAI Policy says "AI-generated papers should not be submitted", and that interpretation and conclusions must be developed independently by the authors. Draft 2's wording was again produced by Claude, this time following Cole's writing profile. It should still be treated as a scaffold. Before submission, please rewrite it in your own words, check that every interpretation is one you hold, and complete the declaration truthfully. The declaration no longer says the authors reviewed and revised the text, because that has not happened yet. Add that statement once it is true.

**AQ19: Originality, course rules and anonymity.**
- (a) Do CSC3119 or university rules allow submitting this coursework to a conference?
- (b) Has any part been published or submitted elsewhere?
- (c) The repository is public and holds both drafts, and the dashboard, Render service and Hugging Face pages carry your names. Reviewers could find them. Consider making them private or removing identifying details during review.

**Approval.** Neither author has reviewed or approved Draft 2. IST-Africa requires every author to approve the submitted version. Charis has not seen this draft, including the voice change to a jointly authored paper. Agree that the paper should sound like Cole, or settle on a voice that fits you both.

## B. Facts still to confirm

**AQ4: Lsoto et al. [5].** "Agree less well at high concentrations and at hourly resolution" comes from your report and could not be checked in full text.

**AQ5: Wabinyai et al. [8].** "Likewise found lagged PM2.5 useful" comes from your report. Confirm against the paper.

**AQ6: Niyonzima et al. [10].** "Large AirQo record" and "of the same order" rest on your report's figures. Confirm before any numeric comparison.

**AQ7: Gürtepe et al. [11].** Confirm that the paper uses station-withheld validation, and that it was harder than temporal validation.

**AQ8: Data provenance and permission.** Who supplied the two CSV files, under what terms, and is permission needed to publish results? Also confirm the field list in Section 3.1.

**AQ13: Variance and significance.** No repeated seeds, confidence intervals or significance tests were found. A 0.07 µg/m³ gap between the two history models means nothing on current evidence.

**AQ16: LSTM with history in August.** The cause is still unknown. `train.ipynb` cell 536 confirms that this model sees PM2.5 only one hour back through its six-hour window, and that August windows are zero-padded at the start. That describes a difference. It does not explain the result, so the paper still says the cause is unknown.

## C. Voice choices to confirm

These are defaults taken from the writing profile, and Cole can veto any of them.

- **Everyday openers:** the eight-day visitor (Section 1, returned to in Sections 5.5 and 6) and the cake and slice analogy for PM10 (Section 3.2). Both are illustrations, not personal experiences.
- **Questions:** Sections 1, 2, 3.2, 5.1, 5.2, 5.3, 5.5 and 6 use a question to turn the argument. Some reviewers may find this unusual in an IST paper. Remove some if you prefer.
- **Spelling:** British, matching Draft 1 and Cole's proposal. The honours paper used American by default, and this is not settled.
- **Person and contractions:** "we" throughout, with no contractions.
- **Spoken hinge words:** "So", "Now" and "yet" are used, following the addendum.

## D. Resolved since Draft 1

| Query | Resolution | Evidence |
|---|---|---|
| AQ20 deadline | 20 November 2026 | Confirmed by Cole, 31 Oct 2026 |
| AQ1 data spans | Sentence narrowed to the one study read in full | Febrian and Permai [9] |
| AQ9 PM2.5 > PM10 | Confirmed: 3,199 rows, 22.41% | Commit `245c2e2`, `train.ipynb` cells 57 and 59 |
| AQ10 cell count | "Recorded run" wording kept, marker removed | Draft 1 ledger M12 |
| AQ11 deployment | Kaggle "did not complete". Dashboard and `/health` both returned 200 on 31 Oct 2026. The first `/health` check gave no reply within 45 s | `DEPLOYMENT.md` line 8 (no conflict markers remain); direct checks |
| AQ12 time features | The dashboard computes them in the browser, in UTC, then sends them | Live dashboard JavaScript bundle; `serve_model.py` |
| AQ17 | Claim stays out of the paper | Unchanged |
| AQ18 | `report/main.tex` no longer contains conflict markers | Direct check |

AQ2 and AQ3 no longer carry markers, because the unverified details stay out of the text. Restore them only if you confirm them against the papers.

**Note for Cole's records:** the literature in `sources/` is wider than Draft 1's inventory recorded. Wang and Ogawa [6] and Yang et al. [7] are there in full. Only their abstracts were used for Draft 2.
