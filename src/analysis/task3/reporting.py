"""Report generation for Task 3 statistical analysis."""

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generate comprehensive reports for hypothesis testing results."""

    def __init__(self, output_path: Path):
        """
        Initialize ReportGenerator.

        Args:
            output_path: Path to save reports
        """
        self.logger = logger
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def generate_results_table(self, results: List[Dict]) -> pd.DataFrame:
        """
        Generate a summary table of all test results.

        Args:
            results: List of test result dictionaries

        Returns:
            DataFrame with summary results
        """
        rows = []

        for i, result in enumerate(results):
            hypothesis = result["hypothesis"]
            group_info = result.get("group_info", {})

            for test_name, test_result in result.get("tests", {}).items():
                row = {
                    "Hypothesis": f"H{i+1}",
                    "Null Hypothesis": hypothesis,
                    "Metric": test_name,
                    "Test Type": test_result.get("test_type", "N/A"),
                    "P-value": test_result.get("p_value", np.nan),
                    "Reject H₀": test_result.get("reject_null", False),
                    "Group A": group_info.get("group_a_name", "N/A"),
                    "Group B": group_info.get("group_b_name", "N/A"),
                    "N (Group A)": group_info.get("group_a_size", 0),
                    "N (Group B)": group_info.get("group_b_size", 0),
                }

                # Add metric-specific statistics
                if "mean_a" in test_result:
                    row["Mean (A)"] = test_result.get("mean_a", np.nan)
                    row["Mean (B)"] = test_result.get("mean_b", np.nan)
                elif "median_a" in test_result:
                    row["Median (A)"] = test_result.get("median_a", np.nan)
                    row["Median (B)"] = test_result.get("median_b", np.nan)

                rows.append(row)

        df = pd.DataFrame(rows)
        return df

    def generate_markdown_report(
        self, results: List[Dict], filename: str = "task3_statistical_report.md"
    ) -> str:
        """
        Generate a comprehensive markdown report.

        Args:
            results: List of test result dictionaries
            filename: Output filename

        Returns:
            Markdown report content
        """
        report_lines = [
            "# Task 3: Statistical Validation of Risk Drivers",
            "",
            "## Executive Summary",
            "",
            "This report presents the results of statistical hypothesis testing to validate "
            "key assumptions about insurance risk drivers. The analysis tests four null "
            "hypotheses related to geographic, demographic, and profitability dimensions.",
            "",
            "---",
            "",
        ]

        # Process each hypothesis
        for i, result in enumerate(results):
            hypothesis = result["hypothesis"]
            group_info = result.get("group_info", {})
            tests = result.get("tests", {})

            report_lines.extend(
                [
                    f"## Hypothesis {i+1}",
                    "",
                    f"**Null Hypothesis:** {hypothesis}",
                    "",
                    f"**Comparison Groups:**",
                    f"- Group A: {group_info.get('group_a_name', 'N/A')} (n={group_info.get('group_a_size', 0):,})",
                    f"- Group B: {group_info.get('group_b_name', 'N/A')} (n={group_info.get('group_b_size', 0):,})",
                    "",
                ]
            )

            # Add test results
            for test_name, test_result in tests.items():
                p_value = test_result.get("p_value", np.nan)
                reject = test_result.get("reject_null", False)
                test_type = test_result.get("test_type", "N/A")

                report_lines.extend(
                    [
                        f"### {test_name.replace('_', ' ').title()}",
                        "",
                        f"- **Test Type:** {test_type}",
                        f"- **P-value:** {p_value:.4f}",
                        f"- **Significance Level (α):** 0.05",
                        f"- **Conclusion:** {'**REJECT H₀**' if reject else '**FAIL TO REJECT H₀**'}",
                        "",
                    ]
                )

                # Add metric-specific details
                if "mean_a" in test_result:
                    report_lines.extend(
                        [
                            f"- **Mean (Group A):** {test_result.get('mean_a', np.nan):.2f}",
                            f"- **Mean (Group B):** {test_result.get('mean_b', np.nan):.2f}",
                            f"- **Difference:** {test_result.get('mean_b', np.nan) - test_result.get('mean_a', np.nan):.2f}",
                            "",
                        ]
                    )
                elif "median_a" in test_result:
                    report_lines.extend(
                        [
                            f"- **Median (Group A):** {test_result.get('median_a', np.nan):.2f}",
                            f"- **Median (Group B):** {test_result.get('median_b', np.nan):.2f}",
                            "",
                        ]
                    )

                # Business interpretation
                if reject:
                    interpretation = self._generate_business_interpretation(
                        i + 1, test_name, test_result, group_info
                    )
                    report_lines.extend(
                        [
                            "**Business Interpretation:**",
                            "",
                            interpretation,
                            "",
                        ]
                    )

            report_lines.append("---")
            report_lines.append("")

        # Summary table
        report_lines.extend(
            [
                "## Summary Table",
                "",
                "| Hypothesis | Metric | P-value | Reject H₀ | Conclusion |",
                "|------------|--------|---------|------------|------------|",
            ]
        )

        for i, result in enumerate(results):
            for test_name, test_result in result.get("tests", {}).items():
                p_value = test_result.get("p_value", np.nan)
                reject = test_result.get("reject_null", False)
                conclusion = (
                    "Significant difference" if reject else "No significant difference"
                )

                report_lines.append(
                    f"| H{i+1} | {test_name.replace('_', ' ').title()} | "
                    f"{p_value:.4f} | {'Yes' if reject else 'No'} | {conclusion} |"
                )

        report_lines.extend(["", "---", ""])

        # Save report
        report_content = "\n".join(report_lines)
        output_file = self.output_path / filename

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        self.logger.info(f"Report saved to {output_file}")

        return report_content

    def _generate_business_interpretation(
        self, hypothesis_num: int, test_name: str, test_result: Dict, group_info: Dict
    ) -> str:
        """
        Generate business interpretation for rejected hypotheses.

        Args:
            hypothesis_num: Hypothesis number
            test_name: Name of the test metric
            test_result: Test result dictionary
            group_info: Group information dictionary

        Returns:
            Business interpretation string
        """
        group_a_name = group_info.get("group_a_name", "Group A")
        group_b_name = group_info.get("group_b_name", "Group B")
        p_value = test_result.get("p_value", np.nan)

        # Get loss ratio information if available
        loss_ratio_a = test_result.get("loss_ratio_a", np.nan)
        loss_ratio_b = test_result.get("loss_ratio_b", np.nan)
        loss_ratio_diff_pct = test_result.get("loss_ratio_diff_pct", np.nan)

        interpretations = {
            (1, "claim_frequency"): (
                f"We reject H₀ for claim frequency across provinces (p < {p_value:.3f}). "
                f"{group_a_name} and {group_b_name} show statistically significant differences "
                f"in claim frequency. "
                + (
                    f"{group_b_name} shows {abs(loss_ratio_diff_pct):.1f}% {'higher' if loss_ratio_diff_pct > 0 else 'lower'} loss ratio than {group_a_name} "
                    f"({loss_ratio_b:.3f} vs {loss_ratio_a:.3f}). "
                    if not pd.isna(loss_ratio_diff_pct)
                    else ""
                )
                + f"This suggests that regional risk factors vary by province, "
                f"and ACIS should consider province-based premium adjustments in their pricing model."
            ),
            (1, "claim_severity"): (
                f"We reject H₀ for claim severity across provinces (p < {p_value:.3f}). "
                f"Claim amounts differ significantly between {group_a_name} and {group_b_name}. "
                f"This indicates that not only do provinces differ in claim frequency, but also "
                f"in the severity of claims when they occur. Regional pricing strategies should "
                f"account for both frequency and severity differences."
            ),
            (2, "claim_frequency"): (
                f"We reject H₀ for claim frequency between zip codes (p < {p_value:.3f}). "
                f"Zip codes {group_a_name} and {group_b_name} exhibit different risk profiles. "
                + (
                    f"Zip code {group_b_name} shows {abs(loss_ratio_diff_pct):.1f}% {'higher' if loss_ratio_diff_pct > 0 else 'lower'} loss ratio than {group_a_name} "
                    f"({loss_ratio_b:.3f} vs {loss_ratio_a:.3f}). "
                    if not pd.isna(loss_ratio_diff_pct)
                    else ""
                )
                + f"This granular geographic segmentation can inform more precise pricing strategies "
                f"and risk assessment at the local level."
            ),
            (2, "claim_severity"): (
                f"We reject H₀ for claim severity between zip codes (p < {p_value:.3f}). "
                f"Significant differences in claim amounts between zip codes {group_a_name} and "
                f"{group_b_name} suggest that local factors (e.g., traffic patterns, crime rates, "
                f"infrastructure) impact claim severity. Consider zip code-level risk adjustments."
            ),
            (3, "margin"): (
                f"We reject H₀ for margin differences between zip codes (p < {p_value:.3f}). "
                f"Profitability (TotalPremium - TotalClaims) differs significantly between "
                f"zip codes {group_a_name} and {group_b_name}. This indicates that some "
                f"geographic areas are more profitable than others. ACIS should review pricing "
                f"strategies for underperforming zip codes and consider reallocating resources "
                f"or adjusting premiums to improve profitability."
            ),
            (4, "claim_frequency"): (
                f"We reject H₀ for claim frequency between genders (p < {p_value:.3f}). "
                f"Statistically significant differences exist between {group_a_name} and "
                f"{group_b_name} in terms of claim frequency. "
                + (
                    f"{group_b_name} shows {abs(loss_ratio_diff_pct):.1f}% {'higher' if loss_ratio_diff_pct > 0 else 'lower'} loss ratio than {group_a_name} "
                    f"({loss_ratio_b:.3f} vs {loss_ratio_a:.3f}). "
                    if not pd.isna(loss_ratio_diff_pct)
                    else ""
                )
                + f"However, note that gender-based pricing may be subject to regulatory restrictions. "
                f"Consider this finding in conjunction with other risk factors and regulatory compliance requirements."
            ),
            (4, "claim_severity"): (
                f"We reject H₀ for claim severity between genders (p < {p_value:.3f}). "
                f"Claim amounts differ significantly between {group_a_name} and {group_b_name}. "
                f"While this finding is statistically significant, ensure that any pricing "
                f"decisions comply with applicable regulations regarding gender-based discrimination."
            ),
        }

        key = (hypothesis_num, test_name)
        if key in interpretations:
            return interpretations[key]
        else:
            return (
                f"Statistically significant difference detected (p < {p_value:.3f}). "
                f"Consider business implications and regulatory compliance when implementing "
                f"changes based on this finding."
            )

    def save_results_table(
        self, results: List[Dict], filename: str = "task3_results_table.csv"
    ):
        """
        Save results table to CSV.

        Args:
            results: List of test result dictionaries
            filename: Output filename
        """
        df = self.generate_results_table(results)
        output_file = self.output_path / filename
        df.to_csv(output_file, index=False)
        self.logger.info(f"Results table saved to {output_file}")
