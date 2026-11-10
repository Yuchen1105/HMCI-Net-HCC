"""Patient-wise binary overlap metrics. No survival or clinical analysis."""
import numpy as np


def overlap_metrics(prediction, reference):
    prediction, reference = np.asarray(prediction, dtype=bool), np.asarray(reference, dtype=bool)
    if prediction.shape != reference.shape:
        raise ValueError("Prediction and reference shapes must match.")
    intersection = int(np.count_nonzero(prediction & reference))
    p, g = int(prediction.sum()), int(reference.sum())
    return {
        "dsc": 2 * intersection / (p + g) if p + g else None,
        "ji": intersection / (p + g - intersection) if p + g else None,
        "reference_positive": g > 0,
        "patient_detected": intersection > 0 if g else None,
    }
