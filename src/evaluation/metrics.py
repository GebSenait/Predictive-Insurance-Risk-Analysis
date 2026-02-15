"""Evaluation metrics for regression and classification tasks.

Provides standalone metric functions so they can be tested independently
of the training pipeline and reused in reporting.
"""

from typing import Dict

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)


def regression_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """Compute standard regression metrics.

    Args:
        y_true: Actual target values.
        y_pred: Predicted target values.

    Returns:
        Dict with ``rmse`` and ``r2``.
    """
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = float(r2_score(y_true, y_pred))
    return {"rmse": rmse, "r2": r2}


def classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """Compute standard binary classification metrics.

    Args:
        y_true: Actual labels.
        y_pred: Predicted labels.

    Returns:
        Dict with ``accuracy``, ``precision``, ``recall``, ``f1``.
    """
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average="binary", zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average="binary", zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average="binary", zero_division=0)),
    }


def compute_loss_ratio(
    total_claims: np.ndarray,
    total_premiums: np.ndarray,
) -> np.ndarray:
    """Compute loss ratio (claims / premiums) element-wise.

    Args:
        total_claims: Claim amounts.
        total_premiums: Premium amounts.

    Returns:
        Array of loss-ratio values (inf-safe).
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(total_premiums > 0, total_claims / total_premiums, 0.0)
    return ratio
