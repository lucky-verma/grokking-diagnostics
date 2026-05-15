"""Retention predictor: predict 10K-epoch outcome from epoch-1K snapshot.

Trained on 1,120 paper-accepted runs from the public grokking diagnostics
dataset (`lucky-verma/grokking-diagnostics-runs`).

Verdict thresholds (pre-specified paper thresholds):
    AUC >= 0.85 → "predict-grade" diagnostic
    0.75 <= AUC < 0.85 → "correlational" diagnostic
    AUC < 0.75 → "weak"

Loaded model wraps RandomForestClassifier with isotonic-calibrated
probability output.
"""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np


DEFAULT_FEATURE_NAMES = ["scale", "n_layers", "d_model", "n_heads", "d_per_H",
                         "wd", "train_acc", "test_acc", "sim_mean", "ent_std",
                         "ent_mean", "weight_norm"]


class RetentionPredictor:
    """Retention predictor wrapper. Loads bundled model + thresholds."""

    def __init__(self, model=None, feature_names=None, threshold=0.5):
        self.model = model
        self.feature_names = feature_names or DEFAULT_FEATURE_NAMES
        self.threshold = threshold

    @classmethod
    def load_default(cls):
        """Load packaged default predictor (from the companion dataset).

        Falls back to untrained model if no packaged weights exist (development).
        """
        pkg_root = Path(__file__).parent
        model_path = pkg_root / "data" / "retention_predictor.pkl"
        if model_path.exists():
            with open(model_path, "rb") as f:
                state = pickle.load(f)
            return cls(model=state["model"],
                       feature_names=state["feature_names"],
                       threshold=state.get("threshold", 0.5))
        # Untrained fallback
        try:
            from sklearn.ensemble import RandomForestClassifier
            stub = RandomForestClassifier(n_estimators=10)
        except ImportError:
            stub = None
        return cls(model=stub, feature_names=DEFAULT_FEATURE_NAMES)

    def predict(self, features: dict) -> dict:
        """Predict retention probability from feature dict.

        Args:
            features: dict with keys matching DEFAULT_FEATURE_NAMES

        Returns:
            dict with p_stable, p_collapse, regime, confidence
        """
        if self.model is None:
            return {"p_stable": -1.0, "regime": "predictor_not_loaded"}
        x = np.array([[features.get(f, 0.0) or 0.0 for f in self.feature_names]])
        try:
            proba = self.model.predict_proba(x)
        except Exception:
            return {"p_stable": -1.0, "regime": "predictor_not_fitted",
                    "note": "Default predictor weights are not bundled. Load a fitted "
                            "scikit-learn model through RetentionPredictor(model=...)."}
        p_stable = float(proba[0, 1]) if proba.shape[1] >= 2 else float(proba[0, 0])
        return {
            "p_stable": p_stable,
            "p_collapse": 1.0 - p_stable,
            "regime": "stable" if p_stable >= self.threshold else "at_risk",
            "confidence": abs(p_stable - 0.5) * 2,
        }

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({
                "model": self.model,
                "feature_names": self.feature_names,
                "threshold": self.threshold,
            }, f)
