"""Data validation utilities."""

from typing import Any, Dict, List, Optional

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataValidator:
    """Class for validating data quality and structure."""

    def __init__(self):
        """Initialize DataValidator."""
        self.logger = logger

    def validate_schema(
        self,
        df: pd.DataFrame,
        required_columns: List[str],
        column_types: Optional[Dict[str, type]] = None,
    ) -> bool:
        """
        Validate that DataFrame has required columns and optional type checking.

        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            column_types: Optional dictionary mapping column names to expected types

        Returns:
            True if validation passes

        Raises:
            ValueError: If validation fails
        """
        # Check for required columns
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Check column types if provided
        if column_types:
            for col, expected_type in column_types.items():
                if col in df.columns:
                    actual_type = df[col].dtype
                    if not pd.api.types.is_dtype_equal(actual_type, expected_type):
                        self.logger.warning(
                            f"Column '{col}' has type {actual_type}, "
                            f"expected {expected_type}"
                        )

        self.logger.info("Schema validation passed")
        return True

    def check_missing_values(
        self,
        df: pd.DataFrame,
        threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Check for missing values in DataFrame.

        Args:
            df: DataFrame to check
            threshold: Threshold for considering a column as having too many
                       missing values (0.0 to 1.0)

        Returns:
            Dictionary with missing value statistics
        """
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100

        result = {
            "total_rows": len(df),
            "columns_with_missing": missing_counts[missing_counts > 0].to_dict(),
            "missing_percentages": missing_percentages[
                missing_percentages > 0
            ].to_dict(),
            "columns_above_threshold": missing_percentages[
                missing_percentages > (threshold * 100)
            ].to_dict(),
        }

        if result["columns_with_missing"]:
            self.logger.warning(
                f"Found missing values in {len(result['columns_with_missing'])} columns"
            )
        else:
            self.logger.info("No missing values found")

        return result

    def check_duplicates(
        self,
        df: pd.DataFrame,
        subset: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Check for duplicate rows in DataFrame.

        Args:
            df: DataFrame to check
            subset: Optional list of column names to consider for duplicates

        Returns:
            Dictionary with duplicate statistics
        """
        duplicate_count = df.duplicated(subset=subset).sum()

        result = {
            "total_rows": len(df),
            "duplicate_count": duplicate_count,
            "duplicate_percentage": (duplicate_count / len(df)) * 100,
        }

        if duplicate_count > 0:
            self.logger.warning(f"Found {duplicate_count} duplicate rows")
        else:
            self.logger.info("No duplicate rows found")

        return result

    def get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for the DataFrame.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with summary statistics
        """
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "missing_values": self.check_missing_values(df),
            "duplicates": self.check_duplicates(df),
        }
