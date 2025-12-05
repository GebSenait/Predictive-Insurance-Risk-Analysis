"""Configuration management module."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


# Global config storage
_config: Optional[Dict[str, Any]] = None


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file and environment variables.

    Args:
        config_path: Path to configuration YAML file. If None, looks for
                     config/config.yaml in project root.

    Returns:
        Dictionary containing configuration
    """
    global _config

    # Load environment variables
    load_dotenv()

    # Determine config path
    if config_path is None:
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "config.yaml"

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load YAML configuration
    with open(config_path, "r") as f:
        _config = yaml.safe_load(f)

    return _config


def get_config(key: Optional[str] = None, default: Any = None) -> Any:
    """
    Get configuration value(s).

    Args:
        key: Configuration key (supports dot notation, e.g., 'data.path')
             If None, returns entire config dictionary
        default: Default value if key not found

    Returns:
        Configuration value or entire dictionary if key is None
    """
    global _config

    if _config is None:
        _config = load_config()

    if key is None:
        return _config

    # Support dot notation for nested keys
    keys = key.split(".")
    value = _config

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value

