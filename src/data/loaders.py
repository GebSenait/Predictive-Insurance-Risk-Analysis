"""Data loading utilities."""

from pathlib import Path
from typing import Optional, Union

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    """Class for loading data from various sources."""

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize DataLoader.

        Args:
            data_path: Base path for data files
        """
        self.data_path = data_path
        self.logger = logger

    def load_csv(
        self,
        file_path: Union[str, Path],
        sep: str = ",",
        **kwargs,
    ) -> pd.DataFrame:
        """
        Load data from CSV file.

        Args:
            file_path: Path to CSV file
            **kwargs: Additional arguments passed to pd.read_csv()

        Returns:
            Loaded DataFrame

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file cannot be read
        """
        file_path = Path(file_path)

        # Resolve relative paths
        if not file_path.is_absolute() and self.data_path:
            file_path = self.data_path / file_path

        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        try:
            self.logger.info(f"Loading CSV file: {file_path}")
            df = pd.read_csv(file_path, sep=sep, **kwargs)
            self.logger.info(f"Successfully loaded {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading CSV file {file_path}: {e}")
            raise ValueError(f"Failed to load CSV file: {e}") from e

    def load_excel(
        self,
        file_path: Union[str, Path],
        sheet_name: Optional[Union[str, int]] = 0,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Load data from Excel file.

        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name or index to load
            **kwargs: Additional arguments passed to pd.read_excel()

        Returns:
            Loaded DataFrame

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file cannot be read
        """
        file_path = Path(file_path)

        # Resolve relative paths
        if not file_path.is_absolute() and self.data_path:
            file_path = self.data_path / file_path

        if not file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")

        try:
            self.logger.info(f"Loading Excel file: {file_path}")
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            self.logger.info(f"Successfully loaded {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading Excel file {file_path}: {e}")
            raise ValueError(f"Failed to load Excel file: {e}") from e

    def load_parquet(
        self,
        file_path: Union[str, Path],
        **kwargs,
    ) -> pd.DataFrame:
        """
        Load data from Parquet file.

        Args:
            file_path: Path to Parquet file
            **kwargs: Additional arguments passed to pd.read_parquet()

        Returns:
            Loaded DataFrame

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file cannot be read
        """
        file_path = Path(file_path)

        # Resolve relative paths
        if not file_path.is_absolute() and self.data_path:
            file_path = self.data_path / file_path

        if not file_path.exists():
            raise FileNotFoundError(f"Parquet file not found: {file_path}")

        try:
            self.logger.info(f"Loading Parquet file: {file_path}")
            df = pd.read_parquet(file_path, **kwargs)
            self.logger.info(f"Successfully loaded {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading Parquet file {file_path}: {e}")
            raise ValueError(f"Failed to load Parquet file: {e}") from e

