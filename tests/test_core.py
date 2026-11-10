import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from hmci_net.config import load_config, paired_files, training_files
from hmci_net.metrics import overlap_metrics

ROOT = Path(__file__).resolve().parents[1]


class ConfigurationTests(unittest.TestCase):
    def test_example_configs(self):
        for p in (ROOT / "configs").glob("*.json"):
            self.assertEqual(load_config(p)["patch_size"], [128] * 3)

    def test_reject_nonmatching_scan_grid(self):
        cfg = load_config(ROOT / "configs/lits.json")
        cfg["patch_size"] = [64] * 3
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text(json.dumps(cfg))
            with self.assertRaisesRegex(ValueError, "fixed scan grids"):
                load_config(p)

    def test_missing_label_is_not_silently_zipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for d in ("imagesTr", "labelsTr"):
                (root / d).mkdir()
            (root / "imagesTr/a.nii.gz").touch()
            (root / "labelsTr/b.nii.gz").touch()
            with self.assertRaisesRegex(ValueError, "filenames differ"):
                paired_files(root, "Tr")

    def test_disallow_split_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for d in ("imagesTr", "labelsTr", "imagesVal", "labelsVal"):
                (root / d).mkdir()
                (root / d / "a.nii.gz").touch()
            with self.assertRaisesRegex(ValueError, "overlap"):
                training_files(root)


class MetricTests(unittest.TestCase):
    def test_perfect_prediction(self):
        self.assertEqual(overlap_metrics([0, 1], [0, 1])["dsc"], 1)

    def test_false_positive_without_reference_is_zero(self):
        result = overlap_metrics([0, 1], [0, 0])
        self.assertEqual(result["dsc"], 0)
        self.assertIsNone(result["patient_detected"])

    def test_empty_masks_are_undefined(self):
        self.assertIsNone(overlap_metrics([0], [0])["dsc"])

    def test_one_voxel_is_enough_for_patient_detection(self):
        result = overlap_metrics([1, 0, 0], [1, 1, 0])
        self.assertTrue(result["patient_detected"])
        self.assertAlmostEqual(result["dsc"], 2 / 3)
        self.assertEqual(result["ji"], 0.5)

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            overlap_metrics(np.zeros((2, 2)), np.zeros(4))


if __name__ == "__main__":
    unittest.main()
