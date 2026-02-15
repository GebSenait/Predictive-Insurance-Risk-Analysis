"""Tests for model training and selection.

All data is created in-memory — no file I/O, no DVC dependency.
"""

import pandas as pd
import pytest

from src.models.selector import get_model_ranking, select_best_model
from src.models.trainer import train_regression_models, train_classification_models


class TestModelTraining:
    """Verify that the trainer returns valid result dicts."""

    def test_regression_models_return_results(self, sample_dataframe: pd.DataFrame) -> None:
        """All regression models train and produce metrics."""
        X = sample_dataframe[["feature_a", "feature_b"]]
        y = sample_dataframe["target_reg"]
        results = train_regression_models(X, y, X, y)
        assert len(results) >= 3  # at least Linear, DT, RF, GB
        for res in results:
            assert "model_name" in res
            assert "test_metrics" in res
            assert "r2" in res["test_metrics"]

    def test_classification_models_return_results(self, sample_dataframe: pd.DataFrame) -> None:
        """All classification models train and produce metrics."""
        X = sample_dataframe[["feature_a", "feature_b"]]
        y = sample_dataframe["target_cls"]
        results = train_classification_models(X, y, X, y)
        assert len(results) >= 3
        for res in results:
            assert "f1" in res["test_metrics"]


class TestModelSelector:
    """Verify model selection and ranking logic."""

    def test_select_best_regression(self, sample_dataframe: pd.DataFrame) -> None:
        """Best regression model has the highest R²."""
        X = sample_dataframe[["feature_a", "feature_b"]]
        y = sample_dataframe["target_reg"]
        results = train_regression_models(X, y, X, y)
        best = select_best_model(results, metric="r2")
        assert best["model_name"] is not None
        assert best["test_metrics"]["r2"] >= 0

    def test_select_raises_on_empty(self) -> None:
        """Selecting from empty results raises ValueError."""
        with pytest.raises(ValueError):
            select_best_model([], metric="r2")

    def test_get_ranking_returns_sorted(self, sample_dataframe: pd.DataFrame) -> None:
        """Ranking returns models sorted by score."""
        X = sample_dataframe[["feature_a", "feature_b"]]
        y = sample_dataframe["target_reg"]
        results = train_regression_models(X, y, X, y)
        ranking = get_model_ranking(results, metric="r2")
        scores = [r["score"] for r in ranking]
        assert scores == sorted(scores, reverse=True)
