"""Draw an editable SVG overview; no measured results are synthesized."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]


def main():
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="850" viewBox="0 0 1280 850" role="img" aria-label="HMCI-Net architecture overview">',
           '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="#64748b" stroke-width="1.2"/></marker></defs>',
           '<rect width="1280" height="850" rx="20" fill="#f8fafc"/>']

    def text(x, y, s, size=16, color="#23344c", weight="400", anchor="middle"):
        svg.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(s)}</text>')

    def box(x, y, w, title, sub, fill="#e6f5f2", stroke="#95cfc4"):
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="66" rx="12" fill="{fill}" stroke="{stroke}"/>')
        text(x + w / 2, y + 27, title, 17, weight="700")
        text(x + w / 2, y + 49, sub, 13)

    def arrow(path, dashed=False):
        dash = 'stroke-dasharray="6 5"' if dashed else ""
        svg.append(f'<path d="{path}" stroke="#64748b" stroke-width="1.6" fill="none" marker-end="url(#arrow)" {dash}/>')

    text(48, 49, "HMCI-Net", 30, "#12263e", "700", "start")
    text(48, 80, "Volumetric segmentation on contrast-enhanced CT", 17, "#62748a", anchor="start")
    text(1232, 48, "METHOD OVERVIEW", 12, "#268270", "700", "end")
    box(30, 130, 220, "CT volume", "Single-channel input", "#eaf0f9", "#b8c9e1")
    box(300, 130, 250, "Shallow convolution", "48 channels · full resolution", "#eaf0f9", "#b8c9e1")
    arrow("M250 163 L300 163")
    arrow("M140 196 L140 263 L300 263")
    text(425, 117, "ENCODER", 12, "#268270", "700")
    text(860, 117, "DECODER", 12, "#987329", "700")
    for i, (channels, scale) in enumerate([(48, 64), (96, 32), (192, 16), (384, 8)]):
        y = 230 + 100 * i
        box(300, y, 250, f"HM + MSFM · Stage {i + 1}", f"{channels} channels · {scale}³ features")
        if i < 3:
            arrow(f"M425 {y+66} L425 {y+100}")
    for i, (channels, scale) in enumerate([(48, 128), (96, 64), (192, 32), (384, 16)]):
        y = 130 + i * 100
        box(750, y, 220, f"Decoder · {scale}³", f"Upsample + skip · {channels} channels", "#fff4dc", "#dec58d")
        arrow(f"M550 {y+33} L750 {y+33}", True)
        text(650, y + 22, "skip" if i == 0 else "skip projection", 12, "#62748a")
        if i > 0:
            arrow(f"M860 {y} L860 {y-34}")
    box(1045, 130, 205, "Segmentation", "Voxel-wise class mask", "#eaf0f9", "#b8c9e1")
    arrow("M970 163 L1045 163")
    box(695, 530, 365, "Cross-Directional Interaction", "Directional gates · cross-branch weighting", "#eaf0f9", "#b8c9e1")
    arrow("M550 563 L695 563")
    arrow("M860 530 L860 496")
    text(878, 620, "CDI bottleneck: 384 → 768 channels", 13, "#62748a")
    text(140, 376, "ENCODER BLOCK", 12, "#268270", "700")
    text(140, 408, "Helical Mamba", 18, "#12263e", "700")
    text(140, 435, "Forward + reverse scans", 13, "#62748a")
    arrow("M140 454 L140 481")
    text(140, 511, "Structural modulation", 17, "#12263e", "700")
    text(140, 538, "Local + volumetric features", 13, "#62748a")
    svg.append('<rect x="48" y="670" width="1184" height="122" rx="12" fill="#ffffff" stroke="#e1e7ef"/>')
    text(74, 701, "ONE ARCHITECTURE · SEPARATE TASK CHECKPOINTS", 13, "#268270", "700", "start")
    for x, a, b in [(74, "Whole-tumor segmentation", "Background + full lesion"), (480, "Enhancing-tumor segmentation", "Background + enhancing region"), (950, "128 × 128 × 128", "Sliding-window patch")]:
        text(x, 733, a, 18, weight="700", anchor="start")
        text(x, 760, b, 14, "#62748a", anchor="start")
    text(48, 824, "Method summary; source uses historical class names. See reproducibility notes for the unresolved scan-direction discrepancy.", 12, "#62748a", anchor="start")
    svg.append("</svg>")
    (ROOT / "docs/figures/architecture.svg").write_text("\n".join(svg), encoding="utf-8")


if __name__ == "__main__":
    main()
