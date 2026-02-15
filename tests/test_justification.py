"""Tests for the decision justification module.

Validates JSON output structure and content — no external data needed.
"""

import json
from pathlib import Path

from src.decision.justification import (
    DECISION_FILENAME,
    build_decision_summary,
    save_decision_summary,
)


class TestBuildDecisionSummary:
    """Verify the summary dict structure."""

    def test_required_keys_present(self) -> None:
        """Summary contains all business-critical keys."""
        summary = build_decision_summary(
            selected_model_name="RandomForestRegressor",
            task_type="regression",
            metric_name="r2",
            metric_score=0.85,
        )
        required_keys = {
            "selected_model",
            "task_type",
            "metric_name",
            "metric_score",
            "timestamp",
            "business_impact",
        }
        assert required_keys.issubset(summary.keys())

    def test_metric_score_rounded(self) -> None:
        """Metric score is rounded to 6 decimal places."""
        summary = build_decision_summary(
            selected_model_name="GBClassifier",
            task_type="classification",
            metric_name="f1",
            metric_score=0.123456789,
        )
        assert summary["metric_score"] == 0.123457

    def test_business_impact_not_empty(self) -> None:
        """Business impact explanation is a non-empty string."""
        summary = build_decision_summary(
            selected_model_name="LinearRegression",
            task_type="regression",
            metric_name="r2",
            metric_score=0.72,
        )
        assert isinstance(summary["business_impact"], str)
        assert len(summary["business_impact"]) > 0


class TestSaveDecisionSummary:
    """Verify file persistence."""

    def test_json_written_to_disk(self, tmp_path: Path) -> None:
        """Summary is saved as valid JSON at the expected path."""
        summary = build_decision_summary(
            selected_model_name="TestModel",
            task_type="regression",
            metric_name="r2",
            metric_score=0.99,
        )
        out = save_decision_summary(summary, output_dir=str(tmp_path))
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["selected_model"] == "TestModel"
