"""Data loading utilities for the insurance risk analysis pipeline.

Provides:
- ``load_insurance_data`` -- lightweight function for the modular pipeline and tests
- ``DataLoader`` -- class-based loader used by Task 3/4 analysis modules

Both accept an explicit ``file_path`` parameter so tests can inject a synthetic
fixture without touching the DVC-tracked production dataset.
"""

from pathlib import Path
from typing import Optional, Union

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_SEPARATOR: str = "|"
DEFAULT_RAW_DIR: str = "data/raw"
DEFAULT_FILENAME: str = "MachineLearningRating_v3.txt"


# ---------------------------------------------------------------------------
# Function-based API (used by scripts/run_pipeline.py and new tests)
# ---------------------------------------------------------------------------


def load_insurance_data(
    file_path: Optional[Union[str, Path]] = None,
    sep: str = DEFAULT_SEPARATOR,
    **kwargs,
) -> pd.DataFrame:
    """Load insurance dataset from a CSV / delimited file.

    Args:
        file_path: Absolute or relative path to the data file.
            Defaults to ``data/raw/MachineLearningRating_v3.txt`` (DVC-tracked).
        sep: Column separator (default ``|``).
        **kwargs: Extra keyword arguments forwarded to ``pd.read_csv``.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If *file_path* does not exist on disk.
        ValueError: If the file cannot be parsed.
    """
    if file_path is None:
        file_path = Path(DEFAULT_RAW_DIR) / DEFAULT_FILENAME

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    try:
        df: pd.DataFrame = pd.read_csv(file_path, sep=sep, low_memory=False, **kwargs)
    except Exception as exc:
        raise ValueError(f"Failed to read {file_path}: {exc}") from exc

    return df


# ---------------------------------------------------------------------------
# Class-based API (used by src/analysis/task3, task4 and legacy tests)
# ---------------------------------------------------------------------------


class DataLoader:
    """Class for loading data from various sources.

    Attributes:
        data_path: Optional base directory that relative file paths are
            resolved against.
    """

    def __init__(self, data_path: Optional[Path] = None) -> None:
        """Initialise DataLoader.

        Args:
            data_path: Base path for data files.
        """
        self.data_path = data_path

    def load_csv(
        self,
        file_path: Union[str, Path],
        sep: str = ",",
        **kwargs,
    ) -> pd.DataFrame:
        """Load data from a CSV file.

        Args:
            file_path: Path to CSV file.
            sep: Column separator.
            **kwargs: Additional arguments passed to ``pd.read_csv``.

        Returns:
            Loaded DataFrame.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If file cannot be read.
        """
        file_path = Path(file_path)

        # Resolve relative paths against base data_path
        if not file_path.is_absolute() and self.data_path:
            file_path = self.data_path / file_path

        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        try:
            df = pd.read_csv(file_path, sep=sep, **kwargs)
            return df
        except Exception as exc:
            raise ValueError(f"Failed to load CSV file: {exc}") from exc

    def load_excel(
        self,
        file_path: Union[str, Path],
        sheet_name: Optional[Union[str, int]] = 0,
        **kwargs,
    ) -> pd.DataFrame:
        """Load data from an Excel file.

        Args:
            file_path: Path to Excel file.
            sheet_name: Sheet name or index to load.
            **kwargs: Additional arguments passed to ``pd.read_excel``.

        Returns:
            Loaded DataFrame.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If file cannot be read.
        """
        file_path = Path(file_path)

        if not file_path.is_absolute() and self.data_path:
            file_path = self.data_path / file_path

        if not file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            return df
        except Exception as exc:
            raise ValueError(f"Failed to load Excel file: {exc}") from exc

    def load_parquet(
        self,
        file_path: Union[str, Path],
        **kwargs,
    ) -> pd.DataFrame:
        """Load data from a Parquet file.

        Args:
            file_path: Path to Parquet file.
            **kwargs: Additional arguments passed to ``pd.read_parquet``.

        Returns:
            Loaded DataFrame.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If file cannot be read.
        """
        file_path = Path(file_path)

        if not file_path.is_absolute() and self.data_path:
            file_path = self.data_path / file_path

        if not file_path.exists():
            raise FileNotFoundError(f"Parquet file not found: {file_path}")

        try:
            df = pd.read_parquet(file_path, **kwargs)
            return df
        except Exception as exc:
            raise ValueError(f"Failed to load Parquet file: {exc}") from exc
