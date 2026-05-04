"""Advanced dataset loading utilities for capstone-grade content intelligence."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd


def load_dataframe(path: str | Path) -> pd.DataFrame:
    """Load a CSV dataset into a clean pandas DataFrame."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    frame = pd.read_csv(dataset_path)
    frame = frame.replace({np.nan: ""})
    frame.columns = [str(column).strip().lower() for column in frame.columns]
    return frame


def load_dataset(path: str | Path) -> List[Dict[str, str]]:
    """Load a CSV dataset as list-of-dicts for compatibility with existing services."""
    frame = load_dataframe(path)
    return frame.astype(str).to_dict(orient="records")


def load_many_frames(paths: Sequence[str | Path]) -> pd.DataFrame:
    """Load and concatenate multiple CSV files into one DataFrame."""
    frames = [load_dataframe(path) for path in paths]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False).replace({np.nan: ""})


def load_many(paths: Sequence[str | Path]) -> List[Dict[str, str]]:
    """Load and merge multiple CSV datasets as dictionaries."""
    return load_many_frames(paths).astype(str).to_dict(orient="records")


def dataset_profile(frame: pd.DataFrame) -> dict[str, object]:
    """Return a compact data-quality profile for Streamlit/reporting."""
    if frame.empty:
        return {"rows": 0, "columns": 0, "missing_values": 0, "duplicate_rows": 0}
    return {
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
        "missing_values": int(frame.isna().sum().sum()),
        "duplicate_rows": int(frame.duplicated().sum()),
        "column_names": list(frame.columns),
    }
