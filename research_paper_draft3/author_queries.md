# Author queries: Draft 3

For Cole and Charis, for your joint editing session. Yellow `[AQn]` markers in the manuscript point here. Numbers carry over from Drafts 1 and 2.

## A. Blocking: resolve before submission (deadline 20 Nov 2026)

**AQ15: AI declaration and the GenAI rule.** IST-Africa's GenAI Policy says "AI-generated papers should not be submitted" and that interpretation and conclusions must be the authors' own. Your findings and decisions are your own, as the git history shows (see `work_up_to_now.md`). The wording of Draft 3, however, was compiled by Claude from your report, notebook and sources. So:
- Rewrite the text in your own words as you edit, above all the Introduction, Discussion and Conclusions.
- The declaration now says that Claude "assisted with parts of the analysis code". The evidence: the stored notebook outputs ran from a Claude Code scratchpad, and two 4 Oct commits originally carried a `Co-Authored-By: Claude` trailer (`1c5625e`, `3fdcd6a`, rewritten as `f83e9a3`, `8fbffd6`). Confirm or correct how much of the code it helped with.
- Add "The authors reviewed, revised and verified the content and take full responsibility for it." only after your revision is done, and then remove the marker.

**Approval.** Both of you must approve the version you submit (Cole answered "Don't worry", 9 Nov; record it here once it is done).

## B. Facts still to confirm

None open. AQ5 and AQ6 were resolved on 16 Nov (see D).

## C. Choices made for you (change them if you disagree)

- **Voice.** Draft 3 blends you both instead of following Cole alone: Cole leads the abstract, introduction, related work and discussion, and Charis leads the methods, results, limitations and conclusion. Rhetorical questions went from 10 to 4. Two analogies remain: the visitor and the cake.
- **Closing line.** A new last paragraph of the Conclusions answers the opening question. Cut it if you need words.
- **Data source.** Section 3.1 now says the files were "provided to us through a university course". The course code is left out to keep the paper anonymous; name it in the camera-ready version if you wish.
- **Deployment platforms** stay generic ("a GPU rental service", "a free hosted notebook platform", "a model-hosting platform"), following your anonymity answer. Render and Vercel are named.

## D. Resolved since Draft 2

| Query | Resolution | Evidence |
|---|---|---|
| AQ1, AQ7 | Gürtepe et al. removed entirely; references renumbered | Cole's answer, 9 Nov; your answer, 15 Nov |
| AQ2 | 68 stations, hourly, 2019–2020 added for [3] | Europe PMC abstract, checked 15 Nov |
| AQ3 | RF RMSE 18.6 → 7.2 µg/m³, more than 120 devices, added for [4] | Cole confirmed, 9 Nov (publisher page not reachable by me) |
| AQ4 | Marker removed; sentence matches the abstract ("dispersed at the higher values"; stronger relationship in 24-hour data) | Europe PMC abstract, checked 15 Nov |
| AQ8 | AirQo network data, provided through the course | Your answer, 15 Nov |
| AQ13 | Kept as a stated limitation, with the 0.07 µg/m³ caveat in the text; marker removed | Your answer, 15 Nov |
| AQ16 | Cause unknown, stated in Section 6; marker removed | Your answer, 15 Nov |
| AQ19 | Lecturer asked for the submission; not published elsewhere; anonymity kept; links only in the camera-ready version | Cole, 9 Nov |
| AQ20 | Deadline 20 November 2026 | Cole, 9 Nov |
| AQ5 | Confirmed; marker removed. Lagged PM2.5 "significantly improved model accuracy"; lag coefficients positive in both cities | Wabinyai et al. full text, checked 16 Nov |
| AQ6 | Confirmed; markers removed. 759,480 hourly observations, 68 sites, MAE 8.71, R² 0.68, so "of the same order" as our 8.43 holds | Niyonzima et al. full text, checked 16 Nov |
| Citation order | [9] was cited before [6] in Drafts 1–2; references renumbered into first-citation order | Template rule: numerical order |
