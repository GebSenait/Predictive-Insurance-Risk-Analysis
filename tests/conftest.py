"""Shared pytest fixtures for the Predictive Insurance Risk Analysis tests.

All test data is synthetic. The DVC-tracked production dataset is NEVER
referenced or required by any test.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def sample_csv_path() -> Path:
    """Path to the small synthetic fixture CSV."""
    return FIXTURES_DIR / "sample_insurance_data.csv"


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """In-memory synthetic DataFrame for model tests (no file I/O)."""
    return pd.DataFrame(
        {
            "feature_a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            "feature_b": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "target_reg": [1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5, 15.0],
            "target_cls": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        }
    )
