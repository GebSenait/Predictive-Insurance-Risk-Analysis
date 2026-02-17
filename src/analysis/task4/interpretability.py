"""Model interpretability using SHAP and LIME for Task 4."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    import shap

    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

try:
    from lime import lime_tabular

    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ModelInterpreter:
    """Interpret models using SHAP and LIME."""

    def __init__(self, output_path: Optional[Path] = None):
        """
        Initialize ModelInterpreter.

        Args:
            output_path: Path to save interpretability results
        """
        self.output_path = output_path or Path("results/task4")
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.logger = logger

    def shap_analysis(
        self,
        model,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        feature_names: List[str],
        model_name: str,
        task_type: str = "regression",
        max_samples: int = 100,
    ) -> Dict:
        """
        Perform SHAP analysis on a model.

        Args:
            model: Trained model
            X_train: Training features
            X_test: Test features
            feature_names: List of feature names
            model_name: Name of the model
            task_type: 'regression' or 'classification'
            max_samples: Maximum number of samples for SHAP (for performance)

        Returns:
            Dictionary with SHAP values and feature importance
        """
        if not SHAP_AVAILABLE:
            self.logger.warning("SHAP not available. Skipping SHAP analysis.")
            return None

        self.logger.info(f"Performing SHAP analysis for {model_name}...")

        try:
            # Limit samples for performance
            if len(X_test) > max_samples:
                X_test_sample = X_test.sample(n=max_samples, random_state=42)
            else:
                X_test_sample = X_test

            # Create SHAP explainer
            # Use TreeExplainer for tree-based models, otherwise KernelExplainer
            model_type = type(model).__name__.lower()
            if (
                "tree" in model_type
                or "forest" in model_type
                or "xgb" in model_type
                or "gradient" in model_type
            ):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_test_sample)
            else:
                # For linear models, use LinearExplainer if available
                try:
                    explainer = shap.LinearExplainer(model, X_train)
                    shap_values = explainer.shap_values(X_test_sample)
                except:
                    # Fallback to KernelExplainer (slower)
                    self.logger.info("Using KernelExplainer (this may take a while)...")
                    explainer = shap.KernelExplainer(
                        model.predict,
                        X_train.sample(n=min(100, len(X_train)), random_state=42),
                    )
                    shap_values = explainer.shap_values(X_test_sample)

            # Handle multi-output (classification)
            if isinstance(shap_values, list):
                shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

            # Calculate feature importance (mean absolute SHAP values)
            if len(shap_values.shape) > 2:
                shap_values = shap_values.reshape(shap_values.shape[0], -1)

            feature_importance = pd.DataFrame(
                {
                    "feature": feature_names[: shap_values.shape[1]],
                    "importance": np.abs(shap_values).mean(axis=0),
                }
            ).sort_values("importance", ascending=False)

            # Get top features
            top_features = feature_importance.head(10).to_dict("records")

            results = {
                "shap_values": shap_values,
                "explainer": explainer,
                "feature_importance": feature_importance,
                "top_features": top_features,
                "X_test_sample": X_test_sample,
            }

            self.logger.info(
                f"SHAP analysis complete. Top feature: {top_features[0]['feature']}"
            )
            return results

        except Exception as e:
            self.logger.error(f"Error in SHAP analysis: {e}")
            return None

    def lime_analysis(
        self,
        model,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        feature_names: List[str],
        model_name: str,
        task_type: str = "regression",
        num_samples: int = 5,
    ) -> Dict:
        """
        Perform LIME analysis on a model.

        Args:
            model: Trained model
            X_train: Training features
            X_test: Test features
            feature_names: List of feature names
            model_name: Name of the model
            task_type: 'regression' or 'classification'
            num_samples: Number of samples to explain

        Returns:
            Dictionary with LIME explanations
        """
        if not LIME_AVAILABLE:
            self.logger.warning("LIME not available. Skipping LIME analysis.")
            return None

        self.logger.info(f"Performing LIME analysis for {model_name}...")

        try:
            # Create LIME explainer
            mode = "regression" if task_type == "regression" else "classification"
            explainer = lime_tabular.LimeTabularExplainer(
                X_train.values,
                feature_names=feature_names,
                mode=mode,
                random_state=42,
            )

            # Explain a few samples
            explanations = []
            sample_indices = np.random.choice(
                len(X_test), size=min(num_samples, len(X_test)), replace=False
            )

            for idx in sample_indices:
                explanation = explainer.explain_instance(
                    X_test.iloc[idx].values,
                    model.predict,
                    num_features=10,
                )
                explanations.append(
                    {
                        "index": idx,
                        "explanation": explanation,
                        "feature_importance": explanation.as_list(),
                    }
                )

            # Aggregate feature importance across samples
            all_features = {}
            for exp in explanations:
                for feature, importance in exp["feature_importance"]:
                    if feature not in all_features:
                        all_features[feature] = []
                    all_features[feature].append(abs(importance))

            # Average importance per feature
            avg_importance = {
                feat: np.mean(imps) for feat, imps in all_features.items()
            }
            feature_importance = pd.DataFrame(
                {
                    "feature": list(avg_importance.keys()),
                    "importance": list(avg_importance.values()),
                }
            ).sort_values("importance", ascending=False)

            results = {
                "explanations": explanations,
                "feature_importance": feature_importance,
                "top_features": feature_importance.head(10).to_dict("records"),
            }

            self.logger.info("LIME analysis complete")
            return results

        except Exception as e:
            self.logger.error(f"Error in LIME analysis: {e}")
            return None

    def get_top_features(
        self,
        shap_results: Optional[Dict],
        lime_results: Optional[Dict],
        top_n: int = 10,
    ) -> List[Dict]:
        """
        Get top features from SHAP and/or LIME analysis.

        Args:
            shap_results: Results from SHAP analysis
            lime_results: Results from LIME analysis
            top_n: Number of top features to return

        Returns:
            List of top features with importance scores
        """
        features_dict = {}

        # Add SHAP features
        if shap_results and "top_features" in shap_results:
            for feat in shap_results["top_features"]:
                feat_name = feat["feature"]
                if feat_name not in features_dict:
                    features_dict[feat_name] = {
                        "shap_importance": 0,
                        "lime_importance": 0,
                    }
                features_dict[feat_name]["shap_importance"] = feat["importance"]

        # Add LIME features
        if lime_results and "top_features" in lime_results:
            for feat in lime_results["top_features"]:
                feat_name = feat["feature"]
                if feat_name not in features_dict:
                    features_dict[feat_name] = {
                        "shap_importance": 0,
                        "lime_importance": 0,
                    }
                features_dict[feat_name]["lime_importance"] = feat["importance"]

        # Combine and rank
        top_features = []
        for feat_name, importances in features_dict.items():
            # Average importance if both available, otherwise use available one
            if (
                importances["shap_importance"] > 0
                and importances["lime_importance"] > 0
            ):
                avg_importance = (
                    importances["shap_importance"] + importances["lime_importance"]
                ) / 2
            elif importances["shap_importance"] > 0:
                avg_importance = importances["shap_importance"]
            else:
                avg_importance = importances["lime_importance"]

            top_features.append(
                {
                    "feature": feat_name,
                    "shap_importance": importances["shap_importance"],
                    "lime_importance": importances["lime_importance"],
                    "combined_importance": avg_importance,
                }
            )

        # Sort by combined importance
        top_features.sort(key=lambda x: x["combined_importance"], reverse=True)
        return top_features[:top_n]

    def interpret_model(
        self,
        model,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        feature_names: List[str],
        model_name: str,
        task_type: str = "regression",
    ) -> Dict:
        """
        Perform full interpretability analysis (SHAP + LIME).

        Args:
            model: Trained model
            X_train: Training features
            X_test: Test features
            feature_names: List of feature names
            model_name: Name of the model
            task_type: 'regression' or 'classification'

        Returns:
            Dictionary with all interpretability results
        """
        self.logger.info(f"Interpreting model: {model_name}")

        results = {
            "model_name": model_name,
            "task_type": task_type,
            "shap_results": None,
            "lime_results": None,
            "top_features": [],
        }

        # SHAP analysis
        if SHAP_AVAILABLE:
            shap_results = self.shap_analysis(
                model, X_train, X_test, feature_names, model_name, task_type
            )
            results["shap_results"] = shap_results

        # LIME analysis
        if LIME_AVAILABLE:
            lime_results = self.lime_analysis(
                model, X_train, X_test, feature_names, model_name, task_type
            )
            results["lime_results"] = lime_results

        # Get top features
        results["top_features"] = self.get_top_features(
            results["shap_results"], results["lime_results"]
        )

        return results
