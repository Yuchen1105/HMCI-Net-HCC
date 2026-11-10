# Reproducibility and source correspondence

The journal manuscript guides the scientific description and reported results. Python files from the supplied ZIP are retained byte-for-byte under `source/`. Newly written modules under `hmci_net/` provide a separate, consistent public interface without altering model weights, layer names or computation.

## Implementation correspondence

| Manuscript concept | Source class | Notes |
| --- | --- | --- |
| Four-stage encoder | `uxnet_conv` | Feature widths 48, 96, 192, 384; depths 2, 2, 2, 2 |
| Helical sequence construction | `OScanner` | Alternating in-plane ring order across slices |
| Bidirectional Mamba | `ux_block` | Three channel groups; forward/reverse traversal per group |
| MSFM | `TripleBranchFusion_KAN` | Includes KAN-based channel modulation in the supplied code |
| CDI | `HPA3D` | Grouped directional pooling and cross-branch weighting |
| Segmentation network | `UXNET` | Class name retained for checkpoint compatibility; used by `build_model` |

**Unresolved source/manuscript discrepancy:** the second and third branches in `ux_block.forward` both use `b c w h d -> b c d w h` and the same inverse permutation. They use separate Mamba parameters but do not implement three distinct spatial permutations as the manuscript description suggests. Changing this can change predictions and should be reconciled against the authors' training source/checkpoints before any architecture correction. The new conceptual figure describes the manuscript, not an assertion that this discrepancy has been resolved.

Scan indices are initialized for spatial sizes `[64, 32, 16, 8]`. The new configuration loader therefore requires a 128-cubed input patch. Larger volumes are handled through sliding windows.

## Experimental evidence shown in this repository

The journal manuscript is the sole source of reported experimental results and evaluation images. The homepage displays Figs. 2–4, all model comparisons in Table 2, cohort and detection results in Table 3, and the size/attenuation findings in the Results section. The architecture overview summarizes Section 2.3. The additional cohort chart is drawn from Table 3; its whiskers are IQRs. [Figure provenance](figures.md) and [structured results](results/journal_results.json) document these sources. Missing supplementary figures and tables are not reconstructed from assumptions.

## New public entry points

- Import the model from the actual supplied `HM.py`; the bundled reference training script refers to an absent `MsMambaV04.py`.
- Support independent binary tasks and the original LiTS three-class setting.
- Validate filename pairing, distinct split case names, input geometry and label IDs.
- Use guarded `main` entry points and support zero data-loader workers.
- Evaluate every validation case, return to training mode after validation, and stop at exactly the requested number of optimizer steps.
- Save best, last and final checkpoints separately, with the effective configuration.
- Restore predictions through inverse spatial transforms rather than attaching an identity or original affine to a cropped/resampled array.
- Strictly check checkpoint keys; use the original network without renaming its parameter hierarchy.
- Correctly treat a false-positive-only mask as zero DSC/JI.

The scripts under `source/` are implementation references; use the `hmci_net` entry points for the documented workflow. They include optional imports for networks/extensions not shipped in the ZIP. Their preprocessing utilities should be reviewed before execution; the new command-line pipeline does not run them automatically.

## Configuration provenance

| Setting | New example value | Basis |
| --- | --- | --- |
| Input patch | 128 × 128 × 128 | Source training arguments and fixed scan indices |
| Voxel spacing | 1 × 1 × 1 mm | Source transforms |
| HU window | −21 to 189, scaled to [0, 1] | Source transforms |
| Case batch / crops per case | 1 / 2 | Source arguments; effective patch batch is 2 |
| Optimizer / learning rate | AdamW / 1e−4 | Source training arguments |
| Weight decay | 0.01 | Made explicit from the original AdamW default |
| Iterations / validation interval | 70,000 / 200 | Source training arguments |
| Sliding-window overlap | 0.5 | Source arguments |
| Drop-path rate | 0.1 | Source training model construction |
| Automatic mixed precision | Disabled by default | Conservative new example setting; source entry points differ |
| Validation selection metric | Mean foreground case/class DSC | New development metric; not the manuscript's tumor-wise analysis |

These values are **not independently verified journal settings**. The Word manuscript refers to Supplementary Material 4 for module formulations and Supplementary Material 5 for training details, neither supplied here. The manuscript reports two RTX 3090 GPUs; the new entry point is a single-process, single-GPU baseline. It does not claim multi-GPU reproduction. Resume restores model, optimizer, scaler and step; data-loader and augmentation RNG state are not restored for bitwise continuation.

## Metrics

`hmci_net.evaluate` computes binary DSC and JI for the selected label in each original-grid NIfTI pair. Both-empty masks produce `null` and are omitted from overlap summaries; a false positive against an empty reference scores zero. Patient recall is the proportion of reference-positive cases with at least one overlapping voxel. Negative-reference cases are excluded from that recall denominator. The output records how many cases contributed to every summary.

The manuscript also reports tumor-wise DSC/JI and connected-component detection precision, recall and F1. Those require a separate, specified component matching and aggregation procedure. They are shown as manuscript-reported results, but this release does not claim to reproduce them with voxel-wise precision/recall. No HD95 values or voxel-wise F1 scores are relabeled as journal lesion-detection metrics.

## Environment and verification

The source dependency file did not contain an environment lock, and omitted Mamba. The new requirements list the public entry points' direct dependencies and separate the compiled CUDA packages. A compatible CUDA toolkit, PyTorch build, compiler and Mamba installation are required for actual model execution; those combinations have not been validated in this packaging environment.

The primary document runtime has NumPy but no PyTorch/MONAI/Mamba. The desktop's ordinary Python import also encounters a PyTorch DLL error. An isolated CPU Python environment can be used for limited preprocessing checks; it is not a validated training environment. See [validation.md](validation.md) for checks actually executed. No weights, patient scans, or training jobs are created or downloaded as part of repository preparation.

## Materials needed for exact journal reproduction

Exact train/validation/test patient lists, the preprocessing and model source used for the reported runs, corresponding trained checkpoints, Supplementary Materials 4–5, environment versions, and tumor-wise evaluation rules remain necessary. Author list, journal/DOI metadata and distribution license are also not supplied. This release does not invent them.
