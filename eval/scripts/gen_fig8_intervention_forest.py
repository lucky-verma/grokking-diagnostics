#!/usr/bin/env python3
"""Generate Figure 8: intervention paired peak-sigma_H forest plot."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42})

OKABE_ITO = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
}


def main() -> None:
    paper_dir = Path(__file__).resolve().parents[2]
    with (paper_dir / "eval/intervention_stats.json").open() as f:
        data = json.load(f)

    comparisons = [
        ("B-A", "B_minus_A", "Head reinit - control", OKABE_ITO["blue"]),
        ("C-A", "C_minus_A", "Weight clip - control", OKABE_ITO["orange"]),
        ("C-B", "C_minus_B", "Weight clip - head reinit", OKABE_ITO["green"]),
    ]
    rows = []
    for short, key, label, color in comparisons:
        stats = data["paired_tests"][key]["peak_ent"]
        lo, hi = stats["ci_95_diff"]
        rows.append(
            {
                "short": short,
                "label": label,
                "mean": stats["mean_diff"],
                "lo": lo,
                "hi": hi,
                "n": stats["n"],
                "color": color,
            }
        )

    fig, ax = plt.subplots(figsize=(4.3, 2.3))
    y_positions = list(range(len(rows)))[::-1]
    for y, row in zip(y_positions, rows):
        xerr = [[row["mean"] - row["lo"]], [row["hi"] - row["mean"]]]
        ax.errorbar(
            row["mean"],
            y,
            xerr=xerr,
            fmt="o",
            color=row["color"],
            ecolor=row["color"],
            elinewidth=2.0,
            capsize=4,
            markersize=5.5,
        )
        ax.text(
            row["hi"] + 0.004,
            y,
            f"n={row['n']}",
            va="center",
            ha="left",
            fontsize=8,
            color="#333333",
        )

    ax.axvline(0, color="#666666", linewidth=1.0, linestyle="--", zorder=0)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"{r['short']}: {r['label']}" for r in rows], fontsize=8)
    ax.set_xlabel(r"Paired change in peak $\sigma_H$", fontsize=9)
    ax.set_xticks([-0.05, 0.0, 0.05])
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(-0.065, 0.055)
    ax.set_ylim(-0.45, len(rows) - 0.55)
    fig.tight_layout()

    out_base = paper_dir / "figures/fig8_intervention_forest"
    fig.savefig(out_base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out_base.with_suffix(".png"), dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
