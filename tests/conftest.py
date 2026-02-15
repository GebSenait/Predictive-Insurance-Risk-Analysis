"""Shared pytest fixtures for the Predictive Insurance Risk Analysis tests.

All test data is synthetic. The DVC-tracked production dataset is NEVER
referenced or required by any test.

This conftest serves both:
- Legacy unit tests (tests/unit/) that use temp_dir, sample_csv_file, etc.
- New pipeline tests (tests/test_*.py) that use sample_csv_path, sample_dataframe.
"""

import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


# ---------------------------------------------------------------------------
# Fixtures for NEW pipeline tests (test_data, test_model_selector, etc.)
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_csv_path() -> Path:
    """Path to the small synthetic fixture CSV (12 rows)."""
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


# ---------------------------------------------------------------------------
# Fixtures for LEGACY unit tests (tests/unit/)
# ---------------------------------------------------------------------------

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_data_dir(temp_dir):
    """Create a sample data directory structure."""
    data_dir = temp_dir / "data"
    data_dir.mkdir()
    (data_dir / "raw").mkdir()
    (data_dir / "processed").mkdir()
    yield data_dir


@pytest.fixture
def sample_config_file(temp_dir):
    """Create a sample configuration YAML file."""
    config_path = temp_dir / "config.yaml"
    config_content = """
data:
  raw_path: "data/raw"
  processed_path: "data/processed"

logging:
  level: "INFO"
  log_file: "logs/test.log"
"""
    config_path.write_text(config_content)
    yield config_path


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file for testing the DataLoader class."""
    csv_path = temp_dir / "test_data.csv"
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    df.to_csv(csv_path, index=False)
    yield csv_path
