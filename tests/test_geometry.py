"""CPU preprocessing checks; these do not exercise the Mamba model."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
import numpy as np

HAS_DEPS = all(importlib.util.find_spec(p) for p in ("torch", "monai", "nibabel"))


@unittest.skipUnless(HAS_DEPS, "Requires torch, monai and nibabel")
class GeometryTests(unittest.TestCase):
    def test_inverse_prediction_restores_input_grid(self):
        import nibabel as nib
        from hmci_net.config import load_config
        from hmci_net.data import make_transforms, restore_mask
        cfg = load_config(Path(__file__).resolve().parents[1] / "configs/whole_tumor.json")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = np.full((13, 17, 19), -1000, dtype=np.float32)
            image[2:11, 3:14, 4:16] = 60
            label = np.zeros(image.shape, dtype=np.uint8)
            label[4:9, 5:12, 6:14] = 1
            affine = np.diag([-2.0, 1.5, 3.0, 1.0])
            affine[:3, 3] = [40, -13, 22]
            for name, arr in (("image", image), ("label", label)):
                nib.save(nib.Nifti1Image(arr, affine), root / f"{name}.nii.gz")
            transform = make_transforms(cfg)
            sample = transform({"image": str(root / "image.nii.gz"), "label": str(root / "label.nii.gz")})
            restored = restore_mask(sample["label"].as_tensor().clone(), sample["image"], transform)
            self.assertEqual(tuple(restored.shape), (1, *image.shape))
            self.assertTrue(np.allclose(restored.affine.numpy(), affine, atol=1e-4))
            p = restored[0].numpy() > 0.5
            self.assertGreater(2 * (p & (label > 0)).sum() / (p.sum() + label.sum()), 0.95)

    def test_reject_geometry_and_label_errors(self):
        import torch
        from monai.data import MetaTensor
        from hmci_net.data import CheckLabels
        image = MetaTensor(torch.zeros((1, 4, 4, 4)), affine=torch.eye(4))
        label = MetaTensor(torch.zeros((1, 4, 4, 4)), affine=torch.eye(4))
        label.affine[0, 3] = 5
        with self.assertRaisesRegex(ValueError, "affines"):
            CheckLabels(2)({"image": image, "label": label})
        label.affine = image.affine.clone()
        label[0, 0, 0, 0] = 2
        with self.assertRaisesRegex(ValueError, "labels"):
            CheckLabels(2)({"image": image, "label": label})


if __name__ == "__main__":
    unittest.main()
