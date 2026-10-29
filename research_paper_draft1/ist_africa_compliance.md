# IST-Africa 2027 compliance checklist: Draft 1

All requirements below were read from the official IST-Africa 2027 pages on **29 Oct 2026**:
- Submission: `ist-africa.org/Conference2027/default.asp?page=submission`
- Paper Guidelines: `?page=paperguidelines`
- GenAI Policy: `?page=genai`
- Editorial Policy: `?page=editorial`
- Publication Ethics: `?page=ethics`
- Call for Papers PDF
- `IST-AfricaTemplate.dot` and `IST-AfricaGuidelinesforPaperPreparation.doc`

Status values: **Met** = checked in the generated file. **Partly** = partly met, or depends on authors. **Not met** = action required. **Conflict** = official sources disagree.

## Deadline (urgent)

| Requirement | Source | Status | Action |
|---|---|---|---|
| Submission deadline | Submission page and Paper Guidelines: "extended deadline of **20 November 2026**". CFP PDF: "Online Submission Extended Deadline: **31 October 2026**"; "Draft Final Papers submitted online by deadline of 31 October 2026" | **Conflict** | Today is 29 Oct. **Confirm the operative date with the Secretariat before relying on 20 Nov.** The web pages look newer than the PDF, but this is not established. (AQ20) |

## Format and template

| Requirement | Source | Status | Notes / action |
|---|---|---|---|
| Use the IST-Africa Word template (`.dot`) | Paper Guidelines | Met | Draft 1 was created from the official `.dot` via Word, using its own styles: Title, Author Name, Abstract, Heading 1/2, Paragraph 1/2, Caption, List Number, Normal. |
| Upload in `.doc` (Word 97–2003) format | Submission page, step 1 | Met (file produced) | A `.doc` is produced alongside the `.docx`. **Submit the `.doc`**, after the authors' revisions. |
| Full paper 8–10 pages **including references**, c. 4,000 words ("up to 4,000 words") | Submission page; Paper Guidelines; CFP ("maximum 4,000 words") | See `quality_control.md` | Page and word counts are measured on the generated file. Note the old guidelines `.doc` still says "five to eight pages"; the 2027 web pages say 8–10, and these take precedence. |
| Abstract: one paragraph, 100–150 words, covering problem, aim, method, results, conclusion | Paper Guidelines; template | Met (see QC count) | Rewritten from the 248-word abstract in `report/abstract`. |
| Structure: Abstract; Introduction; Objectives; Methodology; Technology/Business Case Description; Results; Conclusions and Summary Recommendations; References | Paper Guidelines | Met | Draft 1 adds Related Work and Discussion. Objectives is §1.1, Technology Description is §4. |
| Headings in mixed case; Heading 1 / Heading 2 styles | Guidelines `.doc` | Met | |
| First paragraph in Paragraph 1 style; later paragraphs in Paragraph 2 style with a leading tab | Guidelines `.doc` | Met | Done by the build script. |
| No headers or footers; **no bold or italics in body text** | Guidelines `.doc` | Met | No bold or italic was applied. AQ markers are **highlighted** for findability only; remove the highlighting with the markers. |
| References: numeric [n] in text, numerical order, Times New Roman 10 pt | Guidelines `.doc` | Met | Ordered by first citation, in the template example's loose style (authors, title, venue, vol., year, pages). |
| Tables and figures numbered consecutively; table caption above, figure caption below, Caption style; centred; inside the typing area | Guidelines `.doc` | Met | 4 tables, 1 figure. |
| Minimum 10 pt text in tables; 8 pt lettering in figures after reduction to 80% | Guidelines `.doc` | Met | Tables are 10 pt. Fig. 1 uses 9–11 pt fonts at 6.5 in, so about 8 pt after 80% reduction. |
| **No colour in illustrations** (printed black and white); no Internet images | Guidelines `.doc` | Met for Draft 1 | Fig. 1 is greyscale with hatching. Existing report figures are in colour and were **not** reused. |
| Single line spacing; justified text | Guidelines `.doc` | Met (template styles) | |

