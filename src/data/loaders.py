"""Data loading utilities for the insurance risk analysis pipeline.

Loads CSV/text data from disk. Accepts explicit file_path parameter
so tests can inject a synthetic fixture without touching DVC data.
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


def load_insurance_data(
    file_path: Optional[Union[str, Path]] = None,
    sep: str = DEFAULT_SEPARATOR,
    **kwargs,
) -> pd.DataFrame:
    """Load insurance dataset from a CSV / delimited file.

    Parameters
    ----------
    file_path : str or Path, optional
        Absolute or relative path to the data file.
        Defaults to ``data/raw/MachineLearningRating_v3.txt`` (DVC-tracked).
    sep : str
        Column separator (default ``|``).
    **kwargs
        Extra keyword arguments forwarded to :func:`pandas.read_csv`.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If *file_path* does not exist on disk.
    ValueError
        If the file cannot be parsed.
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
