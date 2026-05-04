"""Evaluation helpers for ML, RAG, and generated content quality."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support


def accuracy_score_safe(y_true: Iterable[str], y_pred: Iterable[str]) -> float:
    """Return classification accuracy with safe input handling."""
    truth = list(y_true)
    pred = list(y_pred)
    if not truth or len(truth) != len(pred):
        return 0.0
    return round(float(accuracy_score(truth, pred)), 4)


def classification_metrics(y_true: Iterable[str], y_pred: Iterable[str]) -> dict[str, object]:
    """Return capstone-ready classification metrics."""
    truth = list(y_true)
    pred = list(y_pred)
    if not truth or len(truth) != len(pred):
        return {"accuracy": 0.0, "macro_precision": 0.0, "macro_recall": 0.0, "macro_f1": 0.0}
    precision, recall, f1, _ = precision_recall_fscore_support(
        truth,
        pred,
        average="macro",
        zero_division=0,
    )
    return {
        "accuracy": accuracy_score_safe(truth, pred),
        "macro_precision": round(float(precision), 4),
        "macro_recall": round(float(recall), 4),
        "macro_f1": round(float(f1), 4),
        "report": classification_report(truth, pred, zero_division=0),
    }


def label_distribution(labels: Iterable[str]) -> dict[str, int]:
    """Return a label distribution using pandas for dashboard readiness."""
    series = pd.Series(list(labels), dtype="string").dropna()
    return {str(label): int(count) for label, count in series.value_counts().items()}


def content_quality_score(text: str) -> float:
    """Transparent heuristic quality score for generated content."""
    content = str(text or "").strip()
    if not content:
        return 0.0
    words = content.split()
    score = 0.35
    score += min(len(words) / 300, 0.25)
    structure_markers = sum(marker in content for marker in ["1.", "-", "CTA", "Call to Action", "Next step"])
    score += min(structure_markers * 0.08, 0.2)
    action_terms = ["audience", "benefit", "value", "action", "optimize", "measure"]
    score += min(sum(term in content.lower() for term in action_terms) * 0.04, 0.2)
    return round(float(np.clip(score, 0.0, 1.0)), 2)