## Double-blind review

| Requirement | Source | Status | Notes / action |
|---|---|---|---|
| No contact details or author-identifying information in the text, file properties or file name, including acknowledgements | Submission steps 2; Editorial Policy | Partly | Author block replaced by "[removed for double-blind review]". No institution, GitHub, Render, Vercel or Hugging Face URLs or names appear in the text. Author, Company and Manager properties were cleared and `RemovePersonalInformation` set. **Check File > Info > Properties in Word before upload.** The file name contains no names. |
| Author details are entered only in the online Author List | Submission page | Not met (author action) | |
| Self-citation / self-plagiarism | Submission (c); Ethics | Partly | The paper reuses the authors' own unpublished course report. That is not prior publication, but the public GitHub repository, live dashboard and Hugging Face Space all reveal identity and content (AQ19). |

## Originality and eligibility

| Requirement | Source | Status | Notes / action |
|---|---|---|---|
| Original work of the listed authors; not previously published; not under review elsewhere | Submission; Editorial; Ethics | Author confirmation required | The report is coursework (CSC3119). Confirm it was not published or submitted elsewhere, and that course rules allow submission (AQ19). |
| Must present analysis of initial or final research results or a case study; "general project descriptions are not appropriate" | Submission; Editorial | Met in framing | Framed as analysis of final results with practitioner lessons, not a project description. |
| Highlight actual or expected impact and the level of innovation | Submission; Paper Guidelines; CFP | Met | §1.1 states the contribution is empirical. §6 separates demonstrated from expected impact. |
| Thematic fit | CFP / Editorial | Met (suggested) | "Next Generation Computing (AI, Big Data, Cloud)" and/or "Environmental Sustainability". Choose the classification at submission. |
| Paper type | Paper Guidelines | Suggested | "Presentation of innovative ICT achievements" or "Lessons learnt from case studies". |
| All authors made substantial contributions and approved the submitted version | Submission; Ethics | **Not met** | Neither author has reviewed or approved Draft 1. |
| Ethical approval / informed consent where appropriate | Ethics | Probably N/A | Sensor data, no human subjects. Confirm the data licence (AQ8). |
| Conflicts of interest disclosed | Ethics | Not addressed | Add if any exist. |
| Presenter registration; one paper per presenter | Submission | Author action | |

## AI use (GenAI Policy)

| Requirement | Source | Status | Notes / action |
|---|---|---|---|
| Declaration of AI use in the Acknowledgements section, using the template's heading and wording, naming the specific tool and purpose | GenAI Policy; template | Partly | Draft 1 includes the template's "acknowledge the use" variant naming Claude (Anthropic) via Claude Code and what it did. **The authors must confirm and complete it** (AQ15), including any AI help with the original code or report. |
| "Intellectual content (including research ideas), research data, methodological design, analysis and discussion of results (including interpretation of findings) as well as conclusions should be developed independently by authors" | GenAI Policy; CFP | **Risk** | The research, analysis and decisions come from the authors' own report and notebook. But the *prose* of Draft 1, including its Discussion and Conclusions, was drafted by an AI from that material. The authors must re-author these sections in their own words and own the interpretation. |
| "AI-generated papers should not be submitted. Where such papers are identified, they will be subject to rejection or withdrawal." | GenAI Policy | **Risk; blocks submission as is** | **Draft 1 must not be submitted as is.** Treat it as a structured, evidence-checked scaffold. |
| Authors have full and sole responsibility for scientific content and originality | GenAI Policy | Author responsibility | |

## Requirements not verified

- Whether the organisers apply a specific reference style beyond the template's single example. The template shows only one book-chapter example.
- Whether "c. 4,000 words" includes references. The pages say "8–10 pages including references" and "up to 4,000 words" without defining the count.
- The online form's paper-type and thematic categories. These are visible only after login.
