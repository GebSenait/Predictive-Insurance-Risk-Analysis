"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil


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
    """Create a sample configuration file."""
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

