"""Generate a structured decision summary in JSON format.

This module bridges model outputs and business stakeholders by producing a
transparent, human-readable JSON artifact that explains *which* model was
selected, *why*, and *what it means* for pricing decisions.
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_OUTPUT_DIR = "results"
DECISION_FILENAME = "decision_summary.json"

# Business-impact templates keyed by task type
BUSINESS_IMPACT_TEMPLATES: Dict[str, str] = {
    "regression": (
        "The selected regression model ({model_name}) achieves an R-squared of "
        "{score:.4f} on the hold-out test set, explaining {pct:.1f}% of the "
        "variance in the target variable.  This level of accuracy supports "
        "data-driven premium pricing and reserve estimation."
    ),
    "classification": (
        "The selected classification model ({model_name}) achieves an F1-score "
        "of {score:.4f} on the hold-out test set, balancing precision and recall "
        "for claim-occurrence prediction.  This supports risk segmentation and "
        "underwriting decisions."
    ),
}


def get_git_commit_hash() -> str:
    """Return the current HEAD commit hash for traceability."""
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def build_decision_summary(
    selected_model_name: str,
    task_type: str,
    metric_name: str,
    metric_score: float,
    all_model_rankings: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Build a structured decision-summary dict.

    Args:
        selected_model_name: Name of the winning model.
        task_type: ``"regression"`` or ``"classification"``.
        metric_name: Name of the selection metric (e.g. ``"r2"``, ``"f1"``).
        metric_score: Numeric score of the winning model.
        all_model_rankings: Optional ranked list of all models.

    Returns:
        Decision-summary dict ready for JSON serialisation.
    """
    template = BUSINESS_IMPACT_TEMPLATES.get(task_type, "")
    pct = metric_score * 100 if task_type == "regression" else 0.0
    business_impact = template.format(
        model_name=selected_model_name,
        score=metric_score,
        pct=pct,
    )

    summary: Dict[str, Any] = {
        "selected_model": selected_model_name,
        "task_type": task_type,
        "metric_name": metric_name,
        "metric_score": round(metric_score, 6),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit_hash(),
        "business_impact": business_impact,
    }
    if all_model_rankings:
        summary["model_rankings"] = all_model_rankings
    return summary


def save_decision_summary(
    summary: Dict[str, Any],
    output_dir: str = DEFAULT_OUTPUT_DIR,
    filename: str = DECISION_FILENAME,
) -> Path:
    """Persist the decision summary as JSON.

    Args:
        summary: Decision-summary dict.
        output_dir: Directory to write the file into.
        filename: File name for the JSON artifact.

    Returns:
        Path to the written file.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    file_path = out_path / filename

    with open(file_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=str)

    return file_path
