"""Automated model selection for insurance risk models.

Picks the best model from a list of training results based on a configurable
metric, following the principle: *higher is better* for R-squared / F1 /
accuracy, *lower is better* for RMSE.
"""

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HIGHER_IS_BETTER_METRICS = {"r2", "accuracy", "f1", "precision", "recall"}
LOWER_IS_BETTER_METRICS = {"rmse"}


def select_best_model(
    results: List[Dict[str, Any]],
    metric: str = "r2",
    split: str = "test_metrics",
) -> Dict[str, Any]:
    """Select the best model from training results.

    Args:
        results: List of result dicts produced by ``trainer.train_*_models``.
        metric: Key inside the metrics sub-dict to rank on (e.g. ``"r2"``,
                ``"f1"``, ``"rmse"``).
        split: Which metrics dict to use (``"train_metrics"`` or
               ``"test_metrics"``).

    Returns:
        The result dict of the winning model.

    Raises:
        ValueError: If *results* is empty or *metric* not found.
    """
    if not results:
        raise ValueError("Cannot select from an empty results list.")

    scored: List[tuple] = []
    for res in results:
        metrics_dict = res.get(split, {})
        if metric not in metrics_dict:
            continue
        scored.append((metrics_dict[metric], res))

    if not scored:
        raise ValueError(
            f"Metric '{metric}' not found in any result under '{split}'."
        )

    higher_is_better = metric in HIGHER_IS_BETTER_METRICS
    scored.sort(key=lambda x: x[0], reverse=higher_is_better)
    return scored[0][1]


def get_model_ranking(
    results: List[Dict[str, Any]],
    metric: str = "r2",
    split: str = "test_metrics",
) -> List[Dict[str, Any]]:
    """Rank all models by a given metric.

    Args:
        results: List of result dicts.
        metric: Metric key for ranking.
        split: Which metrics dict to use.

    Returns:
        Sorted list of ``{"rank", "model_name", "score"}`` dicts.
    """
    higher_is_better = metric in HIGHER_IS_BETTER_METRICS
    scored = []
    for res in results:
        score = res.get(split, {}).get(metric)
        if score is not None:
            scored.append({"model_name": res["model_name"], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=higher_is_better)
    for idx, entry in enumerate(scored, start=1):
        entry["rank"] = idx
    return scored
