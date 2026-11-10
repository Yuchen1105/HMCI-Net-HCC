"""Configuration and path checks, usable without the training dependencies."""
import json
from pathlib import Path


def load_config(path):
    with open(path, encoding="utf-8") as stream:
        config = json.load(stream)
    if config["patch_size"] != [128, 128, 128]:
        raise ValueError("The supplied network has fixed scan grids: use a 128 x 128 x 128 patch.")
    if config["num_classes"] not in (2, 3):
        raise ValueError("Use two classes for binary tasks or three for LiTS.")
    if set(config["labels"]) != {str(i) for i in range(config["num_classes"])}:
        raise ValueError("Labels must cover all output classes.")
    if not 0 <= config["overlap"] < 1:
        raise ValueError("overlap must be in [0, 1).")
    for field in ("iterations", "validation_every", "batch_size", "crops_per_case", "sw_batch_size"):
        if not isinstance(config[field], int) or config[field] < 1:
            raise ValueError(f"{field} must be a positive integer.")
    if config["num_workers"] < 0:
        raise ValueError("num_workers must be nonnegative.")
    if len(config["spacing"]) != 3 or min(config["spacing"]) <= 0:
        raise ValueError("spacing must contain three positive values.")
    if len(config["intensity_window"]) != 2 or config["intensity_window"][0] >= config["intensity_window"][1]:
        raise ValueError("intensity_window must be [lower, upper].")
    return config


def nifti_files(directory):
    directory = Path(directory)
    files = sorted(directory.glob("*.nii.gz")) + sorted(directory.glob("*.nii"))
    if not files:
        raise ValueError(f"No NIfTI files found in {directory}")
    return sorted(files)


def paired_files(root, split):
    root = Path(root)
    images = {p.name: p for p in nifti_files(root / f"images{split}")}
    labels = {p.name: p for p in nifti_files(root / f"labels{split}")}
    if images.keys() != labels.keys():
        raise ValueError(f"Image/mask filenames differ: missing masks={sorted(images.keys()-labels.keys())}, "
                         f"missing images={sorted(labels.keys()-images.keys())}")
    return [{"image": str(images[n]), "label": str(labels[n])} for n in sorted(images)]


def training_files(root):
    train, val = paired_files(root, "Tr"), paired_files(root, "Val")
    overlap = {Path(r["image"]).name for r in train} & {Path(r["image"]).name for r in val}
    if overlap:
        raise ValueError(f"Training and validation case names overlap: {sorted(overlap)}")
    return train, val
