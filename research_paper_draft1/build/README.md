# Rebuilding Draft 1

Run these from the repository root. Python needs only the standard library plus matplotlib and pandas for the figure. Microsoft Word is needed for the `.doc` and `.pdf` outputs.

1. `python -I research_paper_draft1/build/make_fig1.py . research_paper_draft1/figures/fig1_mae_by_setting.png`
   Builds Figure 1 from `deployment_outputs/model_validation_comparison.csv`, plus August values copied from `train.ipynb` cell 537.
2. `python -I research_paper_draft1/build/make_docx.py research_paper_draft1/build/template_base.docx research_paper_draft1/manuscript_source.txt research_paper_draft1/Draft1_IST_Africa_2027.docx`
3. `powershell -ExecutionPolicy Bypass -File research_paper_draft1/build/convert.ps1 -Docx <absolute path to the .docx>`
   Writes the `.pdf` and the `.doc` next to the `.docx`, and prints the page and word counts.

## Notes

- `IST-AfricaTemplate.dot` is the official template, downloaded on 29 Oct 2026.
- `template_base.docx` is Word's conversion of that template and still contains the template's sample text. `make_docx.py` uses only its styles, numbering, theme and page setup.
- Word stamped a user name into the properties of `template_base.docx`. The generated manuscript's properties are blanked by `make_docx.py`; this helper file is not for submission.
- Once you start editing in Word, edit the `.docx` directly. `manuscript_source.txt` is only the Draft 1 starting point.
