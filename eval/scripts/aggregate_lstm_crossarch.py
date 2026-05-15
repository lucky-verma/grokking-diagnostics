#!/usr/bin/env python3
"""Cross-arch aggregator: logistic lambda_c + bootstrap CI.

Reads 70 cross-architecture run JSONs and produces a single
aggregate entry compatible with eval/multitask_logistic.json schema:
  {wd_c, ci_95, n_grok, n_points, n_bins, bins}

Run:
  python3 eval/scripts/aggregate_lstm_crossarch.py \\
      --src cross-arch/lstm/ \\
      --merge eval/multitask_logistic.json

Mamba:
  python3 .../aggregate_lstm_crossarch.py \\
      --src cross-arch/mamba/modadd-exp4/ \\
      --prefix Mamba mod-add probe --key mamba_4L_d128_mod_add \\
      --merge eval/multitask_logistic.json
"""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


def logistic(logw, log_wd_c, k):
    return 1.0 / (1.0 + np.exp(-k * (logw - log_wd_c)))


def load_runs(src_dir: Path, prefix: str):
    runs = []
    for sub in sorted(src_dir.glob(f"{prefix}_*")):
        json_path = sub / f"{sub.name}.json"
        if not json_path.exists():
            json_path = sub
        try:
            d = json.loads(Path(json_path).read_text())
        except Exception:
            continue
        config = d.get("config", {})
        wd = config.get("wd")
        seed = config.get("seed")
        grok_ep = d.get("grok_epoch")
        final = d.get("final_test_acc", 0.0)
        groked = (grok_ep is not None) or (final > 0.95)
        runs.append({"wd": wd, "seed": seed, "grok": groked,
                     "grok_epoch": grok_ep, "final_test_acc": final,
                     "label": sub.name})
    return runs


def fit_logistic(records):
    by_wd = defaultdict(list)
    for r in records:
        if r["wd"] is None or r["wd"] <= 0 or r["wd"] > 5:
            continue
        by_wd[r["wd"]].append(int(r["grok"]))
    wds = np.array(sorted(by_wd))
    p = np.array([np.mean(by_wd[w]) for w in wds])
    logw = np.log10(wds)
    n_grok = sum(int(r["grok"]) for r in records)
    n_points = len(records)

    try:
        popt, _ = curve_fit(logistic, logw, p,
                            p0=[np.log10(0.05), 5.0], maxfev=5000)
    except Exception as e:
        return dict(error=str(e), n_grok=n_grok, n_points=n_points,
                    bins=[{"wd": float(w), "p_grok": float(pp),
                           "n": len(by_wd[w])} for w, pp in zip(wds, p)])
    log_wd_c, k = popt
    wd_c = 10 ** log_wd_c

    rng = random.Random(42)
    wdcs = []
    items = [(w, g) for w, gs in by_wd.items() for g in gs]
    N = len(items)
    for _ in range(1500):
        samp = [items[rng.randrange(N)] for _ in range(N)]
        bb = defaultdict(list)
        for w, g in samp:
            bb[w].append(g)
        wws = np.array(sorted(bb))
        pps = np.array([np.mean(bb[w]) for w in wws])
        try:
            po, _ = curve_fit(logistic, np.log10(wws), pps,
                              p0=[log_wd_c, k], maxfev=2000)
            wdcs.append(10 ** po[0])
        except Exception:
            continue
    lo, hi = (np.quantile(wdcs, [0.025, 0.975]).tolist()
              if wdcs else (None, None))

    return dict(
        wd_c=float(wd_c), k=float(k),
        ci_95=[float(lo), float(hi)] if lo is not None else None,
        n_bootstrap_ok=len(wdcs),
        n_grok=n_grok, n_points=n_points,
        n_bins=len(wds),
        bins=[dict(wd=float(w), p_grok=float(pp), n=len(by_wd[w]))
              for w, pp in zip(wds, p)],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True,
                    help="dir containing <prefix>_*/<prefix>_*.json results")
    ap.add_argument("--merge", type=Path,
                    help="optional: merge into multitask_logistic.json")
    ap.add_argument("--prefix", default="LSTM probe",
                    help="run directory prefix, e.g. LSTM probe or Mamba mod-add probe")
    ap.add_argument("--key", default="lstm_4L_h512_mod_add")
    ap.add_argument("--out", type=Path,
                    help="optional: write standalone JSON here")
    args = ap.parse_args()

    runs = load_runs(args.src, args.prefix)
    print(f"loaded {len(runs)} runs from {args.src}")
    if not runs:
        raise SystemExit("no runs found")
    fit = fit_logistic(runs)
    print(json.dumps(fit, indent=2, default=str))

    if args.merge and args.merge.exists():
        existing = json.loads(args.merge.read_text())
        existing[args.key] = fit
        args.merge.write_text(json.dumps(existing, indent=2))
        print(f"merged into {args.merge} under key {args.key}")
    if args.out:
        args.out.write_text(json.dumps(fit, indent=2))
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
