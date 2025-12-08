"""Main runner for Task 4: Predictive Modeling."""

from pathlib import Path
from typing import Dict

from src.analysis.task4.data_preparation import DataPreprocessor
from src.analysis.task4.interpretability import ModelInterpreter
from src.analysis.task4.models import ModelTrainer
from src.analysis.task4.reporting import ReportGenerator
from src.utils.config import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Task4Runner:
    """Main runner for Task 4 predictive modeling."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize Task4Runner.

        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.logger = logger

        # Setup paths
        self.results_path = Path(self.config.get("output", {}).get("results_path", "results"))
        self.figures_path = Path(self.config.get("output", {}).get("figures_path", "results/figures"))
        self.reports_path = Path(self.config.get("output", {}).get("reports_path", "results/reports"))
        
        # Create task4 subdirectories
        self.task4_results_path = self.results_path / "task4"
        self.task4_figures_path = self.figures_path / "task4"
        self.task4_reports_path = self.reports_path
        
        self.task4_results_path.mkdir(parents=True, exist_ok=True)
        self.task4_figures_path.mkdir(parents=True, exist_ok=True)
        self.task4_reports_path.mkdir(parents=True, exist_ok=True)

        # Get task4 config
        self.task4_config = self.config.get("analysis", {}).get("task4", {})
        self.random_state = self.task4_config.get("random_state", 42)
        self.test_size = self.task4_config.get("test_size", 0.3)

        # Initialize components
        self.data_preprocessor = DataPreprocessor(
            data_path=Path(self.config.get("data", {}).get("raw_path", "data/raw")),
            random_state=self.random_state,
            test_size=self.test_size,
        )
        self.model_trainer = ModelTrainer(random_state=self.random_state)
        self.interpreter = ModelInterpreter(output_path=self.task4_results_path)
        self.report_generator = ReportGenerator(output_path=self.task4_reports_path)

    def run_severity_modeling(self, datasets: Dict) -> Dict:
        """
        Run claim severity modeling.

        Args:
            datasets: Dictionary with prepared datasets

        Returns:
            Dictionary with severity model results
        """
        self.logger.info("=" * 80)
        self.logger.info("CLAIM SEVERITY MODELING")
        self.logger.info("=" * 80)

        X_train, X_test, y_train, y_test = datasets["severity"]

        # Train all regression models
        model_results = self.model_trainer.train_all_regression_models(
            X_train, y_train, X_test, y_test
        )

        # Get best model
        best_model_name, best_model_results = self.model_trainer.get_best_model(
            model_results, metric="test_r2"
        )

        return {
            "model_results": model_results,
            "best_model_name": best_model_name,
            "best_model": best_model_results,
            "X_train": X_train,
            "X_test": X_test,
            "y_test": y_test,
            "feature_names": list(X_train.columns),
        }

    def run_premium_modeling(self, datasets: Dict) -> Dict:
        """
        Run premium optimization modeling.

        Args:
            datasets: Dictionary with prepared datasets

        Returns:
            Dictionary with premium model results
        """
        self.logger.info("=" * 80)
        self.logger.info("PREMIUM OPTIMIZATION MODELING")
        self.logger.info("=" * 80)

        X_train, X_test, y_train, y_test = datasets["premium"]

        # Train all regression models
        model_results = self.model_trainer.train_all_regression_models(
            X_train, y_train, X_test, y_test
        )

        # Get best model
        best_model_name, best_model_results = self.model_trainer.get_best_model(
            model_results, metric="test_r2"
        )

        return {
            "model_results": model_results,
            "best_model_name": best_model_name,
            "best_model": best_model_results,
            "X_train": X_train,
            "X_test": X_test,
            "y_test": y_test,
            "feature_names": list(X_train.columns),
        }

    def run_claim_probability_modeling(self, datasets: Dict) -> Dict:
        """
        Run claim probability classification modeling.

        Args:
            datasets: Dictionary with prepared datasets

        Returns:
            Dictionary with claim probability model results
        """
        self.logger.info("=" * 80)
        self.logger.info("CLAIM PROBABILITY MODELING")
        self.logger.info("=" * 80)

        X_train, X_test, y_train, y_test = datasets["claim_probability"]

        # Train all classification models
        model_results = self.model_trainer.train_all_classification_models(
            X_train, y_train, X_test, y_test
        )

        # Get best model
        best_model_name, best_model_results = self.model_trainer.get_best_model(
            model_results, metric="test_f1"
        )

        return {
            "model_results": model_results,
            "best_model_name": best_model_name,
            "best_model": best_model_results,
            "X_train": X_train,
            "X_test": X_test,
            "y_test": y_test,
            "feature_names": list(X_train.columns),
        }

    def run_interpretability_analysis(self, all_results: Dict) -> Dict:
        """
        Run interpretability analysis on best models.

        Args:
            all_results: Dictionary with all model results

        Returns:
            Dictionary with interpretability results
        """
        self.logger.info("=" * 80)
        self.logger.info("MODEL INTERPRETABILITY ANALYSIS")
        self.logger.info("=" * 80)

        interpretability_results = {}

        # Analyze each model type
        for task_name in ["severity", "premium", "claim_probability"]:
            if task_name not in all_results:
                continue

            task_results = all_results[task_name]
            if "best_model" not in task_results or task_results["best_model"] is None:
                continue

            best_model = task_results["best_model"]["model"]
            model_name = task_results["best_model"]["model_name"]
            X_train = task_results["X_train"]
            X_test = task_results["X_test"]
            feature_names = task_results["feature_names"]
            task_type = "regression" if task_name != "claim_probability" else "classification"

            # Run interpretability
            interp_results = self.interpreter.interpret_model(
                best_model,
                X_train,
                X_test,
                feature_names,
                model_name,
                task_type,
            )

            interpretability_results[task_name] = interp_results

        return interpretability_results

    def save_results(self, all_results: Dict, filename: str = "task4_results.json") -> None:
        """
        Save all results to JSON.

        Args:
            all_results: Dictionary with all results
            filename: Output filename
        """
        self.logger.info(f"Saving results to: {filename}")

        # Convert results to JSON-serializable format
        serializable_results = {}
        for key, value in all_results.items():
            if key == "interpretability":
                # Skip complex objects in interpretability
                serializable_results[key] = {
                    model_name: {
                        "top_features": results.get("top_features", [])
                        for model_name, results in value.items()
                    }
                }
            else:
                # Extract metrics from model results
                serializable_results[key] = {
                    "best_model_name": value.get("best_model_name"),
                    "best_model_metrics": {
                        k: v
                        for k, v in value.get("best_model", {}).items()
                        if k not in ["model", "y_test_pred"]
                    },
                    "all_models": {
                        model_name: {
                            k: v
                            for k, v in model_results.items()
                            if k not in ["model", "y_test_pred"]
                        }
                        for model_name, model_results in value.get("model_results", {}).items()
                    },
                }

        results_path = self.task4_results_path / filename
        import json
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(serializable_results, f, indent=2, default=str)

        self.logger.info(f"Results saved to: {results_path}")

    def run_all(self) -> Dict:
        """
        Run complete Task 4 analysis pipeline.

        Returns:
            Dictionary with all results
        """
        self.logger.info("=" * 80)
        self.logger.info("TASK 4: PREDICTIVE MODELING FOR RISK-BASED PRICING")
        self.logger.info("=" * 80)

        # Step 1: Data preparation
        self.logger.info("\n" + "=" * 80)
        self.logger.info("STEP 1: DATA PREPARATION")
        self.logger.info("=" * 80)
        datasets = self.data_preprocessor.full_pipeline()

        # Step 2: Model training
        self.logger.info("\n" + "=" * 80)
        self.logger.info("STEP 2: MODEL TRAINING")
        self.logger.info("=" * 80)

        all_results = {}
        all_results["severity"] = self.run_severity_modeling(datasets)
        all_results["premium"] = self.run_premium_modeling(datasets)
        all_results["claim_probability"] = self.run_claim_probability_modeling(datasets)

        # Step 3: Interpretability
        self.logger.info("\n" + "=" * 80)
        self.logger.info("STEP 3: MODEL INTERPRETABILITY")
        self.logger.info("=" * 80)
        all_results["interpretability"] = self.run_interpretability_analysis(all_results)

        # Step 4: Reporting
        self.logger.info("\n" + "=" * 80)
        self.logger.info("STEP 4: REPORTING")
        self.logger.info("=" * 80)

        # Save results
        self.save_results(all_results)

        # Generate reports
        self.report_generator.generate_markdown_report(all_results)
        self.report_generator.save_results_table(all_results)
        self.report_generator.save_interpretability_summary(all_results["interpretability"])

        self.logger.info("=" * 80)
        self.logger.info("TASK 4 COMPLETE!")
        self.logger.info("=" * 80)
        self.logger.info(f"Results saved to: {self.task4_results_path}")
        self.logger.info(f"Reports saved to: {self.task4_reports_path}")

        return all_results

