"""Model training for insurance risk prediction.

Trains multiple scikit-learn models on regression or classification tasks
and returns structured results that downstream modules can consume.
"""

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_RANDOM_STATE: int = 42
DEFAULT_N_ESTIMATORS: int = 100
DEFAULT_MAX_DEPTH: int = 10
DEFAULT_LEARNING_RATE: float = 0.1
MAX_ITER_LOGISTIC: int = 1000


def _regression_metrics(
    y_true: pd.Series,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """Compute RMSE and R-squared.

    Args:
        y_true: Actual values.
        y_pred: Predicted values.

    Returns:
        Dict with ``rmse`` and ``r2`` keys.
    """
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def _classification_metrics(
    y_true: pd.Series,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """Compute accuracy, precision, recall, and F1.

    Args:
        y_true: Actual labels.
        y_pred: Predicted labels.

    Returns:
        Dict with classification metric keys.
    """
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average="binary", zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average="binary", zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average="binary", zero_division=0)),
    }


def _train_and_evaluate(
    model: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    task_type: str,
) -> Dict[str, Any]:
    """Fit a model and return structured results.

    Args:
        model: Scikit-learn estimator.
        X_train: Training features.
        y_train: Training target.
        X_test: Test features.
        y_test: Test target.
        task_type: ``"regression"`` or ``"classification"``.

    Returns:
        Dict containing the fitted model, name, and train/test metrics.
    """
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    metric_fn = _regression_metrics if task_type == "regression" else _classification_metrics
    train_metrics = metric_fn(y_train, y_train_pred)
    test_metrics = metric_fn(y_test, y_test_pred)

    return {
        "model": model,
        "model_name": type(model).__name__,
        "task_type": task_type,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
    }


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def train_regression_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    random_state: int = DEFAULT_RANDOM_STATE,
    n_estimators: int = DEFAULT_N_ESTIMATORS,
    max_depth: int = DEFAULT_MAX_DEPTH,
    learning_rate: float = DEFAULT_LEARNING_RATE,
) -> List[Dict[str, Any]]:
    """Train a suite of regression models.

    Args:
        X_train: Training features.
        y_train: Training target.
        X_test: Test features.
        y_test: Test target.
        random_state: Seed for reproducibility.
        n_estimators: Trees for ensemble methods.
        max_depth: Max tree depth.
        learning_rate: Step size for boosting.

    Returns:
        List of result dicts (one per model).
    """
    models = [
        LinearRegression(),
        DecisionTreeRegressor(max_depth=max_depth, random_state=random_state),
        RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
        ),
        GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
        ),
    ]
    return [
        _train_and_evaluate(m, X_train, y_train, X_test, y_test, "regression")
        for m in models
    ]


def train_classification_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    random_state: int = DEFAULT_RANDOM_STATE,
    n_estimators: int = DEFAULT_N_ESTIMATORS,
    max_depth: int = DEFAULT_MAX_DEPTH,
    learning_rate: float = DEFAULT_LEARNING_RATE,
) -> List[Dict[str, Any]]:
    """Train a suite of classification models.

    Args:
        X_train: Training features.
        y_train: Training target.
        X_test: Test features.
        y_test: Test target.
        random_state: Seed for reproducibility.
        n_estimators: Trees for ensemble methods.
        max_depth: Max tree depth.
        learning_rate: Step size for boosting.

    Returns:
        List of result dicts (one per model).
    """
    models = [
        LogisticRegression(
            random_state=random_state, max_iter=MAX_ITER_LOGISTIC, n_jobs=-1
        ),
        DecisionTreeClassifier(max_depth=max_depth, random_state=random_state),
        RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
        ),
        GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
        ),
    ]
    return [
        _train_and_evaluate(m, X_train, y_train, X_test, y_test, "classification")
        for m in models
    ]
