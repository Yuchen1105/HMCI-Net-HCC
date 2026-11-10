# Journal segmentation experiments

Reported results from the supplied manuscript; no new experiments were run. DSC/JI are on a 0–1 scale, with reported IQRs retained.

## Whole-tumor model comparison

| Model | Patient DSC | Patient JI | Tumor DSC | Tumor JI |
| :-- | --: | --: | --: | --: |
| 3D UXNet | 0.886 (0.844-0.928) | 0.801 (0.738-0.864) | 0.888 (0.839-0.937) | 0.805 (0.736-0.875) |
| SegMamba | 0.852 (0.769-0.935) | 0.758 (0.656-0.860) | 0.884 (0.835-0.933) | 0.799 (0.730-0.868) |
| SuperLightNet | 0.710 (0.584-0.836) | 0.579 (0.446-0.711) | 0.777 (0.695-0.859) | 0.649 (0.550-0.748) |
| nnWNet | 0.715 (0.590-0.839) | 0.583 (0.452-0.714) | 0.772 (0.685-0.859) | 0.644 (0.541-0.748) |
| EMNet | 0.840 (0.755-0.925) | 0.740 (0.636-0.845) | 0.878 (0.823-0.933) | 0.790 (0.717-0.863) |
| UKAN-EP | 0.625 (0.471-0.779) | 0.490 (0.344-0.635) | 0.721 (0.623-0.818) | 0.582 (0.471-0.692) |
| SwinSMT | 0.673 (0.526-0.820) | 0.542 (0.398-0.686) | 0.736 (0.635-0.837) | 0.602 (0.487-0.718) |
| UNETR | 0.530 (0.393-0.667) | 0.385 (0.263-0.508) | 0.626 (0.533-0.719) | 0.470 (0.374-0.565) |
| **HMCI-Net** | **0.897 (0.850-0.945)** | **0.820 (0.753-0.887)** | **0.906 (0.866-0.945)** | **0.832 (0.774-0.891)** |

## Enhancing-tumor model comparison

| Model | Patient DSC | Patient JI | Tumor DSC | Tumor JI |
| :-- | --: | --: | --: | --: |
| 3D UXNet | 0.710 (0.608-0.812) | 0.569 (0.460-0.679) | 0.772 (0.693-0.852) | 0.642 (0.550-0.735) |
| SegMamba | 0.589 (0.461-0.717) | 0.442 (0.319-0.564) | 0.677 (0.580-0.774) | 0.528 (0.424-0.633) |
| SuperLightNet | 0.693 (0.570-0.815) | 0.555 (0.429-0.681) | 0.776 (0.709-0.843) | 0.644 (0.560-0.728) |
| nnWNet | 0.619 (0.463-0.774) | 0.482 (0.340-0.624) | 0.714 (0.622-0.806) | 0.571 (0.466-0.676) |
| EMNet | 0.668 (0.547-0.789) | 0.525 (0.403-0.648) | 0.714 (0.620-0.808) | 0.572 (0.464-0.680) |
| UKAN-EP | 0.625 (0.505-0.746) | 0.477 (0.361-0.593) | 0.713 (0.621-0.805) | 0.570 (0.468-0.672) |
| SwinSMT | 0.688 (0.567-0.809) | 0.549 (0.426-0.672) | 0.737 (0.649-0.824) | 0.598 (0.496-0.701) |
| UNETR | 0.384 (0.270-0.497) | 0.251 (0.161-0.341) | 0.541 (0.445-0.637) | 0.384 (0.291-0.478) |
| **HMCI-Net** | **0.801 (0.770-0.832)** | **0.671 (0.627-0.714)** | **0.811 (0.765-0.858)** | **0.688 (0.628-0.748)** |

## Whole-tumor cohort results

| Cohort | Patient DSC | Patient JI | Tumor DSC | Tumor JI |
| :-- | --: | --: | --: | --: |
| Internal test | 0.897 (0.850–0.945) | 0.820 (0.753–0.887) | 0.906 (0.866–0.945) | 0.832 (0.774–0.891) |
| TCIA-HCC | 0.814 (0.640–0.871) | 0.687 (0.471–0.772) | 0.856 (0.754–0.899) | 0.748 (0.605–0.817) |
| LITS | 0.730 (0.652–0.829) | 0.575 (0.484–0.707) | 0.776 (0.675–0.844) | 0.634 (0.509–0.730) |
| MSD | 0.739 (0.632–0.825) | 0.586 (0.462–0.702) | 0.798 (0.719–0.855) | 0.663 (0.562–0.747) |
| CECT | 0.665 (0.573–0.760) | 0.499 (0.402–0.613) | 0.750 (0.659–0.797) | 0.600 (0.491–0.662) |

## Enhancing-tumor cohort results

| Cohort | Patient DSC | Patient JI | Tumor DSC | Tumor JI |
| :-- | --: | --: | --: | --: |
| Internal test | 0.801 (0.770–0.832) | 0.671 (0.627–0.714) | 0.811 (0.765–0.858) | 0.688 (0.628–0.748) |
| TCIA-HCC | 0.759 (0.675–0.845) | 0.612 (0.509–0.731) | 0.819 (0.725–0.859) | 0.693 (0.568–0.753) |

## Detection

| Task | Cohort | Patient recall | Tumor precision | Tumor recall | Tumor F1 |
| :-- | --: | --: | --: | --: | --: |
| whole_tumor | Internal test | 0.927 | 0.942 | 0.927 | 0.935 |
| whole_tumor | TCIA-HCC | 0.804 | 0.920 | 0.805 | 0.860 |
| whole_tumor | LITS | 0.756 | 0.757 | 0.791 | 0.774 |
| whole_tumor | MSD | 0.809 | 0.873 | 0.813 | 0.842 |
| whole_tumor | CECT | 0.586 | 0.852 | 0.637 | 0.729 |
| enhancing_tumor | Internal test | 0.796 | 0.879 | 0.794 | 0.834 |
| enhancing_tumor | TCIA-HCC | 0.674 | 0.840 | 0.817 | 0.828 |

Source: manuscript Tables 2–3. All nine model comparisons are available for overlap; complete comparator detection and external-overlap tables were referenced in the manuscript supplement but were not supplied. Those missing entries are not reconstructed from images.

[Machine-readable values](results/journal_results.json) · [Figure index](figures.md) · [Repository homepage](../README.md)
