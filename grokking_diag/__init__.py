"""grokking-diag: cheap online diagnostics for transformer training dynamics.

Two scalar attention-head order parameters (mean pairwise cosine similarity and
entropy standard deviation across heads) plus a permutation-symmetry diagnostic
(participation-ratio of head-output vectors). All computable in O(H^2 * T^2) per
evaluation step from the attention weights already produced by the forward pass.

Quickstart:
    >>> from grokking_diag import compute_metrics
    >>> metrics = compute_metrics(attention_weights)
    >>> # {"mean_similarity": 0.93, "entropy_std": 0.18, "PR_norm": 0.71, ...}

Phase identification on canonical 4L8H modular-arithmetic transformers:
    Phase 1 (sync, near grokking):     mean_similarity >= 0.93, entropy_std rising
    Phase 2 (differentiation):         mean_similarity dips to ~0.88, entropy_std peaks
    Phase 5 (observed late collapse):  PR_norm < 0.2 on canonical seed-42

Companion paper: Verma 2026, "Weight Decay Regimes in Grokking Transformers:
Cheap Online Diagnostics".

The published verdict on long-horizon retention prediction is correlational
only: random-forest holdout AUC 0.799 falls below the pre-specified 0.85
predictor gate (see paper Section "Order parameters as correlational
discriminators"). The included RetentionPredictor is therefore released as a
research-grade order-parameter aggregator, not as a deployment-ready predictor.
"""
__version__ = "0.1.0"

from .metrics import (
    compute_attention_entropy_per_head,
    compute_head_functional_similarity_matrix,
    compute_synchronization_order_parameter,
    compute_metrics,
)

__all__ = [
    "compute_attention_entropy_per_head",
    "compute_head_functional_similarity_matrix",
    "compute_synchronization_order_parameter",
    "compute_metrics",
]
