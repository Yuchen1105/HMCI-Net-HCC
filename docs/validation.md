# Validation record

Checks performed while preparing the local journal repository on 10 November 2026:

| Check | Result |
| --- | --- |
| Configuration, filename pairing, split separation and metric edge cases | 9 tests passed in the bundled Python/NumPy environment |
| MONAI geometry restoration and label/affine rejection | 2 additional CPU tests passed |
| Complete available unit suite | 11 passed |
| Model source | Original Python contents retained; checked against SHA256 manifest |
| Figure extraction | Manuscript Figs. 2–4 converted to PNG with original dimensions and pixels |
| Architecture SVG | Rendered and visually inspected |
| Python syntax, local Markdown links and figure allowlist | Checked with `python tools/check_repository.py` |
| Full model training / forward inference | Not executed: no configured Mamba/CUDA environment |
| Journal result reproduction | Not performed: experiment-specific configurations, data splits and weights are not supplied |

The CPU geometry check used the existing isolated Python environment with PyTorch 1.12.1, MONAI 1.5.2 and nibabel 5.3.2. It checks preprocessing and inverse transforms only; this is not a supported or validated training stack. The bundled runtime can run the nine core checks and skips the two geometry checks when their dependencies are absent.

The inverse-transform test uses a synthetic anisotropic image with a nontrivial affine, a reversed axis, foreground cropping and a label mask. It verifies the restored volume shape, affine and overlap. No patient data are used in the tests.

Neither passing these tests nor preserving the source establishes the reported scientific performance. The unresolved scan-direction discrepancy and reproduction limits are documented in [reproducibility.md](reproducibility.md).

## Journal experiment presentation

The homepage contains five distinct figures: a method overview based on Section 2.3, manuscript Figs. 2–4 and a chart drawn from Table 3. The cohort chart also has an editable SVG, giving six figure files.

All 18 model/task comparison rows and seven cohort/task rows are normalized from the manuscript tables. The cohort chart was rendered and visually inspected. No patient-level points, statistical tests or missing supplementary tables were synthesized.

`tools/check_repository.py` checks relative documentation links, Python syntax, the preserved source hashes, the six-file figure allowlist, the five homepage images and the journal-result file allowlist. Presentation changes do not alter the model computation or constitute new model experiments.
