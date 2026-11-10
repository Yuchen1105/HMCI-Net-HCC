"""Configurable HMCI-Net training. Run from the repository root."""
import argparse
import json
from pathlib import Path
from .config import load_config, training_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--iterations", type=int, help="Override example training length")
    parser.add_argument("--resume", help="Resume from last.pt, including optimizer state")
    parser.add_argument("--check-data", action="store_true", help="Check configuration and file pairing without loading ML libraries")
    args = parser.parse_args()
    cfg = load_config(args.config)
    if args.iterations is not None:
        if args.iterations < 1:
            parser.error("--iterations must be positive")
        cfg["iterations"] = args.iterations
    train_files, val_files = training_files(args.data)
    if args.check_data:
        print(json.dumps({"task": cfg["task"], "train_cases": len(train_files), "validation_cases": len(val_files)}, indent=2))
        return

    import torch
    from monai.data import Dataset, DataLoader
    from monai.inferers import sliding_window_inference
    from monai.losses import DiceCELoss
    from monai.utils import set_determinism
    from .data import make_transforms
    from .model import build_model, load_weights

    if not torch.cuda.is_available():
        raise RuntimeError("Training requires a CUDA environment with mamba-ssm installed.")
    set_determinism(seed=cfg["seed"])
    device = torch.device("cuda")
    output = Path(args.output)
    if not args.resume and any((output / n).exists() for n in ("last.pt", "best.pt", "final.pt")):
        raise FileExistsError("Output already contains checkpoints. Choose a new output folder or explicitly resume.")
    output.mkdir(parents=True, exist_ok=True)
    model = build_model(cfg).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["learning_rate"], weight_decay=cfg["weight_decay"])
    scaler = torch.amp.GradScaler("cuda", enabled=cfg["amp"])
    loss_fn = DiceCELoss(to_onehot_y=True, softmax=True)
    step, best = 0, -1.0
    if args.resume:
        ckpt = load_weights(model, args.resume, device)
        if ckpt.get("config") and any(ckpt["config"][k] != cfg[k] for k in ("task", "num_classes", "spacing", "intensity_window")):
            raise ValueError("Resume configuration differs from checkpoint task/preprocessing.")
        optimizer.load_state_dict(ckpt["optimizer"])
        scaler.load_state_dict(ckpt["scaler"])
        step, best = ckpt["step"], ckpt["best_validation_dice"]
        if step >= cfg["iterations"]:
            raise ValueError("Checkpoint has already reached the requested iteration count.")
    (output / "config.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    train_loader = DataLoader(Dataset(train_files, make_transforms(cfg, training=True)),
                              batch_size=cfg["batch_size"], shuffle=True, num_workers=cfg["num_workers"],
                              persistent_workers=cfg["num_workers"] > 0)
    val_loader = DataLoader(Dataset(val_files, make_transforms(cfg)), batch_size=1, num_workers=cfg["num_workers"])

    def save(name):
        target = output / name
        temporary = target.with_suffix(".tmp")
        torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(),
                    "scaler": scaler.state_dict(), "step": step, "best_validation_dice": best,
                    "config": cfg}, temporary)
        temporary.replace(target)

    def validate():
        model.eval()
        values = []
        with torch.no_grad():
            for batch in val_loader:
                with torch.amp.autocast("cuda", enabled=cfg["amp"]):
                    logits = sliding_window_inference(batch["image"].to(device), cfg["patch_size"],
                                                      cfg["sw_batch_size"], model, overlap=cfg["overlap"],
                                                      mode="gaussian", device="cpu")
                pred, gt = logits.argmax(1), batch["label"][:, 0].cpu()
                for c in range(1, cfg["num_classes"]):
                    p, g = pred == c, gt == c
                    denom = p.sum() + g.sum()
                    if denom > 0:  # Absent reference + false positive is zero; both absent is omitted.
                        values.append(float(2 * (p & g).sum() / denom))
        model.train()
        return sum(values) / len(values) if values else 0.0

    model.train()
    while step < cfg["iterations"]:
        for batch in train_loader:
            optimizer.zero_grad(set_to_none=True)
            x, y = batch["image"].to(device), batch["label"].to(device)
            with torch.amp.autocast("cuda", enabled=cfg["amp"]):
                loss = loss_fn(model(x), y)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            step += 1
            record = {"step": step, "loss": float(loss.detach())}
            if step % cfg["validation_every"] == 0 or step == cfg["iterations"]:
                score = validate()
                record["validation_foreground_dice"] = score
                if score > best:
                    best = score
                    save("best.pt")
                save("last.pt")
            with (output / "training.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(record) + "\n")
            if step % 10 == 0 or "validation_foreground_dice" in record:
                print(json.dumps(record), flush=True)
            if step >= cfg["iterations"]:
                break
    save("final.pt")
    print(f"Saved final weights at exactly {step} optimizer steps: {output / 'final.pt'}")


if __name__ == "__main__":
    main()
