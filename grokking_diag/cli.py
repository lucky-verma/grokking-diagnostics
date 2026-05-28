"""Command-line interface for grokking-diag.

Usage:
    grokking-diag info
    grokking-diag predict --features '{"wd": 0.1, ...}'
    grokking-diag analyze <checkpoint.pt>
"""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .predictor import RetentionPredictor


def _info():
    print(f"grokking-diag v{__version__}")
    print("Companion paper: Verma 2026 'Weight Decay Regimes in Grokking Transformers'")
    print("Source: https://github.com/lucky-verma/grokking-diagnostics")
    print("Dataset: https://huggingface.co/datasets/lucky-verma/grokking-diagnostics-runs")


def _predict(features_json: str):
    features = json.loads(features_json)
    p = RetentionPredictor.load_default()
    out = p.predict(features)
    print(json.dumps(out, indent=2))


def _analyze(ckpt_path: str):
    print(
        f"analyze {ckpt_path}: checkpoint adapters are not bundled in v0.1. "
        "Use the Python API with attention tensors, or run `grokking-diag predict` "
        "for the shipped aggregate-feature interface."
    )
    return 1


def main():
    ap = argparse.ArgumentParser(prog="grokking-diag")
    ap.add_argument("--version", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    sp = sub.add_parser("info")
    sp = sub.add_parser("predict")
    sp.add_argument("--features", required=True, help="JSON dict of features")
    sp = sub.add_parser("analyze")
    sp.add_argument("checkpoint")

    args = ap.parse_args()
    if args.version:
        print(__version__)
        return
    if args.cmd == "info" or args.cmd is None:
        _info()
    elif args.cmd == "predict":
        _predict(args.features)
    elif args.cmd == "analyze":
        sys.exit(_analyze(args.checkpoint))


if __name__ == "__main__":
    main()
