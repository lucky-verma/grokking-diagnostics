#!/usr/bin/env python3
"""
Download the modular-arithmetic JSON dataset from HuggingFace Hub.

Pulls 1120 transformer-cohort per-run JSONs (0.82M, 19M, 85M models; mod_+/-/×/÷;
seven weight-decay bins; 10K-epoch and 20K-epoch horizons) plus 350 cross-architecture
scope-probe records (70 MLP, 70 LSTM, 210 Mamba) and the per-grid aggregate fits.
Each per-run JSON contains training-step metrics (test_acc, train_acc, mean_sim,
entropy_std, weight_norm, attention dynamics) on the matched cell configuration.

Usage:
    python scripts/download_dataset.py
    python scripts/download_dataset.py --cohort canonical
    python scripts/download_dataset.py --to-dir ./data/raw_jsons
"""
from __future__ import annotations

import argparse
from pathlib import Path

REPO_ID = "lucky-verma/grokking-diagnostics-runs"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--to-dir", type=Path, default=Path("data/raw_jsons"),
                    help="Local directory to store downloaded JSONs")
    ap.add_argument("--cohort", choices=["all", "canonical", "transformer",
                                          "multitask", "intervention", "cross-seed",
                                          "cross-arch", "aggregates"],
                    default="all", help="Which cohort subtree to download "
                                        "(matches HuggingFace folder layout)")
    ap.add_argument("--allow-patterns", nargs="*", default=None,
                    help="Custom HF allow_patterns override")
    args = ap.parse_args()

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        raise SystemExit(
            "huggingface_hub not installed. Run: pip install huggingface_hub"
        )

    # Folder paths match the live HuggingFace dataset layout.
    cohort_patterns = {
        "all":          ["*.json"],
        "canonical":    ["canonical/**/*.json"],
        "transformer":  ["transformer/**/*.json"],
        "multitask":    ["e9-multitask-transformer/**/*.json"],
        "intervention": ["e12-interventions/**/*.json"],
        "cross-seed":   ["e13-crossseed-checkpoints/**/*.json",
                         "e13-canonical-checkpoints/**/*.json"],
        "cross-arch":   ["cross-arch/**/*.json"],
        "aggregates":   ["aggregates/**/*.json"],
    }
    patterns = args.allow_patterns or cohort_patterns[args.cohort]

    args.to_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {args.cohort} cohort from {REPO_ID} ...")
    print(f"Patterns: {patterns}")
    print(f"Target:   {args.to_dir}")

    path = snapshot_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        local_dir=str(args.to_dir),
        allow_patterns=patterns,
    )
    print(f"Downloaded to: {path}")

    n = sum(1 for _ in args.to_dir.rglob("*.json"))
    print(f"Total JSONs in target dir: {n}")


if __name__ == "__main__":
    main()
