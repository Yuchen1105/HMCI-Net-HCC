"""Transforms derived from the original LiTS example; see docs/reproducibility.md."""


class CheckLabels:
    def __init__(self, num_classes):
        self.num_classes = num_classes

    def __call__(self, sample):
        import torch
        label = sample["label"]
        if not torch.isfinite(label).all() or not torch.equal(label, label.round()):
            raise ValueError("Masks must contain finite integer class IDs.")
        if label.min() < 0 or label.max() >= self.num_classes:
            raise ValueError(f"Mask labels must be between 0 and {self.num_classes - 1}.")
        if sample["image"].shape != label.shape:
            raise ValueError("Image and mask shapes differ.")
        if not torch.allclose(sample["image"].affine, label.affine, atol=1e-4, rtol=0):
            raise ValueError("Image and mask affines differ; align them before training.")
        return sample


def make_transforms(config, training=False, labeled=True):
    from monai.transforms import (
        Compose, LoadImaged, EnsureChannelFirstd, Orientationd, Spacingd,
        ScaleIntensityRanged, CropForegroundd, SpatialPadd, RandCropByPosNegLabeld,
        RandFlipd, RandRotate90d, RandShiftIntensityd, RandAffined, EnsureTyped,
    )
    keys = ["image", "label"] if labeled else ["image"]
    transforms = [LoadImaged(keys), EnsureChannelFirstd(keys)]
    if labeled:
        transforms.append(CheckLabels(config["num_classes"]))
    transforms += [
        Orientationd(keys, axcodes="RAS"),
        Spacingd(keys, pixdim=config["spacing"], mode=("bilinear", "nearest") if labeled else "bilinear"),
        ScaleIntensityRanged("image", a_min=config["intensity_window"][0],
                             a_max=config["intensity_window"][1], b_min=0, b_max=1, clip=True),
        CropForegroundd(keys, source_key="image", allow_smaller=True),
    ]
    if training:
        transforms += [
            SpatialPadd(keys, spatial_size=config["patch_size"]),
            RandCropByPosNegLabeld(keys, label_key="label", spatial_size=config["patch_size"],
                                  pos=1, neg=1, num_samples=config["crops_per_case"],
                                  image_key="image", image_threshold=0),
            *[RandFlipd(keys, prob=0.5, spatial_axis=i) for i in range(3)],
            RandRotate90d(keys, prob=0.2, max_k=3),
            RandShiftIntensityd("image", offsets=0.1, prob=0.5),
            RandAffined(keys, mode=("bilinear", "nearest"), prob=0.2,
                        spatial_size=config["patch_size"], rotate_range=(0, 0, 0.15),
                        scale_range=(0.1, 0.1, 0.1)),
        ]
    transforms.append(EnsureTyped(keys, track_meta=True))
    return Compose(transforms)


def restore_mask(mask, image, transform):
    """Invert a channel-first class mask using the image's spatial history."""
    from monai.data import MetaTensor
    from monai.transforms import Invertd
    # Invertd selects MetaTensor history only when the prediction is also a MetaTensor.
    prediction = MetaTensor(mask.detach().cpu().float())
    inverse = Invertd(keys="pred", transform=transform, orig_keys="image", nearest_interp=True, to_tensor=True)
    return inverse({"pred": prediction, "image": image})["pred"]
