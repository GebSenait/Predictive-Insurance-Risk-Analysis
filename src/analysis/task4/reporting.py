"""Reporting module for Task 4 predictive modeling results."""

import json
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generate reports for Task 4 model results."""

    def __init__(self, output_path: Optional[Path] = None):
        """
        Initialize ReportGenerator.

        Args:
            output_path: Path to save reports
        """
        self.output_path = output_path or Path("results/task4")
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.logger = logger

    def create_model_comparison_table(
        self, model_results: Dict[str, Dict], task_type: str = "regression"
    ) -> pd.DataFrame:
        """
        Create a comparison table of all models.

        Args:
            model_results: Dictionary of model results
            task_type: 'regression' or 'classification'

        Returns:
            DataFrame with model comparison
        """
        rows = []
        for model_name, results in model_results.items():
            row = {"Model": results.get("model_name", model_name)}

            if task_type == "regression":
                row["Train RMSE"] = results.get("train_rmse", None)
                row["Test RMSE"] = results.get("test_rmse", None)
                row["Train R²"] = results.get("train_r2", None)
                row["Test R²"] = results.get("test_r2", None)
            else:  # classification
                row["Train Accuracy"] = results.get("train_accuracy", None)
                row["Test Accuracy"] = results.get("test_accuracy", None)
                row["Test Precision"] = results.get("test_precision", None)
                row["Test Recall"] = results.get("test_recall", None)
                row["Test F1"] = results.get("test_f1", None)

            rows.append(row)

        df = pd.DataFrame(rows)
        return df

    def generate_markdown_report(
        self,
        all_results: Dict,
        filename: str = "task4_modeling_report.md",
    ) -> None:
        """
        Generate comprehensive markdown report.

        Args:
            all_results: Dictionary with all model results
            filename: Output filename
        """
        self.logger.info(f"Generating markdown report: {filename}")

        report_path = self.output_path / filename

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Task 4: Predictive Modeling for Risk-Based Pricing\n\n")
            f.write("## Executive Summary\n\n")
            f.write(
                "This report presents the results of predictive modeling for ACIS's "
                "risk-based pricing system, including claim severity prediction, premium "
                "optimization, and claim probability estimation.\n\n"
            )

            # Model Comparison Sections
            for task_name, task_results in all_results.items():
                if task_name == "interpretability":
                    continue

                f.write(f"## {task_name.replace('_', ' ').title()} Models\n\n")

                # Model comparison table
                if "model_results" in task_results:
                    comparison_df = self.create_model_comparison_table(
                        task_results["model_results"],
                        task_type=(
                            "regression"
                            if "severity" in task_name or "premium" in task_name
                            else "classification"
                        ),
                    )
                    f.write("### Model Comparison\n\n")
                    f.write(comparison_df.to_markdown(index=False))
                    f.write("\n\n")

                    # Best model
                    if "best_model" in task_results:
                        best_model_name = task_results["best_model"]["model_name"]
                        f.write(f"### Best Model: {best_model_name}\n\n")

                        if "test_r2" in task_results["best_model"]:
                            f.write(
                                f"- **Test R²**: {task_results['best_model']['test_r2']:.4f}\n"
                            )
                            f.write(
                                f"- **Test RMSE**: {task_results['best_model']['test_rmse']:.2f}\n"
                            )
                        elif "test_f1" in task_results["best_model"]:
                            f.write(
                                f"- **Test F1**: {task_results['best_model']['test_f1']:.4f}\n"
                            )
                            f.write(
                                f"- **Test Accuracy**: {task_results['best_model']['test_accuracy']:.4f}\n"
                            )
                        f.write("\n")

            # Interpretability Section
            if "interpretability" in all_results:
                f.write("## Model Interpretability\n\n")
                f.write("### Top Influential Features\n\n")

                for model_name, interp_results in all_results[
                    "interpretability"
                ].items():
                    f.write(f"#### {model_name}\n\n")

                    if (
                        "top_features" in interp_results
                        and interp_results["top_features"]
                    ):
                        f.write("| Rank | Feature | Combined Importance |\n")
                        f.write("|------|---------|---------------------|\n")

                        for idx, feat in enumerate(
                            interp_results["top_features"][:10], 1
                        ):
                            f.write(
                                f"| {idx} | {feat['feature']} | "
                                f"{feat['combined_importance']:.4f} |\n"
                            )
                        f.write("\n")

            # Business Implications
            f.write("## Business Implications\n\n")
            f.write("### Key Insights\n\n")

            # Add insights based on results
            if "severity" in all_results:
                f.write(
                    "1. **Claim Severity Prediction**: The severity model enables ACIS to "
                    "estimate expected claim amounts for policies with claims, supporting "
                    "reserve setting and pricing strategies.\n\n"
                )

            if "premium" in all_results:
                f.write(
                    "2. **Premium Optimization**: The premium model helps identify appropriate "
                    "premium levels based on policy characteristics, supporting dynamic pricing.\n\n"
                )

            if "claim_probability" in all_results:
                f.write(
                    "3. **Claim Probability**: The claim probability model supports risk-based "
                    "pricing through the formula: Premium = P(Claim) × Predicted Severity + "
                    "Expense Loading + Profit Margin.\n\n"
                )

            f.write("### Recommendations\n\n")
            f.write(
                "1. Implement the best-performing models in production for risk-based pricing.\n"
            )
            f.write(
                "2. Monitor model performance regularly and retrain as new data becomes available.\n"
            )
            f.write(
                "3. Use interpretability insights to understand key risk drivers and adjust "
                "pricing strategies accordingly.\n"
            )
            f.write(
                "4. Ensure regulatory compliance when using demographic or geographic features "
                "in pricing models.\n"
            )

        self.logger.info(f"Report saved to: {report_path}")

    def save_results_table(
        self,
        all_results: Dict,
        filename: str = "task4_model_comparison.csv",
    ) -> None:
        """
        Save model comparison table to CSV.

        Args:
            all_results: Dictionary with all model results
            filename: Output filename
        """
        self.logger.info(f"Saving results table: {filename}")

        all_tables = []

        for task_name, task_results in all_results.items():
            if task_name == "interpretability" or "model_results" not in task_results:
                continue

            comparison_df = self.create_model_comparison_table(
                task_results["model_results"],
                task_type=(
                    "regression"
                    if "severity" in task_name or "premium" in task_name
                    else "classification"
                ),
            )
            comparison_df["Task"] = task_name.replace("_", " ").title()
            all_tables.append(comparison_df)

        if all_tables:
            combined_df = pd.concat(all_tables, ignore_index=True)
            table_path = self.output_path / filename
            combined_df.to_csv(table_path, index=False)
            self.logger.info(f"Results table saved to: {table_path}")

    def save_interpretability_summary(
        self,
        interpretability_results: Dict,
        filename: str = "task4_top_features.json",
    ) -> None:
        """
        Save interpretability summary to JSON.

        Args:
            interpretability_results: Dictionary with interpretability results
            filename: Output filename
        """
        self.logger.info(f"Saving interpretability summary: {filename}")

        summary = {}
        for model_name, results in interpretability_results.items():
            if "top_features" in results:
                summary[model_name] = {
                    "top_10_features": [
                        {
                            "feature": feat["feature"],
                            "combined_importance": float(feat["combined_importance"]),
                        }
                        for feat in results["top_features"][:10]
                    ]
                }

        summary_path = self.output_path / filename
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        self.logger.info(f"Interpretability summary saved to: {summary_path}")

    def generate_business_interpretation(
        self,
        top_features: List[Dict],
        model_type: str = "severity",
    ) -> str:
        """
        Generate business interpretation for top features.

        Args:
            top_features: List of top features with importance
            model_type: Type of model ('severity', 'premium', 'claim_probability')

        Returns:
            Business interpretation text
        """
        interpretation = f"\n### Business Interpretation for {model_type.replace('_', ' ').title()} Model\n\n"

        for idx, feat in enumerate(top_features[:5], 1):
            feat_name = feat["feature"]
            importance = feat["combined_importance"]

            interpretation += f"{idx}. **{feat_name}** (Importance: {importance:.4f})\n"

            # Add business context based on feature name
            if "age" in feat_name.lower():
                interpretation += "   - Age is a significant risk factor. Consider age-based pricing tiers.\n"
            elif "province" in feat_name.lower() or "postal" in feat_name.lower():
                interpretation += "   - Geographic location impacts risk. Consider regional pricing adjustments.\n"
            elif "gender" in feat_name.lower():
                interpretation += "   - Note: Gender-based pricing may be restricted by regulations.\n"
            elif "premium" in feat_name.lower():
                interpretation += "   - Premium level correlates with risk. Higher premiums may indicate higher risk segments.\n"
            else:
                interpretation += f"   - This feature significantly influences {model_type} predictions.\n"
            interpretation += "\n"

        return interpretation
