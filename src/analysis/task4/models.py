"""Model training and evaluation for Task 4 predictive modeling."""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

try:
    import xgboost as xgb

    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelTrainer:
    """Train and evaluate predictive models."""

    def __init__(self, random_state: int = 42):
        """
        Initialize ModelTrainer.

        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.logger = logger
        self.models: Dict[str, Dict] = {}

    def train_linear_regression(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> Dict:
        """
        Train and evaluate Linear Regression model.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary with model and evaluation metrics
        """
        self.logger.info("Training Linear Regression...")
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        # Metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)

        results = {
            "model": model,
            "model_name": "Linear Regression",
            "train_rmse": train_rmse,
            "test_rmse": test_rmse,
            "train_r2": train_r2,
            "test_r2": test_r2,
            "y_test_pred": y_test_pred,
        }

        self.logger.info(
            f"Linear Regression - Test RMSE: {test_rmse:.2f}, Test R²: {test_r2:.4f}"
        )
        return results

    def train_decision_tree(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        task_type: str = "regression",
        max_depth: Optional[int] = 10,
    ) -> Dict:
        """
        Train and evaluate Decision Tree model.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            task_type: 'regression' or 'classification'
            max_depth: Maximum depth of the tree

        Returns:
            Dictionary with model and evaluation metrics
        """
        self.logger.info(f"Training Decision Tree ({task_type})...")

        if task_type == "regression":
            model = DecisionTreeRegressor(
                max_depth=max_depth, random_state=self.random_state
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)

            results = {
                "model": model,
                "model_name": "Decision Tree",
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_r2": train_r2,
                "test_r2": test_r2,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"Decision Tree - Test RMSE: {test_rmse:.2f}, Test R²: {test_r2:.4f}"
            )

        else:  # classification
            model = DecisionTreeClassifier(
                max_depth=max_depth, random_state=self.random_state
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, y_train_pred)
            test_acc = accuracy_score(y_test, y_test_pred)
            test_precision = precision_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_recall = recall_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_f1 = f1_score(y_test, y_test_pred, average="binary", zero_division=0)

            results = {
                "model": model,
                "model_name": "Decision Tree",
                "train_accuracy": train_acc,
                "test_accuracy": test_acc,
                "test_precision": test_precision,
                "test_recall": test_recall,
                "test_f1": test_f1,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"Decision Tree - Test Accuracy: {test_acc:.4f}, Test F1: {test_f1:.4f}"
            )

        return results

    def train_random_forest(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        task_type: str = "regression",
        n_estimators: int = 100,
        max_depth: Optional[int] = 10,
    ) -> Dict:
        """
        Train and evaluate Random Forest model.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            task_type: 'regression' or 'classification'
            n_estimators: Number of trees
            max_depth: Maximum depth of trees

        Returns:
            Dictionary with model and evaluation metrics
        """
        self.logger.info(f"Training Random Forest ({task_type})...")

        if task_type == "regression":
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=self.random_state,
                n_jobs=-1,
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)

            results = {
                "model": model,
                "model_name": "Random Forest",
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_r2": train_r2,
                "test_r2": test_r2,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"Random Forest - Test RMSE: {test_rmse:.2f}, Test R²: {test_r2:.4f}"
            )

        else:  # classification
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=self.random_state,
                n_jobs=-1,
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, y_train_pred)
            test_acc = accuracy_score(y_test, y_test_pred)
            test_precision = precision_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_recall = recall_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_f1 = f1_score(y_test, y_test_pred, average="binary", zero_division=0)

            results = {
                "model": model,
                "model_name": "Random Forest",
                "train_accuracy": train_acc,
                "test_accuracy": test_acc,
                "test_precision": test_precision,
                "test_recall": test_recall,
                "test_f1": test_f1,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"Random Forest - Test Accuracy: {test_acc:.4f}, Test F1: {test_f1:.4f}"
            )

        return results

    def train_gradient_boosting(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        task_type: str = "regression",
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 5,
    ) -> Dict:
        """
        Train and evaluate Gradient Boosting model.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            task_type: 'regression' or 'classification'
            n_estimators: Number of boosting stages
            learning_rate: Learning rate
            max_depth: Maximum depth of trees

        Returns:
            Dictionary with model and evaluation metrics
        """
        self.logger.info(f"Training Gradient Boosting ({task_type})...")

        if task_type == "regression":
            model = GradientBoostingRegressor(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=self.random_state,
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)

            results = {
                "model": model,
                "model_name": "Gradient Boosting",
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_r2": train_r2,
                "test_r2": test_r2,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"Gradient Boosting - Test RMSE: {test_rmse:.2f}, Test R²: {test_r2:.4f}"
            )

        else:  # classification
            from sklearn.ensemble import GradientBoostingClassifier

            model = GradientBoostingClassifier(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=self.random_state,
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, y_train_pred)
            test_acc = accuracy_score(y_test, y_test_pred)
            test_precision = precision_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_recall = recall_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_f1 = f1_score(y_test, y_test_pred, average="binary", zero_division=0)

            results = {
                "model": model,
                "model_name": "Gradient Boosting",
                "train_accuracy": train_acc,
                "test_accuracy": test_acc,
                "test_precision": test_precision,
                "test_recall": test_recall,
                "test_f1": test_f1,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"Gradient Boosting - Test Accuracy: {test_acc:.4f}, Test F1: {test_f1:.4f}"
            )

        return results

    def train_xgboost(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        task_type: str = "regression",
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 5,
    ) -> Dict:
        """
        Train and evaluate XGBoost model.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            task_type: 'regression' or 'classification'
            n_estimators: Number of boosting rounds
            learning_rate: Learning rate
            max_depth: Maximum depth of trees

        Returns:
            Dictionary with model and evaluation metrics
        """
        if not XGBOOST_AVAILABLE:
            self.logger.warning("XGBoost not available. Skipping XGBoost model.")
            return None

        self.logger.info(f"Training XGBoost ({task_type})...")

        if task_type == "regression":
            model = xgb.XGBRegressor(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=self.random_state,
                n_jobs=-1,
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)

            results = {
                "model": model,
                "model_name": "XGBoost",
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_r2": train_r2,
                "test_r2": test_r2,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"XGBoost - Test RMSE: {test_rmse:.2f}, Test R²: {test_r2:.4f}"
            )

        else:  # classification
            model = xgb.XGBClassifier(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=self.random_state,
                n_jobs=-1,
            )
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, y_train_pred)
            test_acc = accuracy_score(y_test, y_test_pred)
            test_precision = precision_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_recall = recall_score(
                y_test, y_test_pred, average="binary", zero_division=0
            )
            test_f1 = f1_score(y_test, y_test_pred, average="binary", zero_division=0)

            results = {
                "model": model,
                "model_name": "XGBoost",
                "train_accuracy": train_acc,
                "test_accuracy": test_acc,
                "test_precision": test_precision,
                "test_recall": test_recall,
                "test_f1": test_f1,
                "y_test_pred": y_test_pred,
            }
            self.logger.info(
                f"XGBoost - Test Accuracy: {test_acc:.4f}, Test F1: {test_f1:.4f}"
            )

        return results

    def train_logistic_regression(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> Dict:
        """
        Train and evaluate Logistic Regression model for classification.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary with model and evaluation metrics
        """
        self.logger.info("Training Logistic Regression...")
        model = LogisticRegression(
            random_state=self.random_state, max_iter=1000, n_jobs=-1
        )
        model.fit(X_train, y_train)

        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_precision = precision_score(
            y_test, y_test_pred, average="binary", zero_division=0
        )
        test_recall = recall_score(
            y_test, y_test_pred, average="binary", zero_division=0
        )
        test_f1 = f1_score(y_test, y_test_pred, average="binary", zero_division=0)

        results = {
            "model": model,
            "model_name": "Logistic Regression",
            "train_accuracy": train_acc,
            "test_accuracy": test_acc,
            "test_precision": test_precision,
            "test_recall": test_recall,
            "test_f1": test_f1,
            "y_test_pred": y_test_pred,
        }

        self.logger.info(
            f"Logistic Regression - Test Accuracy: {test_acc:.4f}, Test F1: {test_f1:.4f}"
        )
        return results

    def train_all_regression_models(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> Dict[str, Dict]:
        """
        Train all regression models and return results.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary with all model results
        """
        self.logger.info("=" * 80)
        self.logger.info("Training all regression models")
        self.logger.info("=" * 80)

        results = {}

        # Linear Regression
        results["linear"] = self.train_linear_regression(
            X_train, y_train, X_test, y_test
        )

        # Decision Tree
        results["decision_tree"] = self.train_decision_tree(
            X_train, y_train, X_test, y_test, task_type="regression"
        )

        # Random Forest
        results["random_forest"] = self.train_random_forest(
            X_train, y_train, X_test, y_test, task_type="regression"
        )

        # Gradient Boosting
        results["gradient_boosting"] = self.train_gradient_boosting(
            X_train, y_train, X_test, y_test, task_type="regression"
        )

        # XGBoost
        if XGBOOST_AVAILABLE:
            xgb_result = self.train_xgboost(
                X_train, y_train, X_test, y_test, task_type="regression"
            )
            if xgb_result:
                results["xgboost"] = xgb_result

        return results

    def train_all_classification_models(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> Dict[str, Dict]:
        """
        Train all classification models and return results.

        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary with all model results
        """
        self.logger.info("=" * 80)
        self.logger.info("Training all classification models")
        self.logger.info("=" * 80)

        results = {}

        # Logistic Regression
        results["logistic"] = self.train_logistic_regression(
            X_train, y_train, X_test, y_test
        )

        # Decision Tree
        results["decision_tree"] = self.train_decision_tree(
            X_train, y_train, X_test, y_test, task_type="classification"
        )

        # Random Forest
        results["random_forest"] = self.train_random_forest(
            X_train, y_train, X_test, y_test, task_type="classification"
        )

        # Gradient Boosting
        results["gradient_boosting"] = self.train_gradient_boosting(
            X_train, y_train, X_test, y_test, task_type="classification"
        )

        # XGBoost
        if XGBOOST_AVAILABLE:
            xgb_result = self.train_xgboost(
                X_train, y_train, X_test, y_test, task_type="classification"
            )
            if xgb_result:
                results["xgboost"] = xgb_result

        return results

    def get_best_model(
        self, results: Dict[str, Dict], metric: str = "test_r2"
    ) -> Tuple[str, Dict]:
        """
        Get the best model based on a metric.

        Args:
            results: Dictionary of model results
            metric: Metric to use for comparison ('test_r2', 'test_rmse', 'test_f1', etc.)

        Returns:
            Tuple of (best_model_name, best_model_results)
        """
        best_model_name = None
        best_score = None

        for model_name, model_results in results.items():
            if metric in model_results:
                score = model_results[metric]
                if best_score is None:
                    best_score = score
                    best_model_name = model_name
                elif metric in ["test_r2", "test_accuracy", "test_f1"]:
                    # Higher is better
                    if score > best_score:
                        best_score = score
                        best_model_name = model_name
                else:  # Lower is better (RMSE)
                    if score < best_score:
                        best_score = score
                        best_model_name = model_name

        if best_model_name:
            self.logger.info(
                f"Best model: {best_model_name} ({metric}={best_score:.4f})"
            )
            return best_model_name, results[best_model_name]
        else:
            self.logger.warning(
                f"Could not determine best model using metric: {metric}"
            )
            return None, None
