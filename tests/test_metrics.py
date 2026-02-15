"""Tests for evaluation metrics module.

Pure computation tests — no data files required.
"""

import numpy as np

from src.evaluation.metrics import (
    classification_metrics,
    compute_loss_ratio,
    regression_metrics,
)


class TestRegressionMetrics:
    """Verify regression metric correctness."""

    def test_perfect_predictions(self) -> None:
        """Perfect predictions yield RMSE=0 and R²=1."""
        y = np.array([1.0, 2.0, 3.0])
        metrics = regression_metrics(y, y)
        assert metrics["rmse"] == 0.0
        assert metrics["r2"] == 1.0

    def test_rmse_positive(self) -> None:
        """RMSE is always non-negative."""
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        metrics = regression_metrics(y_true, y_pred)
        assert metrics["rmse"] > 0


class TestClassificationMetrics:
    """Verify classification metric correctness."""

    def test_perfect_classification(self) -> None:
        """Perfect predictions give all metrics = 1.0."""
        y = np.array([0, 1, 1, 0])
        metrics = classification_metrics(y, y)
        assert metrics["accuracy"] == 1.0
        assert metrics["f1"] == 1.0

    def test_zero_division_handled(self) -> None:
        """Metrics handle all-negative predictions without error."""
        y_true = np.array([0, 0, 0, 0])
        y_pred = np.array([0, 0, 0, 0])
        metrics = classification_metrics(y_true, y_pred)
        assert metrics["accuracy"] == 1.0
        # precision/recall/f1 are 0 when no positive class predicted or present
        assert metrics["precision"] == 0.0


class TestLossRatio:
    """Verify loss ratio computation."""

    def test_basic_ratio(self) -> None:
        """Loss ratio equals claims / premiums."""
        claims = np.array([100.0, 0.0])
        premiums = np.array([200.0, 300.0])
        ratio = compute_loss_ratio(claims, premiums)
        np.testing.assert_array_almost_equal(ratio, [0.5, 0.0])

    def test_zero_premium_safe(self) -> None:
        """Zero premium returns 0 instead of inf."""
        claims = np.array([100.0])
        premiums = np.array([0.0])
        ratio = compute_loss_ratio(claims, premiums)
        assert ratio[0] == 0.0
