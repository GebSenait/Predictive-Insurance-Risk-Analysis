"""Main hypothesis testing script for Task 3."""

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from src.analysis.task3.metrics import MetricCalculator
from src.analysis.task3.segmentation import DataSegmentation
from src.analysis.task3.statistical_tests import StatisticalTester
from src.data.loaders import DataLoader
from src.utils.config import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HypothesisTestingRunner:
    """Run all hypothesis tests for Task 3."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize HypothesisTestingRunner.

        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.logger = logger
        self.metric_calculator = MetricCalculator()
        self.segmentation = DataSegmentation()
        self.tester = StatisticalTester()

        # Setup paths
        data_path = Path(self.config["data"]["raw_path"])
        self.data_loader = DataLoader(data_path=data_path)
        self.results_path = Path(self.config["output"]["results_path"])
        self.reports_path = Path(self.config["output"]["reports_path"])
        self.figures_path = Path(self.config["output"]["figures_path"])

        # Create output directories
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self.figures_path.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> pd.DataFrame:
        """
        Load the insurance dataset.

        Returns:
            Loaded DataFrame
        """
        self.logger.info("Loading insurance dataset...")
        df = self.data_loader.load_csv(
            "MachineLearningRating_v3.txt", sep="|", low_memory=False
        )
        self.logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df

    def test_province_risk_differences(self, df: pd.DataFrame) -> Dict:
        """
        Test H₀: No risk differences across provinces.

        Tests both claim frequency and claim severity.

        Args:
            df: DataFrame with insurance data

        Returns:
            Dictionary with test results
        """
        self.logger.info("=" * 80)
        self.logger.info("HYPOTHESIS 1: No risk differences across provinces")
        self.logger.info("=" * 80)

        # Create province groups
        group_a, group_b, group_info = self.segmentation.create_province_groups(
            df, min_samples=1000
        )

        results = {
            "hypothesis": "H₀: No risk differences across provinces",
            "group_info": group_info,
            "tests": {},
        }

        # Test Claim Frequency
        self.logger.info("\n--- Testing Claim Frequency ---")
        freq_a = self.metric_calculator.calculate_claim_frequency(group_a)
        freq_b = self.metric_calculator.calculate_claim_frequency(group_b)
        freq_test = self.tester.test_difference(
            freq_a, freq_b, metric_type="categorical"
        )
        # Add loss ratio for context
        loss_ratio_a = self.metric_calculator.calculate_loss_ratio(group_a, group_col=None).mean()
        loss_ratio_b = self.metric_calculator.calculate_loss_ratio(group_b, group_col=None).mean()
        freq_test["loss_ratio_a"] = loss_ratio_a
        freq_test["loss_ratio_b"] = loss_ratio_b
        if not pd.isna(loss_ratio_a) and not pd.isna(loss_ratio_b) and loss_ratio_a > 0:
            freq_test["loss_ratio_diff_pct"] = ((loss_ratio_b - loss_ratio_a) / loss_ratio_a) * 100
        results["tests"]["claim_frequency"] = freq_test

        # Test Claim Severity (only for policies with claims)
        self.logger.info("\n--- Testing Claim Severity ---")
        severity_a = self.metric_calculator.calculate_claim_severity(group_a)
        severity_b = self.metric_calculator.calculate_claim_severity(group_b)
        severity_test = self.tester.test_difference(
            severity_a, severity_b, metric_type="continuous"
        )
        results["tests"]["claim_severity"] = severity_test

        return results

    def test_zipcode_risk_differences(self, df: pd.DataFrame) -> Dict:
        """
        Test H₀: No risk differences between zip codes.

        Tests both claim frequency and claim severity.

        Args:
            df: DataFrame with insurance data

        Returns:
            Dictionary with test results
        """
        self.logger.info("=" * 80)
        self.logger.info("HYPOTHESIS 2: No risk differences between zip codes")
        self.logger.info("=" * 80)

        # Create zip code groups
        group_a, group_b, group_info = self.segmentation.create_zipcode_groups(
            df, min_samples=500
        )

        results = {
            "hypothesis": "H₀: No risk differences between zip codes",
            "group_info": group_info,
            "tests": {},
        }

        # Test Claim Frequency
        self.logger.info("\n--- Testing Claim Frequency ---")
        freq_a = self.metric_calculator.calculate_claim_frequency(group_a)
        freq_b = self.metric_calculator.calculate_claim_frequency(group_b)
        freq_test = self.tester.test_difference(
            freq_a, freq_b, metric_type="categorical"
        )
        # Add loss ratio for context
        loss_ratio_a = self.metric_calculator.calculate_loss_ratio(group_a, group_col=None).mean()
        loss_ratio_b = self.metric_calculator.calculate_loss_ratio(group_b, group_col=None).mean()
        freq_test["loss_ratio_a"] = loss_ratio_a
        freq_test["loss_ratio_b"] = loss_ratio_b
        if not pd.isna(loss_ratio_a) and not pd.isna(loss_ratio_b) and loss_ratio_a > 0:
            freq_test["loss_ratio_diff_pct"] = ((loss_ratio_b - loss_ratio_a) / loss_ratio_a) * 100
        results["tests"]["claim_frequency"] = freq_test

        # Test Claim Severity
        self.logger.info("\n--- Testing Claim Severity ---")
        severity_a = self.metric_calculator.calculate_claim_severity(group_a)
        severity_b = self.metric_calculator.calculate_claim_severity(group_b)
        severity_test = self.tester.test_difference(
            severity_a, severity_b, metric_type="continuous"
        )
        results["tests"]["claim_severity"] = severity_test

        return results

    def test_zipcode_margin_differences(self, df: pd.DataFrame) -> Dict:
        """
        Test H₀: No significant margin (profit) difference between zip codes.

        Args:
            df: DataFrame with insurance data

        Returns:
            Dictionary with test results
        """
        self.logger.info("=" * 80)
        self.logger.info("HYPOTHESIS 3: No significant margin difference between zip codes")
        self.logger.info("=" * 80)

        # Create zip code groups
        group_a, group_b, group_info = self.segmentation.create_zipcode_groups(
            df, min_samples=500
        )

        results = {
            "hypothesis": "H₀: No significant margin difference between zip codes",
            "group_info": group_info,
            "tests": {},
        }

        # Test Margin
        self.logger.info("\n--- Testing Margin ---")
        margin_a = self.metric_calculator.calculate_margin(group_a)
        margin_b = self.metric_calculator.calculate_margin(group_b)
        margin_test = self.tester.test_difference(
            margin_a, margin_b, metric_type="continuous"
        )
        results["tests"]["margin"] = margin_test

        return results

    def test_gender_risk_differences(self, df: pd.DataFrame) -> Dict:
        """
        Test H₀: No significant risk difference between women and men.

        Tests both claim frequency and claim severity.

        Args:
            df: DataFrame with insurance data

        Returns:
            Dictionary with test results
        """
        self.logger.info("=" * 80)
        self.logger.info("HYPOTHESIS 4: No significant risk difference between genders")
        self.logger.info("=" * 80)

        # Create gender groups
        group_a, group_b, group_info = self.segmentation.create_gender_groups(
            df, min_samples=1000
        )

        results = {
            "hypothesis": "H₀: No significant risk difference between genders",
            "group_info": group_info,
            "tests": {},
        }

        # Test Claim Frequency
        self.logger.info("\n--- Testing Claim Frequency ---")
        freq_a = self.metric_calculator.calculate_claim_frequency(group_a)
        freq_b = self.metric_calculator.calculate_claim_frequency(group_b)
        freq_test = self.tester.test_difference(
            freq_a, freq_b, metric_type="categorical"
        )
        # Add loss ratio for context
        loss_ratio_a = self.metric_calculator.calculate_loss_ratio(group_a, group_col=None).mean()
        loss_ratio_b = self.metric_calculator.calculate_loss_ratio(group_b, group_col=None).mean()
        freq_test["loss_ratio_a"] = loss_ratio_a
        freq_test["loss_ratio_b"] = loss_ratio_b
        if not pd.isna(loss_ratio_a) and not pd.isna(loss_ratio_b) and loss_ratio_a > 0:
            freq_test["loss_ratio_diff_pct"] = ((loss_ratio_b - loss_ratio_a) / loss_ratio_a) * 100
        results["tests"]["claim_frequency"] = freq_test

        # Test Claim Severity
        self.logger.info("\n--- Testing Claim Severity ---")
        severity_a = self.metric_calculator.calculate_claim_severity(group_a)
        severity_b = self.metric_calculator.calculate_claim_severity(group_b)
        severity_test = self.tester.test_difference(
            severity_a, severity_b, metric_type="continuous"
        )
        results["tests"]["claim_severity"] = severity_test

        return results

    def run_all_tests(self) -> List[Dict]:
        """
        Run all hypothesis tests.

        Returns:
            List of test result dictionaries
        """
        self.logger.info("Starting Task 3: Statistical Validation of Risk Drivers")
        self.logger.info("=" * 80)

        # Load data
        df = self.load_data()

        # Run all hypothesis tests
        all_results = []

        # Hypothesis 1: Province risk differences
        results_1 = self.test_province_risk_differences(df)
        all_results.append(results_1)

        # Hypothesis 2: Zip code risk differences
        results_2 = self.test_zipcode_risk_differences(df)
        all_results.append(results_2)

        # Hypothesis 3: Zip code margin differences
        results_3 = self.test_zipcode_margin_differences(df)
        all_results.append(results_3)

        # Hypothesis 4: Gender risk differences
        results_4 = self.test_gender_risk_differences(df)
        all_results.append(results_4)

        return all_results

    def save_results(self, results: List[Dict], filename: str = "task3_results.json"):
        """
        Save test results to JSON file.

        Args:
            results: List of test result dictionaries
            filename: Output filename
        """
        output_path = self.results_path / filename

        # Convert numpy types to native Python types for JSON serialization
        def convert_to_serializable(obj):
            """Convert numpy types to Python native types."""
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, (pd.DataFrame, pd.Series)):
                return obj.to_dict()
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj) if isinstance(obj, np.floating) else int(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif pd.isna(obj):
                return None
            else:
                return obj

        serializable_results = convert_to_serializable(results)

        with open(output_path, "w") as f:
            json.dump(serializable_results, f, indent=2, default=str)

        self.logger.info(f"Results saved to {output_path}")


if __name__ == "__main__":
    runner = HypothesisTestingRunner()
    results = runner.run_all_tests()
    runner.save_results(results)

