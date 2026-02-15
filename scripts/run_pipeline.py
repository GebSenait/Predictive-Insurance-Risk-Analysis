#!/usr/bin/env python
"""End-to-end Predictive Insurance Risk Analysis pipeline.

Orchestrates:
    1. Data loading & preprocessing
    2. Model training (regression + classification)
    3. Automated best-model selection
    4. Decision justification JSON generation

Usage (production — requires DVC dataset):
    python scripts/run_pipeline.py

The pipeline writes ``results/decision_summary.json`` upon completion.
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path so ``src`` is importable.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loaders import load_insurance_data
from src.data.preprocessing import run_preprocessing_pipeline
from src.decision.justification import (
    build_decision_summary,
    save_decision_summary,
)
from src.models.selector import get_model_ranking, select_best_model
from src.models.trainer import train_regression_models, train_classification_models


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_FILE = "data/raw/MachineLearningRating_v3.txt"
RESULTS_DIR = "results"
REGRESSION_TARGET = "TotalPremium"
REGRESSION_METRIC = "r2"
CLASSIFICATION_METRIC = "f1"


def main() -> None:
    """Run the full pipeline."""
    print("=" * 72)
    print("  Predictive Insurance Risk Analysis — Pipeline")
    print("=" * 72)

    # ------------------------------------------------------------------
    # 1. Load production data (DVC-tracked)
    # ------------------------------------------------------------------
    data_path = PROJECT_ROOT / DATA_FILE
    df = load_insurance_data(file_path=data_path)
    print(f"[DATA] Loaded {len(df)} rows, {len(df.columns)} columns")

    # ------------------------------------------------------------------
    # 2. Regression task — predict TotalPremium
    # ------------------------------------------------------------------
    print("\n--- Regression: predict TotalPremium ---")
    X_train, X_test, y_train, y_test = run_preprocessing_pipeline(
        df, target_col=REGRESSION_TARGET
    )
    reg_results = train_regression_models(X_train, y_train, X_test, y_test)
    best_reg = select_best_model(reg_results, metric=REGRESSION_METRIC)
    reg_ranking = get_model_ranking(reg_results, metric=REGRESSION_METRIC)
    print(
        f"[MODEL] Best regression model: {best_reg['model_name']} "
        f"(R²={best_reg['test_metrics']['r2']:.4f})"
    )

    # ------------------------------------------------------------------
    # 3. Classification task — predict HasClaim (binary)
    # ------------------------------------------------------------------
    print("\n--- Classification: predict HasClaim ---")
    X_tr_c, X_te_c, y_tr_c, y_te_c = run_preprocessing_pipeline(
        df, target_col="TotalClaims", filter_positive=False
    )
    # Binarise target for classification
    y_tr_c = (y_tr_c > 0).astype(int)
    y_te_c = (y_te_c > 0).astype(int)

    clf_results = train_classification_models(X_tr_c, y_tr_c, X_te_c, y_te_c)
    best_clf = select_best_model(clf_results, metric=CLASSIFICATION_METRIC)
    clf_ranking = get_model_ranking(clf_results, metric=CLASSIFICATION_METRIC)
    print(
        f"[MODEL] Best classification model: {best_clf['model_name']} "
        f"(F1={best_clf['test_metrics']['f1']:.4f})"
    )

    # ------------------------------------------------------------------
    # 4. Decision justification
    # ------------------------------------------------------------------
    # Use the best-performing regression model for the primary decision summary
    primary_metric = REGRESSION_METRIC
    primary_score = best_reg["test_metrics"][primary_metric]
    summary = build_decision_summary(
        selected_model_name=best_reg["model_name"],
        task_type="regression",
        metric_name=primary_metric,
        metric_score=primary_score,
        all_model_rankings=reg_ranking,
    )
    out_file = save_decision_summary(summary, output_dir=RESULTS_DIR)
    print(f"\n[DECISION] Summary written to {out_file}")
    print("=" * 72)
    print("  Pipeline complete.")
    print("=" * 72)


if __name__ == "__main__":
    main()
