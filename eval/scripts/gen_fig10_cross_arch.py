#!/usr/bin/env python3
"""Generate Figure 10: cross-architecture wd_c comparison."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42})

BAR_COLORS = ["#0072B2", "#56B4E9", "#E69F00", "#009E73", "#CC79A7"]


def main() -> None:
    paper_dir = Path(__file__).resolve().parents[2]
    with (paper_dir / "eval/multitask_logistic.json").open() as f:
        data = json.load(f)

    keys = [
        ("transformer_small_pooled_4ops", "Transformer\nsmall"),
        ("transformer_medium_pooled_4ops", "Transformer\nmedium"),
        ("mlp_4L_h512_mod_add", "4L MLP\nh=512"),
    ]
    if "lstm_4L_h512_mod_add" in data:
        keys.append(("lstm_4L_h512_mod_add", "4L LSTM\nh=512"))
    if "mamba_4L_d128_mod_add" in data:
        keys.append(("mamba_4L_d128_mod_add", "4L Mamba\n$d=128$"))

    means = []
    lows = []
    highs = []
    ns = []
    for key, _ in keys:
        row = data[key]
        means.append(row["wd_c"])
        lows.append(row["ci_95"][0])
        highs.append(row["ci_95"][1])
        ns.append((row["n_grok"], row["n_points"]))

    x = np.arange(len(keys))
    yerr = np.array([[m - lo for m, lo in zip(means, lows)], [hi - m for m, hi in zip(means, highs)]])

    width = 5.2 if len(keys) >= 5 else (4.3 if len(keys) >= 4 else 3.8)
    fig, ax = plt.subplots(figsize=(width, 2.65))
    ax.bar(x, means, color=BAR_COLORS[:len(keys)], width=0.62)
    ax.errorbar(x, means, yerr=yerr, fmt="none", ecolor="#222222", elinewidth=1.3, capsize=4)
    for i, (ng, n) in enumerate(ns):
        ax.text(i, highs[i] + 0.003, f"{ng}/{n}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in keys], fontsize=8)
    ax.set_ylabel(r"Logistic $\mathrm{wd}_c$", fontsize=9)
    # Auto-extend y axis if any bar exceeds the existing 0.068 ceiling.
    ymax = max(0.068, max(h + 0.008 for h in highs))
    ax.set_ylim(0, ymax)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    out_base = paper_dir / "figures/fig10_cross_arch"
    fig.savefig(out_base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out_base.with_suffix(".png"), dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
