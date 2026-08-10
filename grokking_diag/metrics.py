"""Cheap online order parameters for attention-head coordination.

All metrics computable in O(H^2 * T^2) per evaluation step from raw attention
weights. No second-order information (no Hessian, no rLLC), suitable for live
training-loop monitoring.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def _to_numpy(x):
    """Accept torch tensor, numpy array, or list. Return numpy."""
    if hasattr(x, "detach"):
        x = x.detach().cpu().numpy()
    return np.asarray(x)


def compute_attention_entropy_per_head(
    attn_weights_list: Sequence,
    n_heads: int,
) -> dict:
    """Compute per-head attention entropy + entropy std/range across heads.

    Args:
        attn_weights_list: list of attention tensors per layer, shape (B, H, T, T)
        n_heads: number of attention heads

    Returns:
        dict with entropy_mean, entropy_std, entropy_range
    """
    per_layer = []
    for attn in attn_weights_list:
        a = _to_numpy(attn)
        if a.ndim != 4:
            raise ValueError(f"expected (B, H, T, T) attention; got shape {a.shape}")
        # entropy per head per row, then average over batch + rows
        # Add small eps to prevent log(0)
        eps = 1e-12
        ent = -np.sum(a * np.log(a + eps), axis=-1)  # (B, H, T)
        per_head = ent.mean(axis=(0, 2))  # (H,)
        per_layer.append(per_head)
    stacked = np.stack(per_layer)  # (L, H)
    entropy_mean = stacked.mean()
    entropy_std = stacked.std(axis=1).mean()  # std across heads, mean over layers
    entropy_range = (stacked.max(axis=1) - stacked.min(axis=1)).mean()
    return {
        "entropy_mean": float(entropy_mean),
        "entropy_std": float(entropy_std),
        "entropy_range": float(entropy_range),
    }


def compute_head_functional_similarity_matrix(
    attn_weights_list: Sequence,
    n_heads: int,
) -> tuple:
    """Compute mean pairwise cosine similarity of head attention patterns +
    spectral gap of similarity matrix.

    Returns:
        (mean_similarity, spectral_gap)
    """
    sims = []
    gaps = []
    for attn in attn_weights_list:
        a = _to_numpy(attn)
        if a.ndim != 4:
            raise ValueError(f"expected (B, H, T, T) attention; got shape {a.shape}")
        # Flatten each head pattern: (H, B*T*T)
        flat = a.transpose(1, 0, 2, 3).reshape(a.shape[1], -1)
        norms = np.linalg.norm(flat, axis=-1, keepdims=True) + 1e-12
        normed = flat / norms
        sim_mat = normed @ normed.T  # (H, H)
        # Mean of off-diagonal
        mask = ~np.eye(sim_mat.shape[0], dtype=bool)
        sims.append(sim_mat[mask].mean())
        # Spectral gap: lambda_1 - lambda_2
        eigs = np.linalg.eigvalsh(sim_mat)
        gaps.append(float(eigs[-1] - eigs[-2]))
    return float(np.mean(sims)), float(np.mean(gaps))


def compute_synchronization_order_parameter(specs):
    """Kuramoto-style coherence from per-head principal direction phases.

    Currently returns a stub if specs is None or empty. Compatible with the
    paper's reference implementation: returns (r_dist, r_spread).
    """
    if specs is None or len(specs) == 0:
        return 0.0, 0.0
    s = _to_numpy(specs)
    if s.ndim == 1:
        return 0.0, 0.0
    r_dist = float(np.abs(np.exp(1j * s).mean()))
    r_spread = float(s.std())
    return r_dist, r_spread


def compute_metrics(attention_weights_list, n_heads=None) -> dict:
    """One-shot: compute all order parameters from attention weights.

    Args:
        attention_weights_list: per-layer attention tensors (B, H, T, T)
        n_heads: optional; inferred from shape if None

    Returns:
        dict with all metrics flattened.
    """
    if n_heads is None:
        n_heads = _to_numpy(attention_weights_list[0]).shape[1]
    ent = compute_attention_entropy_per_head(attention_weights_list, n_heads)
    sim, gap = compute_head_functional_similarity_matrix(attention_weights_list, n_heads)
    return {
        "entropy_mean": ent["entropy_mean"],
        "entropy_std": ent["entropy_std"],
        "entropy_range": ent["entropy_range"],
        "mean_similarity": sim,
        "spectral_gap": gap,
    }
