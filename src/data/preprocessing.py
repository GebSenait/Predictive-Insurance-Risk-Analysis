"""Data preprocessing pipeline for insurance risk analysis.

Handles missing values, feature engineering, encoding, and train-test splitting.
Designed for production use with the DVC-tracked dataset and for testing with
synthetic fixtures.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ---------------------------------------------------------------------------
# Constants — no magic numbers
# ---------------------------------------------------------------------------
DEFAULT_RANDOM_STATE: int = 42
DEFAULT_TEST_SIZE: float = 0.3
CLAIM_THRESHOLD: float = 0.0
MISSING_CATEGORY_FILL: str = "Unknown"
MISSING_NUMERIC_FILL: float = 0.0

# Columns that must not be used as features
TARGET_COLUMNS: List[str] = [
    "TotalClaims",
    "TotalPremium",
    "HasClaim",
    "LossRatio",
    "ClaimSeverity",
    "ProfitMargin",
]


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values using median for numeric and mode/Unknown for categorical.

    Args:
        df: Raw DataFrame.

    Returns:
        DataFrame with no missing values.
    """
    df = df.copy()
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
        if df[col].dtype in ("int64", "float64"):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode_vals = df[col].mode()
            fill = mode_vals.iloc[0] if len(mode_vals) > 0 else MISSING_CATEGORY_FILL
            df[col] = df[col].fillna(fill)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features relevant to insurance risk.

    Args:
        df: Cleaned DataFrame.

    Returns:
        DataFrame with engineered features appended.
    """
    df = df.copy()
    if "TotalClaims" in df.columns and "TotalPremium" in df.columns:
        df["HasClaim"] = (df["TotalClaims"] > CLAIM_THRESHOLD).astype(int)
        df["LossRatio"] = np.where(
            df["TotalPremium"] > 0,
            df["TotalClaims"] / df["TotalPremium"],
            MISSING_NUMERIC_FILL,
        )
        df["ProfitMargin"] = df["TotalPremium"] - df["TotalClaims"]
    return df


def encode_categoricals(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Label-encode categorical columns (fast, deterministic).

    Args:
        df: DataFrame with potential object columns.
        columns: Explicit list of columns to encode. Auto-detected when *None*.

    Returns:
        DataFrame with all object columns converted to numeric.
    """
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=["object"]).columns.tolist()
    columns = [c for c in columns if c not in TARGET_COLUMNS and c in df.columns]

    for col in columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    return df


def prepare_features_target(
    df: pd.DataFrame,
    target_col: str,
    filter_positive: bool = False,
) -> Tuple[pd.DataFrame, pd.Series]:
    """Extract numeric features and a target column.

    Args:
        df: Preprocessed DataFrame.
        target_col: Name of the target column.
        filter_positive: If *True*, keep only rows where target > 0.

    Returns:
        Tuple of (X, y).
    """
    if filter_positive:
        df = df[df[target_col] > CLAIM_THRESHOLD].copy()

    y = df[target_col].copy()
    feature_cols = [c for c in df.columns if c not in TARGET_COLUMNS]
    X = df[feature_cols].select_dtypes(include=[np.number]).copy()
    return X, y


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into train and test sets.

    Args:
        X: Feature matrix.
        y: Target vector.
        test_size: Fraction held out for testing.
        random_state: Seed for reproducibility.

    Returns:
        (X_train, X_test, y_train, y_test)
    """
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )


def run_preprocessing_pipeline(
    df: pd.DataFrame,
    target_col: str = "TotalPremium",
    filter_positive: bool = False,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """End-to-end preprocessing: clean -> engineer -> encode -> split.

    Args:
        df: Raw DataFrame.
        target_col: Column to predict.
        filter_positive: Keep only positive-target rows when True.
        test_size: Test set proportion.
        random_state: Seed for reproducibility.

    Returns:
        (X_train, X_test, y_train, y_test)
    """
    df = handle_missing_values(df)
    df = engineer_features(df)
    df = encode_categoricals(df)
    X, y = prepare_features_target(df, target_col, filter_positive)
    return split_data(X, y, test_size=test_size, random_state=random_state)
