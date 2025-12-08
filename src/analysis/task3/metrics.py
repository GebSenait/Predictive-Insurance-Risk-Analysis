"""Metric computation for insurance risk analysis."""

from typing import Dict, Optional

import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class MetricCalculator:
    """Calculate insurance risk metrics for hypothesis testing."""

    def __init__(self):
        """Initialize MetricCalculator."""
        self.logger = logger

    def calculate_claim_frequency(
        self, df: pd.DataFrame, group_col: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate claim frequency (number of claims per policy).

        Args:
            df: DataFrame with insurance data
            group_col: Optional column to group by

        Returns:
            Series with claim frequency values
        """
        if group_col:
            # Group-level claim frequency
            grouped = df.groupby(group_col)
            total_policies = grouped.size()
            total_claims = grouped["TotalClaims"].sum()
            # Avoid division by zero
            claim_freq = total_claims / total_policies.replace(0, np.nan)
            return claim_freq
        else:
            # Policy-level claim frequency (binary: 0 or 1+)
            claim_freq = (df["TotalClaims"] > 0).astype(int)
            return claim_freq

    def calculate_claim_severity(
        self, df: pd.DataFrame, group_col: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate claim severity (average claim amount when claims occur).

        Args:
            df: DataFrame with insurance data
            group_col: Optional column to group by

        Returns:
            Series with claim severity values
        """
        if group_col:
            # Group-level claim severity
            grouped = df.groupby(group_col)
            total_claims_amount = grouped["TotalClaims"].sum()
            num_claims = grouped.apply(
                lambda x: (x["TotalClaims"] > 0).sum()
            )  # Count policies with claims
            # Average claim amount per claim
            claim_severity = total_claims_amount / num_claims.replace(0, np.nan)
            return claim_severity
        else:
            # Policy-level claim severity (only for policies with claims)
            claim_severity = df["TotalClaims"].copy()
            # Set to NaN for policies without claims
            claim_severity[claim_severity == 0] = np.nan
            return claim_severity

    def calculate_margin(
        self, df: pd.DataFrame, group_col: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate margin (TotalPremium - TotalClaims).

        Args:
            df: DataFrame with insurance data
            group_col: Optional column to group by

        Returns:
            Series with margin values
        """
        if group_col:
            # Group-level margin
            grouped = df.groupby(group_col)
            total_premium = grouped["TotalPremium"].sum()
            total_claims = grouped["TotalClaims"].sum()
            margin = total_premium - total_claims
            return margin
        else:
            # Policy-level margin
            margin = df["TotalPremium"] - df["TotalClaims"]
            return margin

    def calculate_loss_ratio(
        self, df: pd.DataFrame, group_col: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate loss ratio (TotalClaims / TotalPremium).

        Args:
            df: DataFrame with insurance data
            group_col: Optional column to group by

        Returns:
            Series with loss ratio values
        """
        if group_col:
            # Group-level loss ratio
            grouped = df.groupby(group_col)
            total_premium = grouped["TotalPremium"].sum()
            total_claims = grouped["TotalClaims"].sum()
            # Avoid division by zero
            loss_ratio = total_claims / total_premium.replace(0, np.nan)
            return loss_ratio
        else:
            # Policy-level loss ratio
            loss_ratio = df["TotalClaims"] / df["TotalPremium"].replace(0, np.nan)
            return loss_ratio

    def compute_all_metrics(
        self, df: pd.DataFrame, group_col: Optional[str] = None
    ) -> Dict[str, pd.Series]:
        """
        Compute all metrics for a dataset.

        Args:
            df: DataFrame with insurance data
            group_col: Optional column to group by

        Returns:
            Dictionary with all computed metrics
        """
        metrics = {
            "claim_frequency": self.calculate_claim_frequency(df, group_col),
            "claim_severity": self.calculate_claim_severity(df, group_col),
            "margin": self.calculate_margin(df, group_col),
            "loss_ratio": self.calculate_loss_ratio(df, group_col),
        }
        return metrics

