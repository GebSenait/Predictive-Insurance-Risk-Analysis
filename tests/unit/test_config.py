"""Unit tests for configuration management."""

from pathlib import Path

import pytest

from src.utils.config import get_config, load_config


def test_load_config_success(sample_config_file):
    """Test successful configuration loading."""
    config = load_config(sample_config_file)
    assert "data" in config
    assert "logging" in config


def test_load_config_file_not_found():
    """Test configuration loading with non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_config(Path("nonexistent_config.yaml"))


def test_get_config(sample_config_file):
    """Test getting configuration values."""
    load_config(sample_config_file)
    log_level = get_config("logging.level")
    assert log_level == "INFO"
