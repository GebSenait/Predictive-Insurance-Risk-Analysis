"""Reproducibility enforcement tests.

Ensures deterministic model training by validating that critical
configuration parameters are pinned to known values.
"""

from src.utils.config import load_config


def test_random_state_is_fixed():
    """Config must enforce a fixed random_state for deterministic runs."""
    config = load_config()
    assert config["analysis"]["task4"]["random_state"] == 42
