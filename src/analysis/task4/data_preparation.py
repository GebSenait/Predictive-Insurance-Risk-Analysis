"""Data preparation pipeline for Task 4 predictive modeling."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

from src.data.loaders import DataLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataPreprocessor:
    """Data preprocessing pipeline for predictive modeling."""

    def __init__(
        self,
        data_path: Optional[Path] = None,
        random_state: int = 42,
        test_size: float = 0.3,
    ):
        """
        Initialize DataPreprocessor.

        Args:
            data_path: Base path for data files
            random_state: Random seed for reproducibility
            test_size: Proportion of data for testing (default: 0.3)
        """
        self.data_path = data_path
        self.random_state = random_state
        self.test_size = test_size
        self.logger = logger
        self.data_loader = DataLoader(data_path)

        # Encoders and scalers (fitted during preprocessing)
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.onehot_encoders: Dict[str, OneHotEncoder] = {}
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []

    def load_data(self, filename: str = "MachineLearningRating_v3.txt") -> pd.DataFrame:
        """
        Load the insurance dataset.

        Args:
            filename: Name of the data file

        Returns:
            Loaded DataFrame
        """
        self.logger.info(f"Loading dataset: {filename}")
        df = self.data_loader.load_csv(filename, sep="|", low_memory=False)
        self.logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df

    def handle_missing_values(
        self, df: pd.DataFrame, strategy: str = "median"
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset.

        Args:
            df: Input DataFrame
            strategy: Strategy for filling missing values ('median', 'mean', 'mode', 'drop')

        Returns:
            DataFrame with missing values handled
        """
        self.logger.info("Handling missing values...")
        df = df.copy()

        # Count missing values
        missing_counts = df.isnull().sum()
        if missing_counts.sum() > 0:
            self.logger.info(f"Missing values found:\n{missing_counts[missing_counts > 0]}")

        # Handle missing values based on strategy
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if strategy == "drop":
                    df = df.dropna(subset=[col])
                elif strategy == "median" and df[col].dtype in ["int64", "float64"]:
                    df[col].fillna(df[col].median(), inplace=True)
                elif strategy == "mean" and df[col].dtype in ["int64", "float64"]:
                    df[col].fillna(df[col].mean(), inplace=True)
                elif strategy == "mode":
                    df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 0, inplace=True)
                else:
                    # For categorical or other types, use mode or 'Unknown'
                    if df[col].dtype == "object":
                        df[col].fillna("Unknown", inplace=True)
                    else:
                        df[col].fillna(0, inplace=True)

        self.logger.info("Missing values handled")
        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer new features from existing ones.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with engineered features
        """
        self.logger.info("Engineering features...")
        df = df.copy()

        # Claim-related features
        if "TotalClaims" in df.columns and "TotalPremium" in df.columns:
            # Claim indicator (binary)
            df["HasClaim"] = (df["TotalClaims"] > 0).astype(int)

            # Loss ratio
            df["LossRatio"] = np.where(
                df["TotalPremium"] > 0,
                df["TotalClaims"] / df["TotalPremium"],
                0,
            )

            # Claim severity (only for policies with claims)
            df["ClaimSeverity"] = np.where(
                df["HasClaim"] == 1, df["TotalClaims"], 0
            )

            # Profit margin
            df["ProfitMargin"] = df["TotalPremium"] - df["TotalClaims"]

        # Age-related features (if Age column exists)
        if "Age" in df.columns:
            # Age groups
            df["AgeGroup"] = pd.cut(
                df["Age"],
                bins=[0, 25, 35, 45, 55, 65, 100],
                labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"],
            )

        # Geographic features (if available)
        if "PostalCode" in df.columns:
            # Extract first few digits of postal code as region indicator
            df["PostalCodePrefix"] = df["PostalCode"].astype(str).str[:3]

        # Vehicle-related features (if available)
        vehicle_cols = [col for col in df.columns if "Vehicle" in col or "Auto" in col]
        if vehicle_cols:
            self.logger.info(f"Found vehicle-related columns: {vehicle_cols}")

        self.logger.info(f"Feature engineering complete. New shape: {df.shape}")
        return df

    def encode_categorical(
        self,
        df: pd.DataFrame,
        categorical_cols: Optional[List[str]] = None,
        encoding_method: str = "onehot",
    ) -> pd.DataFrame:
        """
        Encode categorical variables.

        Args:
            df: Input DataFrame
            categorical_cols: List of categorical column names (auto-detected if None)
            encoding_method: 'onehot' or 'label'

        Returns:
            DataFrame with encoded categorical variables
        """
        self.logger.info("Encoding categorical variables...")
        df = df.copy()

        # Auto-detect categorical columns if not provided
        if categorical_cols is None:
            categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

        # Remove target variables from categorical encoding
        target_vars = ["TotalClaims", "TotalPremium", "HasClaim", "ClaimSeverity"]
        categorical_cols = [col for col in categorical_cols if col not in target_vars]

        self.logger.info(f"Categorical columns to encode: {categorical_cols}")

        for col in categorical_cols:
            if col not in df.columns:
                continue

            if encoding_method == "label":
                # Label encoding
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    # Handle unseen categories
                    unique_values = set(df[col].astype(str).unique())
                    known_values = set(self.label_encoders[col].classes_)
                    for val in unique_values - known_values:
                        # Add to encoder
                        self.label_encoders[col].classes_ = np.append(
                            self.label_encoders[col].classes_, val
                        )
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))

            elif encoding_method == "onehot":
                # One-hot encoding with error handling
                try:
                    if col not in self.onehot_encoders:
                        self.onehot_encoders[col] = OneHotEncoder(
                            sparse_output=False, handle_unknown="ignore"
                        )
                        encoded = self.onehot_encoders[col].fit_transform(
                            df[[col]].astype(str)
                        )
                    else:
                        encoded = self.onehot_encoders[col].transform(
                            df[[col]].astype(str)
                        )

                    # Create column names
                    feature_names = [f"{col}_{cat}" for cat in self.onehot_encoders[col].categories_[0]]
                    
                    # Ensure encoded is a numpy array and convert to float if needed
                    if not isinstance(encoded, np.ndarray):
                        encoded = np.array(encoded)
                    encoded = encoded.astype(float)
                    
                    # Create DataFrame with proper index alignment
                    encoded_df = pd.DataFrame(
                        encoded, 
                        columns=feature_names, 
                        index=df.index
                    )

                    # Drop original column first
                    df = df.drop(columns=[col], errors="ignore")
                    
                    # Use assign method for safer concatenation (avoids numpy vstack issues)
                    for feat_col in feature_names:
                        df[feat_col] = encoded_df[feat_col]
                    
                except Exception as e:
                    self.logger.warning(
                        f"Error encoding column {col} with one-hot: {e}. "
                        f"Using label encoding instead."
                    )
                    # Fallback to label encoding
                    if col not in self.label_encoders:
                        self.label_encoders[col] = LabelEncoder()
                        df[col] = self.label_encoders[col].fit_transform(
                            df[col].astype(str).fillna("Unknown")
                        )
                    else:
                        unique_values = set(df[col].astype(str).fillna("Unknown").unique())
                        known_values = set(self.label_encoders[col].classes_)
                        for val in unique_values - known_values:
                            self.label_encoders[col].classes_ = np.append(
                                self.label_encoders[col].classes_, val
                            )
                        df[col] = self.label_encoders[col].transform(
                            df[col].astype(str).fillna("Unknown")
                        )

        self.logger.info("Categorical encoding complete")
        return df

    def prepare_severity_data(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
        """
        Prepare data for claim severity modeling (only policies with claims).

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (features, target, feature_names)
        """
        self.logger.info("Preparing data for severity modeling...")

        # Filter to only policies with claims
        severity_df = df[df["TotalClaims"] > 0].copy()
        self.logger.info(f"Severity dataset: {len(severity_df)} policies with claims")

        # Target variable
        target = severity_df["TotalClaims"].copy()

        # Features (exclude target variables)
        exclude_cols = [
            "TotalClaims",
            "TotalPremium",
            "HasClaim",
            "LossRatio",
            "ClaimSeverity",
            "ProfitMargin",
        ]
        feature_cols = [col for col in severity_df.columns if col not in exclude_cols]

        # Select only numeric features for severity model
        numeric_features = severity_df[feature_cols].select_dtypes(
            include=[np.number]
        ).columns.tolist()

        features = severity_df[numeric_features].copy()

        self.logger.info(f"Severity model: {len(features.columns)} features, {len(features)} samples")
        return features, target, numeric_features

    def prepare_premium_data(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
        """
        Prepare data for premium optimization modeling.

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (features, target, feature_names)
        """
        self.logger.info("Preparing data for premium modeling...")

        # Target variable
        target = df["TotalPremium"].copy()

        # Features (exclude target variables)
        exclude_cols = [
            "TotalClaims",
            "TotalPremium",
            "HasClaim",
            "LossRatio",
            "ClaimSeverity",
            "ProfitMargin",
        ]
        feature_cols = [col for col in df.columns if col not in exclude_cols]

        # Select only numeric features
        numeric_features = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()

        features = df[numeric_features].copy()

        self.logger.info(f"Premium model: {len(features.columns)} features, {len(features)} samples")
        return features, target, numeric_features

    def prepare_claim_probability_data(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
        """
        Prepare data for claim probability classification.

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (features, target, feature_names)
        """
        self.logger.info("Preparing data for claim probability modeling...")

        # Create binary target (1 if claim, 0 if no claim)
        if "HasClaim" not in df.columns:
            target = (df["TotalClaims"] > 0).astype(int)
        else:
            target = df["HasClaim"].copy()

        # Features (exclude target variables)
        exclude_cols = [
            "TotalClaims",
            "TotalPremium",
            "HasClaim",
            "LossRatio",
            "ClaimSeverity",
            "ProfitMargin",
        ]
        feature_cols = [col for col in df.columns if col not in exclude_cols]

        # Select only numeric features
        numeric_features = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()

        features = df[numeric_features].copy()

        self.logger.info(
            f"Claim probability model: {len(features.columns)} features, {len(features)} samples"
        )
        self.logger.info(f"Claim rate: {target.mean():.2%}")

        return features, target, numeric_features

    def split_data(
        self, X: pd.DataFrame, y: pd.Series
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split data into train and test sets.

        Args:
            X: Features
            y: Target variable

        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        self.logger.info(f"Splitting data: {1-self.test_size:.0%} train, {self.test_size:.0%} test")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=None
        )
        self.logger.info(f"Train: {len(X_train)} samples, Test: {len(X_test)} samples")
        return X_train, X_test, y_train, y_test

    def scale_features(
        self, X_train: pd.DataFrame, X_test: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Scale features using StandardScaler.

        Args:
            X_train: Training features
            X_test: Test features

        Returns:
            Tuple of (scaled_X_train, scaled_X_test)
        """
        self.logger.info("Scaling features...")
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index,
        )
        X_test_scaled = pd.DataFrame(
            self.scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index,
        )
        self.logger.info("Feature scaling complete")
        return X_train_scaled, X_test_scaled

    def full_pipeline(
        self,
        filename: str = "MachineLearningRating_v3.txt",
        handle_missing: bool = True,
        engineer_features: bool = True,
        encode_categorical: bool = True,
        encoding_method: str = "onehot",
    ) -> Dict[str, Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]:
        """
        Run full data preparation pipeline.

        Args:
            filename: Name of the data file
            handle_missing: Whether to handle missing values
            engineer_features: Whether to engineer new features
            encode_categorical: Whether to encode categorical variables
            encoding_method: 'onehot' or 'label'

        Returns:
            Dictionary with prepared datasets for each model type
        """
        self.logger.info("=" * 80)
        self.logger.info("Starting full data preparation pipeline")
        self.logger.info("=" * 80)

        # Load data
        df = self.load_data(filename)

        # Handle missing values
        if handle_missing:
            df = self.handle_missing_values(df)

        # Engineer features
        if engineer_features:
            df = self.engineer_features(df)

        # Encode categorical variables
        if encode_categorical:
            df = self.encode_categorical(df, encoding_method=encoding_method)

        # Prepare datasets for each model
        datasets = {}

        # 1. Severity model
        X_sev, y_sev, feature_names_sev = self.prepare_severity_data(df)
        X_sev_train, X_sev_test, y_sev_train, y_sev_test = self.split_data(X_sev, y_sev)
        datasets["severity"] = (X_sev_train, X_sev_test, y_sev_train, y_sev_test)
        self.feature_names = feature_names_sev

        # 2. Premium model
        X_prem, y_prem, feature_names_prem = self.prepare_premium_data(df)
        X_prem_train, X_prem_test, y_prem_train, y_prem_test = self.split_data(X_prem, y_prem)
        datasets["premium"] = (X_prem_train, X_prem_test, y_prem_train, y_prem_test)

        # 3. Claim probability model
        X_prob, y_prob, feature_names_prob = self.prepare_claim_probability_data(df)
        X_prob_train, X_prob_test, y_prob_train, y_prob_test = self.split_data(X_prob, y_prob)
        datasets["claim_probability"] = (
            X_prob_train,
            X_prob_test,
            y_prob_train,
            y_prob_test,
        )

        self.logger.info("=" * 80)
        self.logger.info("Data preparation pipeline complete")
        self.logger.info("=" * 80)

        return datasets

