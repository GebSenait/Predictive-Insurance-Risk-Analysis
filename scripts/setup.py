"""Setup script for initializing project directories and environment."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_config


def create_directories():
    """Create necessary project directories."""
    try:
        config = load_config()
    except FileNotFoundError:
        print("Warning: config.yaml not found. Creating default directories.")
        config = {
            "data": {
                "raw_path": "data/raw",
                "processed_path": "data/processed",
                "external_path": "data/external",
            },
            "output": {
                "results_path": "results",
                "figures_path": "results/figures",
                "reports_path": "results/reports",
            },
            "logging": {"log_file": "logs/application.log"},
        }

    directories = [
        Path(config["data"]["raw_path"]),
        Path(config["data"]["processed_path"]),
        Path(config["data"]["external_path"]),
        Path(config["output"]["results_path"]),
        Path(config["output"]["figures_path"]),
        Path(config["output"]["reports_path"]),
        Path(config["logging"]["log_file"]).parent,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        # Create .gitkeep file
        (directory / ".gitkeep").touch(exist_ok=True)
        print(f"Created directory: {directory}")


if __name__ == "__main__":
    create_directories()
    print("Project directories initialized successfully!")

