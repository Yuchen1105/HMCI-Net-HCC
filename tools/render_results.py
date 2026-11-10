"""Plot supplied aggregate results; never simulate patient-level measurements."""
import json
import re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/figures"
TEAL, GOLD = "#117f80", "#b77a16"


def read(name):
    return json.loads((ROOT / "docs/results" / name).read_text(encoding="utf-8"))


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#c7d0da")
    ax.grid(axis="x", color="#e8edf2", zorder=0)
    ax.tick_params(colors="#34485d", labelsize=10)


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=190, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def validation_plot():
    rows = read("journal_results.json")["cohort_results"]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 6.2), sharey=True)
    fig.subplots_adjust(left=.24, right=.97, top=.78, bottom=.19, wspace=.18)
    fig.suptitle("Segmentation across internal and external cohorts", x=.035, y=.97,
                 ha="left", fontsize=19, weight="bold", color="#152b43")
    fig.text(.035, .91, "Journal manuscript, Table 3  |  Dots: reported DSC; whiskers: interquartile ranges",
             fontsize=11, color="#586b80")
    labels = [("Whole tumor" if r["task"] == "whole_tumor" else "Enhancing tumor") + " / " + r["cohort"] for r in rows]
    for ax, field, title in zip(axes, ("patient_dsc", "tumor_dsc"), ("Patient-wise DSC", "Tumor-wise DSC")):
        style(ax)
        for i, row in enumerate(rows):
            value, low, high = map(float, re.findall(r"\d+\.\d+", row[field]))
            color = TEAL if row["task"] == "whole_tumor" else GOLD
            ax.errorbar(value, i, xerr=[[value-low], [high-value]], fmt="o", color=color,
                        capsize=4, linewidth=2.2, markersize=7, zorder=3)
            ax.annotate(f"{value:.3f}", (value, i), xytext=(0, 11), textcoords="offset points",
                        ha="center", fontsize=10, weight="bold", color=color)
        ax.set_xlim(0, 1.02)
        ax.set_xticks(np.arange(0, 1.01, .2))
        ax.set_yticks(range(len(rows)))
        ax.set_title(title, loc="left", fontsize=13, weight="bold", pad=20)
        ax.set_xlabel("DSC (0–1)", fontsize=10)
        ax.axhline(4.5, color="#d5dee7", linestyle="--", linewidth=1)
    axes[0].set_yticklabels(labels)
    axes[0].set_ylim(len(rows)-.4, -.7)
    fig.legend([Line2D([0],[0],color=TEAL,marker="o"),Line2D([0],[0],color=GOLD,marker="o")],
               ["Whole tumor", "Enhancing tumor"], loc="lower center", bbox_to_anchor=(.57,.04),
               ncol=2, frameon=False)
    fig.text(.035,.015,"Replotted from the supplied table. IQRs describe distributions; they are not confidence intervals.",
             fontsize=10,color="#586b80")
    save(fig,"journal_cohort_performance")


if __name__ == "__main__":
    plt.rcParams.update({"font.family":"DejaVu Sans","svg.fonttype":"none"})
    validation_plot()
    print("Rendered the journal Table 3 cohort figure in PNG and editable SVG.")
