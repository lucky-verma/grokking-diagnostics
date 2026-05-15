#!/usr/bin/env python3
"""
Verify public paper-cited numerical claims against shipped aggregate JSONs.

The GitHub artifact repo intentionally ships small aggregate JSONs rather than
the full raw-run mirror. Raw per-run records live in the companion Hugging Face
dataset; this script is the lightweight CI check for the public aggregate
surface.

Exits 0 if all checks PASS; non-zero on any mismatch.

Usage:
    python scripts/verify_numerical_claims.py
    python scripts/verify_numerical_claims.py --data-dir ./eval/aggregates
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def check(label, claim, actual, tol_abs=0.0005, tol_rel=0.01):
    claim_n = float(claim)
    actual_n = float(actual)
    if claim_n == 0 or actual_n == 0:
        diff = abs(claim_n - actual_n)
        match = diff <= tol_abs
    else:
        diff = abs(claim_n - actual_n)
        rel = abs(diff / max(abs(claim_n), abs(actual_n)))
        match = diff <= tol_abs or rel <= tol_rel
    sym = "✅" if match else "❌"
    return match, f"  {sym} {label:42} | paper={claim_n:>10} | data={actual_n:>10} | Δ={diff:.5f}"


def find_json(label: str, data_dirs: list[Path]):
    """Find an aggregate JSON file matching the label across known locations."""
    for data_dir in data_dirs:
        for candidate in [data_dir / f"{label}.json",
                          data_dir / "aggregates" / f"{label}.json",
                          data_dir.parent / f"{label}.json"]:
            if candidate.exists():
                return candidate
    return None


def load_required(label: str, data_dirs: list[Path]):
    path = find_json(label, data_dirs)
    if path is None:
        searched = ", ".join(str(p) for p in data_dirs)
        raise FileNotFoundError(f"{label}.json not found; searched: {searched}")
    return json.loads(path.read_text()), path


def candidate_data_dirs(requested: Path) -> list[Path]:
    dirs = [
        requested,
        Path("eval/aggregates"),
        Path("eval"),
        Path("data/raw_jsons/aggregates"),
        Path("data/raw_jsons"),
    ]
    seen = set()
    unique = []
    for data_dir in dirs:
        resolved = data_dir.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(data_dir)
    return unique


def add_claim(fails, label, claim, actual, tol_abs=0.0005, tol_rel=0.01):
    ok, msg = check(label, claim, actual, tol_abs=tol_abs, tol_rel=tol_rel)
    print(msg)
    if not ok:
        fails.append(label)
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=Path("eval/aggregates"),
                    help="Directory containing shipped aggregate JSONs")
    ap.add_argument("--skip-gpu", action="store_true",
                    help="Compatibility flag; no GPU checks are run in this public artifact")
    args = ap.parse_args()

    data_dirs = candidate_data_dirs(args.data_dir)
    print("[Aggregate JSONs] Search path:")
    for data_dir in data_dirs:
        marker = "exists" if data_dir.exists() else "missing"
        print(f"  - {data_dir} ({marker})")

    fails = []

    # Pure formula checks (no aggregate JSONs needed)
    print()
    print("[Formula] AdamW relaxation: lambda_c = -ln(1-p) / (eta*kappa*T)")
    print("    canonical: eta=1e-3, kappa=18.6, T=20000")
    eta, kappa, T = 1e-3, 18.6, 20000
    sensitivity_paper = {0.50: 0.0019, 0.70: 0.0032, 0.90: 0.0062, 0.95: 0.0081, 0.99: 0.0124}
    checked = 0
    for p_relax, claim in sensitivity_paper.items():
        derived = -math.log(1 - p_relax) / (eta * kappa * T)
        add_claim(fails, f"sensitivity p={p_relax}", claim, derived, tol_abs=0.0005)
        checked += 1

    print()
    print("[Shipped aggregate checks]")
    try:
        a5, p = load_required("a5_wdc_fit", data_dirs)
        print(f"  using {p}")
        for label, expected, actual, tol in [
            ("lambda_c value", 0.0158, a5["wd_c_fit"]["wd_c"], 0.0005),
            ("lambda_c CI lower", 0.0109, a5["wd_c_fit"]["wd_c_ci"][0], 0.0005),
            ("lambda_c CI upper", 0.0200, a5["wd_c_fit"]["wd_c_ci"][1], 0.0005),
            ("logistic n_records", 210, a5["n_records"], 0.0),
            ("nu value", 0.757, a5["nu_fit"]["nu"], 0.001),
            ("nu CI lower", 0.725, a5["nu_fit"]["nu_ci"][0], 0.001),
            ("nu CI upper", 0.799, a5["nu_fit"]["nu_ci"][1], 0.001),
            ("nu n_points", 140, a5["nu_fit"]["n_points"], 0.0),
        ]:
            add_claim(fails, label, expected, actual, tol_abs=tol)
            checked += 1

        a3, p = load_required("a3_perm_test", data_dirs)
        print(f"  using {p}")
        for label, expected, actual in [
            ("null amp mean", 0.087, a3["null_amp_stats"]["mean"]),
            ("amp perm p", 0.009, a3["amplitude_perm"]["p"]),
        ]:
            add_claim(fails, label, expected, actual, tol_abs=0.001)
            checked += 1

        a7, p = load_required("a7_cohens_d", data_dirs)
        print(f"  using {p}")
        add_claim(fails, "Cohen's d (add vs random)", 1.11,
                  a7["add_vs_random_amplitude"]["d"], tol_abs=0.01)
        checked += 1

        c1, p = load_required("c1_empirical_validation", data_dirs)
        print(f"  using {p}")
        add_claim(fails, "C1 identity max error", 1.73e-6,
                  c1["identity_error_bias_corrected"]["PR_max_err"], tol_abs=1e-8)
        checked += 1
        add_claim(fails, "C1 identity rows", 183, c1["_n_valid_rows"], tol_abs=0.0)
        checked += 1

        multitask, p = load_required("multitask_logistic", data_dirs)
        print(f"  using {p}")
        for key, label, expected, lo, hi, n_grok, n_points in [
            ("mlp_4L_h512_mod_add", "4L MLP lambda_c", 0.0511, 0.0495, 0.0591, 13, 70),
            ("lstm_4L_h512_mod_add", "4L LSTM lambda_c", 0.0365, 0.0299, 0.0473, 22, 70),
            ("mamba_4L_d128_mod_add", "4L Mamba lambda_c", 0.0144, 0.0106, 0.0160, 46, 70),
        ]:
            row = multitask[key]
            add_claim(fails, label, expected, row["wd_c"], tol_abs=0.0005)
            add_claim(fails, f"{label} CI lower", lo, row["ci_95"][0], tol_abs=0.0005)
            add_claim(fails, f"{label} CI upper", hi, row["ci_95"][1], tol_abs=0.0005)
            add_claim(fails, f"{label} n_grok", n_grok, row["n_grok"], tol_abs=0.0)
            add_claim(fails, f"{label} n_points", n_points, row["n_points"], tol_abs=0.0)
            checked += 5

        intervention, p = load_required("intervention_stats", data_dirs)
        print(f"  using {p}")
        wd05 = intervention["stratified_by_wd"]["wd0.05"]["B_minus_A__peak_ent"]
        for label, expected, actual, tol in [
            ("intervention peak sigma_H delta", -0.055, wd05["mean_diff"], 0.001),
            ("intervention paired t p", 0.0045, wd05["p_value_t"], 0.0002),
            ("intervention Cohen's d", -1.190, wd05["cohen_d"], 0.001),
            ("intervention paired n", 10, wd05["n"], 0.0),
        ]:
            add_claim(fails, label, expected, actual, tol_abs=tol)
            checked += 1

        holdout, p = load_required("holdout_retention", data_dirs)
        print(f"  using {p}")
        add_claim(fails, "holdout RF AUC", 0.799, holdout["rf"]["holdout_auc"], tol_abs=0.001)
        checked += 1
    except (FileNotFoundError, KeyError, json.JSONDecodeError, TypeError) as exc:
        print(f"ERROR: aggregate verification failed before completion: {exc}")
        sys.exit(2)

    print()
    if fails:
        print(f"FAILED {len(fails)} checks: {fails}")
        sys.exit(1)
    print(f"PASS: all {checked} public numerical checks within tolerance.")


if __name__ == "__main__":
    main()
