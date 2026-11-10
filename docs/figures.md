# Journal figure index and provenance

The homepage displays **5 distinct figures**, with **6 image files** including the editable SVG of the cohort performance chart. The journal manuscript is the sole source of reported experimental evidence.

| Figure | File | Manuscript basis | Content |
| --- | --- | --- | --- |
| Architecture overview | [SVG](figures/architecture.svg) | Section 2.3; implementation mapping in [method.md](method.md) | Four-stage encoder–decoder with HM, MSFM and CDI; a conceptual repository diagram |
| Model comparison | [PNG](figures/segmentation_comparison.png) | Fig. 2 | Nine models, two segmentation tasks, patient-wise and tumor-wise overlap/detection |
| Cohort performance | [PNG](figures/journal_cohort_performance.png) · [SVG](figures/journal_cohort_performance.svg) | Table 3 | Seven task–cohort settings; DSC and IQR |
| Segmentation examples | [PNG](figures/qualitative_segmentation.png) | Fig. 3 | Reference and prediction contours for whole tumors and enhancing regions |
| Size and attenuation robustness | [PNG](figures/segmentation_robustness.png) | Fig. 4 | Tumor maximum-diameter groups and CT-attenuation relationships |

## Extraction and plotting

Manuscript Figs. 2–4 (`word/media/image2.tiff` through `image4.tiff`) were converted losslessly to PNG at their original pixel dimensions, retaining alpha where present. Labels and panels are unchanged.

The cohort chart uses only the central estimates and IQRs in manuscript Table 3. Whiskers are IQRs, not confidence intervals. No patient-level observations were synthesized. Rebuild it with `python tools/render_results.py` after installing `requirements-figures.txt`.

The architecture overview is drawn from the method described in Section 2.3, with code-level mapping in [method.md](method.md). It does not reproduce unavailable supplementary Figs. S1–S2. Implementation correspondence is documented in [reproducibility.md](reproducibility.md).

## Results access

- [Full model, cohort and detection tables](experiments.md)
- [Normalized journal results](results/journal_results.json)
- [Extracted manuscript table text](results/reported_segmentation_results.json)

## Display scope

The repository covers segmentation methodology and model evaluation. The mixed study/prognostic workflow in Fig. 1, clinical baseline variables, prognostic ROC curves, survival curves, Cox models and clinical volumetry agreement analyses are not displayed. Cohort allocation is reported as case counts in the README. Supplementary materials referenced by the manuscript but not supplied are not reconstructed.
