#!/usr/bin/env python3
"""Generate Figure 9: multi-task grok-rate heatmap (4 ops x 2 scales x 7 WDs)."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42})

OPS = ["mod_add", "mod_sub", "mod_mul", "mod_div"]
SCALES = ["small", "medium"]
WDS = [0.003, 0.006, 0.015, 0.020, 0.030, 0.050, 0.070]
OP_LABELS = {
    "mod_add": r"$\mathrm{mod}_+$",
    "mod_sub": r"$\mathrm{mod}_-$",
    "mod_mul": r"$\mathrm{mod}_\times$",
    "mod_div": r"$\mathrm{mod}_\div$",
}


def main() -> None:
    paper_dir = Path(__file__).resolve().parents[2]
    with (paper_dir / "eval/multitask_summary.json").open() as f:
        data = json.load(f)

    grid = data["multitask_full_grid"]
    rows = [(op, sc) for op in OPS for sc in SCALES]
    matrix = np.full((len(rows), len(WDS)), np.nan)
    annot = [["" for _ in WDS] for _ in rows]

    for i, (op, sc) in enumerate(rows):
        for j, wd in enumerate(WDS):
            key_g = f"{wd:g}"  # 0.020 -> '0.02', 0.070 -> '0.07'
            key = f"{op}__{sc}__wd{key_g}"
            cell = grid.get(key)
            if cell is None:
                continue
            num, den = cell["grok_rate"].split("/")
            matrix[i, j] = float(num) / float(den)
            annot[i][j] = cell["grok_rate"]

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    im = ax.imshow(matrix, vmin=0.0, vmax=1.0, cmap="cividis", aspect="auto")

    ax.set_xticks(range(len(WDS)))
    ax.set_xticklabels([f"{w:g}" for w in WDS], fontsize=8)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{OP_LABELS[op]} {sc}" for op, sc in rows], fontsize=9)
    ax.set_xlabel(r"Weight decay $\lambda$", fontsize=9)

    for i in range(len(rows)):
        for j in range(len(WDS)):
            v = matrix[i, j]
            if np.isnan(v):
                continue
            color = "white" if v < 0.45 else "black"
            ax.text(j, i, annot[i][j], ha="center", va="center",
                    color=color, fontsize=7.5, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.038, pad=0.02)
    cb.set_label("Grok rate (n=5 per cell)", fontsize=8)
    cb.ax.tick_params(labelsize=8)

    fig.tight_layout()

    out_base = paper_dir / "figures/fig9_multitask_heatmap"
    fig.savefig(out_base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out_base.with_suffix(".png"), dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
