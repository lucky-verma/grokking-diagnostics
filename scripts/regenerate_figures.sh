#!/bin/bash
# Regenerate the selected public figures whose scripts are bundled here, then
# verify aggregate-backed numerical claims.
#
# This lightweight public repository ships the rendered figures, aggregate JSONs,
# selected figure scripts, and the numerical verifier. Full raw-run retraining
# and full end-to-end regeneration of every paper figure are intentionally not
# part of this script.

set -euo pipefail

echo "=== Regenerating selected public figures ==="
python eval/scripts/gen_fig8_intervention_forest.py
python eval/scripts/gen_fig9_multitask_heatmap.py
python eval/scripts/gen_fig10_cross_arch.py

echo "=== Verifying numerical claims ==="
python scripts/verify_numerical_claims.py

echo ""
echo "Done. Regenerated Figures 8-10 and verified aggregate-backed claims."
