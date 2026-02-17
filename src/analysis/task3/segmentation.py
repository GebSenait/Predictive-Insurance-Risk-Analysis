"""Data segmentation for A/B hypothesis testing."""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataSegmentation:
    """Create A/B test groups for hypothesis testing."""

    def __init__(self, random_seed: int = 42):
        """
        Initialize DataSegmentation.

        Args:
            random_seed: Random seed for reproducibility
        """
        self.logger = logger
        self.random_seed = random_seed
        np.random.seed(random_seed)

    def create_province_groups(
        self, df: pd.DataFrame, min_samples: int = 100
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, int]]:
        """
        Create A/B groups for province comparison.

        Selects two provinces with sufficient sample sizes and similar
        characteristics for comparison.

        Args:
            df: DataFrame with insurance data
            min_samples: Minimum number of samples per province

        Returns:
            Tuple of (group_a_df, group_b_df, group_info)
        """
        # Count samples per province
        province_counts = df["Province"].value_counts()
        valid_provinces = province_counts[province_counts >= min_samples].index.tolist()

        if len(valid_provinces) < 2:
            self.logger.warning(
                f"Only {len(valid_provinces)} provinces meet minimum sample size. "
                f"Using all available provinces."
            )
            valid_provinces = province_counts.index.tolist()[:2]

        # Select two provinces with largest sample sizes
        selected_provinces = valid_provinces[:2]
        province_a, province_b = selected_provinces[0], selected_provinces[1]

        group_a = df[df["Province"] == province_a].copy()
        group_b = df[df["Province"] == province_b].copy()

        group_info = {
            "group_a_name": province_a,
            "group_b_name": province_b,
            "group_a_size": len(group_a),
            "group_b_size": len(group_b),
        }

        self.logger.info(
            f"Created province groups: {province_a} (n={len(group_a)}) vs "
            f"{province_b} (n={len(group_b)})"
        )

        return group_a, group_b, group_info

    def create_zipcode_groups(
        self, df: pd.DataFrame, min_samples: int = 50
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, int]]:
        """
        Create A/B groups for zip code comparison.

        Selects two zip codes with sufficient sample sizes.

        Args:
            df: DataFrame with insurance data
            min_samples: Minimum number of samples per zip code

        Returns:
            Tuple of (group_a_df, group_b_df, group_info)
        """
        # Count samples per zip code
        zipcode_counts = df["PostalCode"].value_counts()
        valid_zipcodes = zipcode_counts[zipcode_counts >= min_samples].index.tolist()

        if len(valid_zipcodes) < 2:
            self.logger.warning(
                f"Only {len(valid_zipcodes)} zip codes meet minimum sample size. "
                f"Using all available zip codes."
            )
            valid_zipcodes = zipcode_counts.index.tolist()[:2]

        # Select two zip codes with largest sample sizes
        selected_zipcodes = valid_zipcodes[:2]
        zipcode_a, zipcode_b = selected_zipcodes[0], selected_zipcodes[1]

        group_a = df[df["PostalCode"] == zipcode_a].copy()
        group_b = df[df["PostalCode"] == zipcode_b].copy()

        group_info = {
            "group_a_name": str(zipcode_a),
            "group_b_name": str(zipcode_b),
            "group_a_size": len(group_a),
            "group_b_size": len(group_b),
        }

        self.logger.info(
            f"Created zip code groups: {zipcode_a} (n={len(group_a)}) vs "
            f"{zipcode_b} (n={len(group_b)})"
        )

        return group_a, group_b, group_info

    def create_gender_groups(
        self, df: pd.DataFrame, min_samples: int = 100
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, int]]:
        """
        Create A/B groups for gender comparison.

        Args:
            df: DataFrame with insurance data
            min_samples: Minimum number of samples per gender

        Returns:
            Tuple of (group_a_df, group_b_df, group_info)
        """
        # Filter out 'Not specified' or missing genders
        gender_df = df[df["Gender"].notna()].copy()
        gender_df = gender_df[gender_df["Gender"] != "Not specified"]

        # Get gender counts
        gender_counts = gender_df["Gender"].value_counts()
        valid_genders = gender_counts[gender_counts >= min_samples].index.tolist()

        if len(valid_genders) < 2:
            self.logger.warning(
                f"Only {len(valid_genders)} genders meet minimum sample size. "
                f"Using all available genders."
            )
            valid_genders = gender_counts.index.tolist()[:2]

        # Select two genders (typically Male and Female)
        selected_genders = valid_genders[:2]
        gender_a, gender_b = selected_genders[0], selected_genders[1]

        group_a = gender_df[gender_df["Gender"] == gender_a].copy()
        group_b = gender_df[gender_df["Gender"] == gender_b].copy()

        group_info = {
            "group_a_name": gender_a,
            "group_b_name": gender_b,
            "group_a_size": len(group_a),
            "group_b_size": len(group_b),
        }

        self.logger.info(
            f"Created gender groups: {gender_a} (n={len(group_a)}) vs "
            f"{gender_b} (n={len(group_b)})"
        )

        return group_a, group_b, group_info

    def balance_groups(
        self,
        group_a: pd.DataFrame,
        group_b: pd.DataFrame,
        method: str = "undersample",
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Balance two groups to have similar sample sizes.

        Args:
            group_a: First group DataFrame
            group_b: Second group DataFrame
            method: Balancing method ('undersample' or 'oversample')

        Returns:
            Tuple of balanced DataFrames
        """
        size_a, size_b = len(group_a), len(group_b)

        if method == "undersample":
            # Undersample the larger group
            min_size = min(size_a, size_b)
            if size_a > size_b:
                group_a = group_a.sample(n=min_size, random_state=self.random_seed)
            elif size_b > size_a:
                group_b = group_b.sample(n=min_size, random_state=self.random_seed)
        elif method == "oversample":
            # Oversample the smaller group (with replacement)
            max_size = max(size_a, size_b)
            if size_a < size_b:
                group_a = group_a.sample(
                    n=max_size, replace=True, random_state=self.random_seed
                )
            elif size_b < size_a:
                group_b = group_b.sample(
                    n=max_size, replace=True, random_state=self.random_seed
                )

        self.logger.info(
            f"Balanced groups: Group A (n={len(group_a)}) vs Group B (n={len(group_b)})"
        )

        return group_a, group_b
