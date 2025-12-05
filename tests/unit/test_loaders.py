"""Unit tests for data loaders."""

import pandas as pd
import pytest
from pathlib import Path

from src.data.loaders import DataLoader


def test_dataloader_init():
    """Test DataLoader initialization."""
    loader = DataLoader()
    assert loader.data_path is None

    loader = DataLoader(data_path=Path("data"))
    assert loader.data_path == Path("data")


def test_load_csv_success(temp_dir, sample_csv_file):
    """Test successful CSV loading."""
    loader = DataLoader(data_path=temp_dir)
    df = loader.load_csv(sample_csv_file.name)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_csv_file_not_found():
    """Test CSV loading with non-existent file."""
    loader = DataLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_csv("nonexistent_file.csv")


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file for testing."""
    csv_path = temp_dir / "test_data.csv"
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    df.to_csv(csv_path, index=False)
    yield csv_path

