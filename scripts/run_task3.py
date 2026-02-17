"""Main script to run Task 3: Statistical Validation of Risk Drivers."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.task3.hypothesis_testing import HypothesisTestingRunner
from src.analysis.task3.reporting import ReportGenerator
from src.analysis.task3.visualizations import VisualizationGenerator
from src.utils.config import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Run Task 3 analysis."""
    logger.info("Starting Task 3: Statistical Validation of Risk Drivers")

    # Load configuration
    config = load_config()

    # Initialize runner
    runner = HypothesisTestingRunner()

    # Run all hypothesis tests
    results = runner.run_all_tests()

    # Save results
    runner.save_results(results, filename="task3_results.json")

    # Generate visualizations
    logger.info("Generating visualizations...")
    viz_gen = VisualizationGenerator(runner.figures_path)
    viz_gen.plot_summary_statistics(results, filename="hypothesis_test_summary.png")

    # Generate report
    logger.info("Generating report...")
    report_gen = ReportGenerator(runner.reports_path)
    report_gen.generate_markdown_report(results, filename="task3_statistical_report.md")
    report_gen.save_results_table(results, filename="task3_results_table.csv")

    logger.info("Task 3 analysis complete!")
    logger.info(f"Results saved to: {runner.results_path}")
    logger.info(f"Reports saved to: {runner.reports_path}")
    logger.info(f"Visualizations saved to: {runner.figures_path}")


if __name__ == "__main__":
    main()
