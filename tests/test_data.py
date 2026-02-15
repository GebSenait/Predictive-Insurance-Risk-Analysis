"""Tests for data loading and preprocessing modules.

Uses the synthetic fixture CSV — never touches DVC data.
"""

from pathlib import Path

import pandas as pd
import pytest

from src.data.loaders import load_insurance_data
from src.data.preprocessing import (
    encode_categoricals,
    engineer_features,
    handle_missing_values,
    prepare_features_target,
    run_preprocessing_pipeline,
)


class TestLoadInsuranceData:
    """Tests for the data loader."""

    def test_load_fixture_csv(self, sample_csv_path: Path) -> None:
        """Loader reads the synthetic fixture CSV correctly."""
        df = load_insurance_data(file_path=sample_csv_path, sep=",")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 12
        assert "TotalPremium" in df.columns
        assert "TotalClaims" in df.columns

    def test_load_missing_file_raises(self, tmp_path: Path) -> None:
        """Loader raises FileNotFoundError for non-existent paths."""
        with pytest.raises(FileNotFoundError):
            load_insurance_data(file_path=tmp_path / "nonexistent.csv")


class TestPreprocessing:
    """Tests for preprocessing functions."""

    def test_handle_missing_values(self) -> None:
        """Missing values are filled (median for numeric, mode for object)."""
        df = pd.DataFrame(
            {
                "num": [1.0, None, 3.0],
                "cat": ["a", None, "a"],
            }
        )
        result = handle_missing_values(df)
        assert result["num"].isnull().sum() == 0
        assert result["cat"].isnull().sum() == 0
        # Median of [1,3] = 2.0
        assert result["num"].iloc[1] == 2.0

    def test_engineer_features_adds_columns(self, sample_csv_path: Path) -> None:
        """Feature engineering creates HasClaim, LossRatio, ProfitMargin."""
        df = load_insurance_data(file_path=sample_csv_path, sep=",")
        result = engineer_features(df)
        assert "HasClaim" in result.columns
        assert "LossRatio" in result.columns
        assert "ProfitMargin" in result.columns

    def test_encode_categoricals(self) -> None:
        """Categorical columns are label-encoded to numeric."""
        df = pd.DataFrame({"Province": ["A", "B", "A"], "Age": [30, 40, 50]})
        result = encode_categoricals(df)
        assert result["Province"].dtype != object

    def test_run_preprocessing_pipeline(self, sample_csv_path: Path) -> None:
        """Full preprocessing pipeline returns correct split shapes."""
        df = load_insurance_data(file_path=sample_csv_path, sep=",")
        X_train, X_test, y_train, y_test = run_preprocessing_pipeline(
            df, target_col="TotalPremium", test_size=0.3, random_state=42
        )
        assert len(X_train) + len(X_test) == len(df)
        assert len(y_train) == len(X_train)
        assert len(y_test) == len(X_test)
