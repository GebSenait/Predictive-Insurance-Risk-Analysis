"""Statistical hypothesis testing utilities."""

from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

from src.utils.logger import get_logger

logger = get_logger(__name__)


class StatisticalTester:
    """Perform statistical hypothesis tests for insurance risk analysis."""

    def __init__(self, alpha: float = 0.05):
        """
        Initialize StatisticalTester.

        Args:
            alpha: Significance level (default: 0.05)
        """
        self.logger = logger
        self.alpha = alpha

    def check_normality(self, data: pd.Series, test: str = "shapiro") -> Dict:
        """
        Check if data follows normal distribution.

        Args:
            data: Data series to test
            test: Test to use ('shapiro' or 'normaltest')

        Returns:
            Dictionary with test results
        """
        data_clean = data.dropna()

        if len(data_clean) < 3:
            return {"is_normal": False, "p_value": 1.0, "test": test}

        if test == "shapiro":
            # Shapiro-Wilk test (works well for small samples)
            if len(data_clean) > 5000:
                # Sample for large datasets
                data_sample = data_clean.sample(n=5000, random_state=42)
            else:
                data_sample = data_clean
            stat, p_value = stats.shapiro(data_sample)
        else:
            # D'Agostino and Pearson's normality test
            stat, p_value = stats.normaltest(data_clean)

        is_normal = p_value > self.alpha

        return {
            "is_normal": is_normal,
            "p_value": p_value,
            "statistic": stat,
            "test": test,
        }

    def t_test(
        self, group_a: pd.Series, group_b: pd.Series, equal_var: bool = True
    ) -> Dict:
        """
        Perform independent samples t-test.

        Args:
            group_a: First group data
            group_b: Second group data
            equal_var: Whether to assume equal variances

        Returns:
            Dictionary with test results
        """
        group_a_clean = group_a.dropna()
        group_b_clean = group_b.dropna()

        if len(group_a_clean) < 2 or len(group_b_clean) < 2:
            self.logger.warning("Insufficient data for t-test")
            return {
                "test_type": "t-test",
                "statistic": np.nan,
                "p_value": 1.0,
                "reject_null": False,
                "mean_a": np.nan,
                "mean_b": np.nan,
            }

        # Perform t-test
        stat, p_value = stats.ttest_ind(
            group_a_clean, group_b_clean, equal_var=equal_var
        )

        mean_a = group_a_clean.mean()
        mean_b = group_b_clean.mean()

        reject_null = p_value < self.alpha

        result = {
            "test_type": "t-test",
            "statistic": stat,
            "p_value": p_value,
            "reject_null": reject_null,
            "mean_a": mean_a,
            "mean_b": mean_b,
            "std_a": group_a_clean.std(),
            "std_b": group_b_clean.std(),
            "n_a": len(group_a_clean),
            "n_b": len(group_b_clean),
        }

        self.logger.info(
            f"T-test: p-value={p_value:.4f}, reject H0={reject_null}, "
            f"mean_a={mean_a:.2f}, mean_b={mean_b:.2f}"
        )

        return result

    def mannwhitney_u_test(self, group_a: pd.Series, group_b: pd.Series) -> Dict:
        """
        Perform Mann-Whitney U test (non-parametric alternative to t-test).

        Args:
            group_a: First group data
            group_b: Second group data

        Returns:
            Dictionary with test results
        """
        group_a_clean = group_a.dropna()
        group_b_clean = group_b.dropna()

        if len(group_a_clean) < 2 or len(group_b_clean) < 2:
            self.logger.warning("Insufficient data for Mann-Whitney U test")
            return {
                "test_type": "mannwhitney_u",
                "statistic": np.nan,
                "p_value": 1.0,
                "reject_null": False,
                "median_a": np.nan,
                "median_b": np.nan,
            }

        # Perform Mann-Whitney U test
        stat, p_value = stats.mannwhitneyu(
            group_a_clean, group_b_clean, alternative="two-sided"
        )

        median_a = group_a_clean.median()
        median_b = group_b_clean.median()

        reject_null = p_value < self.alpha

        result = {
            "test_type": "mannwhitney_u",
            "statistic": stat,
            "p_value": p_value,
            "reject_null": reject_null,
            "median_a": median_a,
            "median_b": median_b,
            "n_a": len(group_a_clean),
            "n_b": len(group_b_clean),
        }

        self.logger.info(
            f"Mann-Whitney U test: p-value={p_value:.4f}, reject H0={reject_null}, "
            f"median_a={median_a:.2f}, median_b={median_b:.2f}"
        )

        return result

    def chi_square_test(
        self, group_a: pd.Series, group_b: pd.Series
    ) -> Dict:
        """
        Perform chi-square test for categorical frequency differences.

        Args:
            group_a: First group data (binary: 0 or 1)
            group_b: Second group data (binary: 0 or 1)

        Returns:
            Dictionary with test results
        """
        # Create contingency table: rows = groups, columns = claim status (0 vs 1)
        group_a_clean = group_a.dropna()
        group_b_clean = group_b.dropna()
        
        # Count claims (1) and no claims (0) for each group
        contingency_data = {
            "Group A": [
                (group_a_clean == 0).sum(),  # No claims
                (group_a_clean == 1).sum(),  # Claims
            ],
            "Group B": [
                (group_b_clean == 0).sum(),  # No claims
                (group_b_clean == 1).sum(),  # Claims
            ],
        }
        contingency = pd.DataFrame(
            contingency_data,
            index=["No Claim", "Claim"],
        ).T

        if contingency.shape[0] < 2 or contingency.shape[1] < 2:
            self.logger.warning("Insufficient data for chi-square test")
            return {
                "test_type": "chi_square",
                "statistic": np.nan,
                "p_value": 1.0,
                "reject_null": False,
            }

        # Check for zero frequencies in all cells
        if (contingency == 0).all().all():
            self.logger.warning("All contingency table cells are zero")
            return {
                "test_type": "chi_square",
                "statistic": np.nan,
                "p_value": 1.0,
                "reject_null": False,
            }

        # Perform chi-square test
        stat, p_value, dof, expected = stats.chi2_contingency(contingency)

        reject_null = p_value < self.alpha

        result = {
            "test_type": "chi_square",
            "statistic": stat,
            "p_value": p_value,
            "reject_null": reject_null,
            "contingency_table": contingency,
            "expected_frequencies": expected,
        }

        self.logger.info(
            f"Chi-square test: p-value={p_value:.4f}, reject H0={reject_null}"
        )

        return result

    def test_difference(
        self,
        group_a: pd.Series,
        group_b: pd.Series,
        metric_type: str = "continuous",
        use_nonparametric: bool = False,
    ) -> Dict:
        """
        Perform appropriate statistical test based on data type.

        Args:
            group_a: First group data
            group_b: Second group data
            metric_type: Type of metric ('continuous' or 'categorical')
            use_nonparametric: Whether to use non-parametric tests

        Returns:
            Dictionary with test results
        """
        if metric_type == "categorical":
            return self.chi_square_test(group_a, group_b)
        else:
            if use_nonparametric:
                return self.mannwhitney_u_test(group_a, group_b)
            else:
                # Check normality
                norm_a = self.check_normality(group_a)
                norm_b = self.check_normality(group_b)

                # Use parametric test if both groups are normal
                if norm_a["is_normal"] and norm_b["is_normal"]:
                    return self.t_test(group_a, group_b)
                else:
                    # Use non-parametric test if data is not normal
                    self.logger.info(
                        "Data not normally distributed, using Mann-Whitney U test"
                    )
                    return self.mannwhitney_u_test(group_a, group_b)

