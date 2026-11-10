"""Check Python syntax, source hashes and relative Markdown targets without ML dependencies."""
import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = list(ROOT.rglob("*.py"))
    for p in files:
        ast.parse(p.read_text(encoding="utf-8-sig"), filename=str(p))
    source_files = json.loads((ROOT / "docs/source_manifest.json").read_text())
    for item in source_files:
        p = ROOT / item["file"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item["sha256"], f"Changed original source: {p}"
    for p in ROOT.rglob("*.md"):
        targets = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding="utf-8"))
        for target in targets:
            target = target.split("#", 1)[0]
            if target and "://" not in target:
                assert (p.parent / target).exists(), f"Broken link in {p}: {target}"
    figure_root = ROOT / "docs/figures"
    figures = {p.relative_to(figure_root).as_posix() for p in figure_root.rglob("*") if p.is_file()}
    expected = {
        "architecture.svg", "segmentation_comparison.png", "qualitative_segmentation.png",
        "segmentation_robustness.png", "journal_cohort_performance.png", "journal_cohort_performance.svg",
    }
    assert figures == expected, f"Unexpected/missing figure files: {figures ^ expected}"
    result_files = {p.name for p in (ROOT / "docs/results").iterdir() if p.is_file()}
    assert result_files == {"journal_results.json", "reported_segmentation_results.json"}, result_files
    homepage = (ROOT / "README.md").read_text(encoding="utf-8")
    images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', homepage)
    expected_images = {f"docs/figures/{name}" for name in expected if name != "journal_cohort_performance.svg"}
    assert len(images) == 5 and set(images) == expected_images, "Homepage must show all five journal figures exactly once."
    assert not list(ROOT.rglob("*.docx"))
    assert not list(ROOT.rglob("*.tiff"))
    print(f"PASS: {len(files)} Python syntax checks; {len(source_files)} original-source hashes; "
          f"5 homepage figures / {len(figures)} assets; journal result files; Markdown links.")


if __name__ == "__main__":
    main()
