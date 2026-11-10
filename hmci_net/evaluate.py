"""Evaluate patient-wise DSC, JI and reference-positive patient detection recall."""
import argparse
import json
from pathlib import Path
from .config import nifti_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--label", type=int, required=True, help="1 for binary masks; 2 for LiTS tumor")
    parser.add_argument("--output", required=True, help="New JSON file")
    args = parser.parse_args()
    if args.label < 1:
        parser.error("--label must identify a foreground class")
    if Path(args.output).exists():
        raise FileExistsError(args.output)
    preds = {p.name: p for p in nifti_files(args.predictions)}
    refs = {p.name: p for p in nifti_files(args.references)}
    if preds.keys() != refs.keys():
        raise ValueError("Prediction and reference filenames must match exactly; no case is silently skipped.")
    import numpy as np
    import nibabel as nib
    from .metrics import overlap_metrics
    cases = []
    for name in sorted(refs):
        p, r = nib.load(preds[name]), nib.load(refs[name])
        if p.shape != r.shape or not np.allclose(p.affine, r.affine, atol=1e-4, rtol=0):
            raise ValueError(f"Shape/affine mismatch for {name}. Evaluate masks in the same physical grid.")
        pd, rd = np.asarray(p.dataobj), np.asarray(r.dataobj)
        if any(not np.isfinite(x).all() or not np.array_equal(x, x.round()) or x.min() < 0 for x in (pd, rd)):
            raise ValueError(f"Invalid label map: {name}")
        cases.append({"case": name, **overlap_metrics(pd == args.label, rd == args.label)})
    summary = {}
    for metric in ("dsc", "ji"):
        values = [r[metric] for r in cases if r[metric] is not None]
        summary[metric] = {"n": len(values), "median": float(np.median(values)) if values else None,
                           "q25": float(np.percentile(values, 25)) if values else None,
                           "q75": float(np.percentile(values, 75)) if values else None}
    positive = [r for r in cases if r["reference_positive"]]
    summary["patient_recall"] = sum(r["patient_detected"] for r in positive) / len(positive) if positive else None
    summary["reference_positive_cases"] = len(positive)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"label": args.label, "summary": summary, "cases": cases}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
