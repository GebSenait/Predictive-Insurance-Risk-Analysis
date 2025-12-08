"""Visualization utilities for Task 3 statistical analysis."""

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


class VisualizationGenerator:
    """Generate visualizations for hypothesis testing results."""

    def __init__(self, output_path: Path):
        """
        Initialize VisualizationGenerator.

        Args:
            output_path: Path to save visualizations
        """
        self.logger = logger
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def plot_metric_comparison(
        self,
        group_a_data: pd.Series,
        group_b_data: pd.Series,
        metric_name: str,
        group_a_name: str,
        group_b_name: str,
        filename: str,
    ):
        """
        Create comparison plot for a metric between two groups.

        Args:
            group_a_data: Data for group A
            group_b_data: Data for group B
            metric_name: Name of the metric
            group_a_name: Name of group A
            group_b_name: Name of group B
            filename: Output filename
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Box plot
        ax1 = axes[0]
        data_to_plot = [group_a_data.dropna(), group_b_data.dropna()]
        bp = ax1.boxplot(data_to_plot, labels=[group_a_name, group_b_name])
        ax1.set_title(f"{metric_name} Comparison (Box Plot)")
        ax1.set_ylabel(metric_name)
        ax1.grid(True, alpha=0.3)

        # Histogram
        ax2 = axes[1]
        ax2.hist(
            group_a_data.dropna(),
            alpha=0.6,
            label=group_a_name,
            bins=30,
            density=True,
        )
        ax2.hist(
            group_b_data.dropna(),
            alpha=0.6,
            label=group_b_name,
            bins=30,
            density=True,
        )
        ax2.set_title(f"{metric_name} Distribution Comparison")
        ax2.set_xlabel(metric_name)
        ax2.set_ylabel("Density")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = self.output_path / filename
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.logger.info(f"Saved visualization to {output_file}")

    def plot_summary_statistics(
        self,
        results: List[Dict],
        filename: str = "hypothesis_test_summary.png",
    ):
        """
        Create summary visualization of all hypothesis tests.

        Args:
            results: List of test result dictionaries
            filename: Output filename
        """
        # Extract p-values and test names
        test_names = []
        p_values = []
        rejections = []

        for i, result in enumerate(results):
            hypothesis_name = result["hypothesis"].split(":")[0]
            for test_name, test_result in result["tests"].items():
                if "p_value" in test_result:
                    test_names.append(f"H{i+1}: {test_name}")
                    p_values.append(test_result["p_value"])
                    rejections.append(test_result.get("reject_null", False))

        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))

        # Bar plot of p-values
        colors = ["red" if reject else "green" for reject in rejections]
        bars = ax.barh(test_names, p_values, color=colors, alpha=0.7)

        # Add significance line
        ax.axvline(x=0.05, color="red", linestyle="--", linewidth=2, label="α = 0.05")

        # Add value labels
        for i, (bar, p_val) in enumerate(zip(bars, p_values)):
            ax.text(
                p_val + 0.01,
                i,
                f"{p_val:.4f}",
                va="center",
                fontweight="bold" if rejections[i] else "normal",
            )

        ax.set_xlabel("P-value", fontsize=12)
        ax.set_title("Hypothesis Test Results Summary", fontsize=14, fontweight="bold")
        ax.set_xlim(0, max(p_values) * 1.2)
        ax.legend()
        ax.grid(True, alpha=0.3, axis="x")

        plt.tight_layout()
        output_file = self.output_path / filename
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.logger.info(f"Saved summary visualization to {output_file}")

    def plot_group_comparison_table(
        self,
        group_a_data: pd.Series,
        group_b_data: pd.Series,
        group_a_name: str,
        group_b_name: str,
        metric_name: str,
        filename: str,
    ):
        """
        Create a summary statistics table visualization.

        Args:
            group_a_data: Data for group A
            group_b_data: Data for group B
            group_a_name: Name of group A
            group_b_name: Name of group B
            metric_name: Name of the metric
            filename: Output filename
        """
        # Calculate summary statistics
        stats_a = {
            "Mean": group_a_data.mean(),
            "Median": group_a_data.median(),
            "Std": group_a_data.std(),
            "Min": group_a_data.min(),
            "Max": group_a_data.max(),
            "Count": len(group_a_data.dropna()),
        }

        stats_b = {
            "Mean": group_b_data.mean(),
            "Median": group_b_data.median(),
            "Std": group_b_data.std(),
            "Min": group_b_data.min(),
            "Max": group_b_data.max(),
            "Count": len(group_b_data.dropna()),
        }

        # Create DataFrame
        stats_df = pd.DataFrame(
            {
                group_a_name: stats_a,
                group_b_name: stats_b,
            }
        )

        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis("tight")
        ax.axis("off")

        table = ax.table(
            cellText=stats_df.values,
            rowLabels=stats_df.index,
            colLabels=stats_df.columns,
            cellLoc="center",
            loc="center",
        )

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)

        # Style header
        for i in range(len(stats_df.columns)):
            table[(0, i)].set_facecolor("#4CAF50")
            table[(0, i)].set_text_props(weight="bold", color="white")

        plt.title(f"{metric_name} - Summary Statistics", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()

        output_file = self.output_path / filename
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()

        self.logger.info(f"Saved statistics table to {output_file}")

