# Reference check (comment 8), 17 Nov 2026

Every reference with a DOI was looked up in the Crossref API (api.crossref.org/works/<doi>) and its title, authors, journal, volume, issue, pages and year compared with the manuscript. References without a DOI were checked against the downloaded file in `sources/` or are standard, well-known works.

| Ref | Year | Result |
|---|---|---|
| [2] Okure et al. | 2022 | Matches Crossref |
| [3] Sserunjogi et al. | 2022 | Matches |
| [4] Adong et al. | 2022 | Matches |
| [5] Lsoto et al. | 2026 | Matches. **"Lsoto" is correct, not a typo**: Crossref lists Dorothy Lsoto (ORCID 0009-0003-7222-8469, University of Wisconsin-Madison); she is also first author of doi:10.1029/2025jd044895 on Kampala air quality. DOI resolves to tandfonline.com. |
| [6] Febrian and Permai | 2025 | Matches (E3S Web Conf. 680, 00067) |
| [7] Wang and Ogawa | 2015 | Matches |
| [8] Yang et al. | 2017 | Matches |
| [9] Wabinyai et al. | 2026 | Matches (vol. 29, Jan 2026, art. 100411; DOI prefix says 2025, online date) |
| [10] Niyonzima et al. | 2026 | Matches (vol. 6, art. 1039, 16 Jun 2026) |
| [12], [13], [14], [16], [17] | 1997-2020 | Match |
| [21] Atuyambe et al. | 2025 | Matches; **issue number (no. 2) was missing and has been added** |
| [24] Le et al. | 2025 | Matches |
| [1], [11], [15], [18], [19], [20] | | No DOI; standard works (WHO guidelines; BRITS, NeurIPS 2018; SHAP, NeurIPS 2017; LightGBM, NeurIPS 2017; scikit-learn, JMLR 2011; Evidently software) |
| [22], [23] | | UN SDG metadata PDFs, downloaded to `sources/` |
| [25]-[28] | 2022-2024 | arXiv PDFs downloaded to `sources/` and read |
