"""Unit tests for data loaders."""

from pathlib import Path

import pandas as pd
import pytest

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
    df = loader.load_csv(sample_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_csv_file_not_found():
    """Test CSV loading with non-existent file."""
    loader = DataLoader()
    with pytest.raises(FileNotFoundError):
        loader.load_csv("nonexistent_file.csv")
