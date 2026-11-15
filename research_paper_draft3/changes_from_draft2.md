# Changes from Draft 2

Date: 15 Nov 2026. Status: **Ready for joint author editing. Not ready for submission** (AQ15; see `author_queries.md`. AQ5 and AQ6 resolved 16 Nov).

`research_paper_draft1/` and `research_paper_draft2/` are unchanged. `work_up_to_now.md` in this folder is the project history Draft 3 was built from.

## What changed

- **Voice.** Blended Cole and Charis (the `col-ris-write` base-voice table) instead of Cole alone. Questions cut from 10 to 4 (abstract, introduction, related work, Section 5.5); the methods and results now run on statements. Procedure is described impersonally in Section 3, and "we" is kept for decisions and findings.
- **Your answers applied.** Gürtepe et al. removed (AQ1/AQ7). Sserunjogi [3]: 68 stations, hourly, 2019–2020 (AQ2). Adong [4]: RMSE 18.6 → 7.2 µg/m³, more than 120 devices (AQ3). Lsoto [5]: sensors tracked the reference at low concentrations, dispersed at high ones and agreed better in 24-hour data (AQ4). Data provenance stated (AQ8).
- **References renumbered** into first-citation order: Febrian and Permai is now [6], Wang and Ogawa [7], Yang et al. [8], Wabinyai et al. [9]; BRITS onwards each move down by one. There are 20 references.
- **Caveats moved beside claims.** "This decision rests on five models" is now in Section 5.3; the 0.07 µg/m³ gap between the history models is flagged in the limitations.
- **AI declaration** rewritten: the research, findings and decisions are attributed to the authors, and AI is credited with compiling the draft text, tables and figure and with assisting on parts of the code. The "reviewed and revised" sentence waits for your revision (AQ15).
- **Closing line** added that answers the opening question.
- **Cut.** The Gürtepe sentences in Sections 2 and 6, a repeated sensor-error sentence in Section 2, and the rhetorical questions in Sections 3.2, 5.1, 5.2, 5.3 and 6.

## Checks run on 15 Nov 2026

| Check | Result |
|---|---|
| Table 3 against `model_validation_comparison.csv` and `train.ipynb` cell 537 | Match |
| Tables 1, 2 and 4 against Draft 2 | Unchanged |
| Citations in first-citation order | [1]–[20] in order |
| Abstract | 143 words (limit 100–150) |
| Words (abstract, headings, body, captions; counted as in Draft 2) | 3,984 (Draft 2: 3,989 by the same script) |
| Pages, measured in Microsoft Word | 9 of 10 |
| Em dashes, ellipses, contractions in the paper | None |
| Author names, institution, course code, project URLs in the paper | None. Document properties are blanked, and Word's `RemovePersonalInformation` is set |
| Earlier draft folders | Unchanged |

## Not done

- The notebook was not re-executed. The numbers rest on the Draft 1 evidence ledger and on today's check of Table 3.
- AQ5 and AQ6 could not be checked on 15 Nov, because the publishers blocked automated access. Both were checked against the full texts on 16 Nov and their markers removed.
- No author has revised or approved Draft 3 yet.

## Rebuild

From the repository root:

```sh
python -I research_paper_draft3/build/make_docx.py research_paper_draft1/build/template_base.docx research_paper_draft3/manuscript_source.txt research_paper_draft3/Draft3_IST_Africa_2027.docx
powershell -ExecutionPolicy Bypass -File research_paper_draft1/build/convert.ps1 -Docx "<absolute path to the .docx>"
```

Once you start editing in Word, edit `Draft3_IST_Africa_2027.docx` directly and stop rebuilding from `manuscript_source.txt`, or your edits will be overwritten. Submit the `.doc`.
