"""Main script to run Task 4: Predictive Modeling for Risk-Based Pricing."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.task4.task4_runner import Task4Runner
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Run Task 4 analysis."""
    logger.info("Starting Task 4: Predictive Modeling for Risk-Based Pricing")

    # Initialize runner
    runner = Task4Runner()

    # Run all analyses
    results = runner.run_all()

    logger.info("Task 4 analysis complete!")
    logger.info(f"Results saved to: {runner.task4_results_path}")
    logger.info(f"Reports saved to: {runner.task4_reports_path}")


if __name__ == "__main__":
    main()

