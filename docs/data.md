# Data layout and preprocessing

Use one folder per segmentation task with `imagesTr`, `labelsTr`, `imagesVal` and `labelsVal`. Each pair has identical filenames, a matching 3D shape, and matching NIfTI affine. Images must contain CT intensities in HU. Masks must contain integer class IDs. One model consumes one single-channel CT volume; multiphase fusion is not implemented by this release.

| Configuration | Mask labels | Model output |
| --- | --- | --- |
| `configs/whole_tumor.json` | 0 background; 1 whole tumor | 2 channels |
| `configs/enhancing_tumor.json` | 0 background; 1 enhancing region | 2 channels |
| `configs/lits.json` | 0 background; 1 liver; 2 tumor | 3 channels |

Whole-tumor and enhancing-tumor configurations train independent models. Do not pass three-class LiTS labels to a binary configuration without explicitly converting the labels beforehand. Do not infer enhancing-region labels from a whole-tumor mask.

The supplied source's example preprocessing reorients to RAS, resamples to isotropic 1 mm spacing, clips/scales the −21 to 189 HU window, and crops to positive image foreground. The new training transforms additionally pad small images before sampling fixed-size patches, then apply the source-style flip, rotation, affine and intensity augmentations. The exact journal preprocessing must still be checked against the missing supplement.

If liver-region cropping is required for a particular experiment, supply a liver ROI obtained independently of the tumor reference labels. The new entry point does not generate liver masks or silently crop using tumor ground truth. Predictions are restored to the geometry of the **input file**; if that file was already externally cropped, restoration to the original uncropped scan requires the external cropping metadata.

Training/validation pairing fails on missing or extra masks. The same case filename cannot appear in both splits. Users should also maintain patient-level split integrity when a patient has several scans; distinct filenames alone cannot establish that separation.

Inference accepts an image-only directory and saves one same-named NIfTI mask per input. Existing predictions are not overwritten. Evaluation requires exactly matching prediction/reference filenames and checks physical geometry before comparing voxels.

No datasets, patient identifiers, split lists, or trained weights are distributed here. The manuscript identifies LiTS, MSD Hepatic Vessels, CECT and HCC-TACE-Seg as external datasets; acquire data and applicable permissions through their respective providers. The local example configuration does not recreate the manuscript's fixed external-validation cohorts.
