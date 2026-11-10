"""Sliding-window inference with predictions restored to the input NIfTI grid."""
import argparse
from pathlib import Path
from .config import load_config, nifti_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--images", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    cfg = load_config(args.config)
    files = nifti_files(args.images)
    if not Path(args.checkpoint).is_file():
        parser.error("Checkpoint not found")
    output = Path(args.output)
    for p in files:
        if (output / p.name).exists():
            raise FileExistsError(f"Prediction already exists: {output / p.name}")
    import numpy as np
    import nibabel as nib
    import torch
    from monai.inferers import sliding_window_inference
    from .data import make_transforms, restore_mask
    from .model import build_model, load_weights
    if not torch.cuda.is_available():
        raise RuntimeError("Inference requires CUDA and mamba-ssm.")
    device = torch.device("cuda")
    model = build_model(cfg).to(device)
    ckpt = load_weights(model, args.checkpoint, device)
    if ckpt.get("config") and any(ckpt["config"][k] != cfg[k] for k in ("task", "num_classes", "spacing", "intensity_window")):
        raise ValueError("Use the task and preprocessing configuration saved alongside this checkpoint.")
    model.eval()
    transform = make_transforms(cfg, labeled=False)
    output.mkdir(parents=True, exist_ok=True)
    for path in files:
        sample = transform({"image": str(path)})
        with torch.inference_mode(), torch.amp.autocast("cuda", enabled=cfg["amp"]):
            logits = sliding_window_inference(sample["image"].unsqueeze(0).to(device), cfg["patch_size"],
                                              cfg["sw_batch_size"], model, overlap=cfg["overlap"],
                                              mode="gaussian", device="cpu")
        # Keep a channel dimension for inverse spatial transforms.
        restored_tensor = restore_mask(logits[0].argmax(0, keepdim=True), sample["image"], transform)
        restored = restored_tensor[0].cpu().numpy().astype(np.uint8)
        original = nib.load(path)
        if restored.shape != original.shape or not np.allclose(restored_tensor.affine.numpy(), original.affine, atol=1e-4, rtol=0):
            raise RuntimeError(f"Inverse transform geometry mismatch for {path.name}")
        header = original.header.copy()
        header.set_data_dtype(np.uint8)
        nib.save(nib.Nifti1Image(restored, original.affine, header), output / path.name)
        print(f"Saved {output / path.name}", flush=True)


if __name__ == "__main__":
    main()
