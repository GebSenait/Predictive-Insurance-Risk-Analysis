"""Unit tests for data validators."""

import pandas as pd
import pytest

from src.data.validators import DataValidator


def test_validate_schema_success():
    """Test successful schema validation."""
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    validator = DataValidator()
    result = validator.validate_schema(df, required_columns=["col1", "col2"])
    assert result is True


def test_validate_schema_missing_column():
    """Test schema validation with missing column."""
    df = pd.DataFrame({"col1": [1, 2, 3]})
    validator = DataValidator()
    with pytest.raises(ValueError, match="Missing required columns"):
        validator.validate_schema(df, required_columns=["col1", "col2"])


def test_check_missing_values_no_missing():
    """Test missing value check with no missing values."""
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    validator = DataValidator()
    result = validator.check_missing_values(df)
    assert result["columns_with_missing"] == {}


def test_check_duplicates_no_duplicates():
    """Test duplicate check with no duplicates."""
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    validator = DataValidator()
    result = validator.check_duplicates(df)
    assert result["duplicate_count"] == 0

