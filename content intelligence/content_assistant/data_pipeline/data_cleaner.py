"""Text and dataset cleaning helpers powered by pandas and NumPy."""
from __future__ import annotations

import re
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

_WHITESPACE_RE = re.compile(r"\s+")
_URL_RE = re.compile(r"https?://\S+|www\.\S+")


def clean_text(text: object) -> str:
    """Normalize text while preserving meaning for classification and RAG."""
    value = "" if text is None else str(text)
    value = _URL_RE.sub(" ", value)
    value = value.replace("\n", " ").replace("\t", " ")
    value = _WHITESPACE_RE.sub(" ", value).strip()
    return value


def clean_dataframe(frame: pd.DataFrame, text_columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Clean a pandas DataFrame and normalize selected text columns."""
    cleaned = frame.copy().replace({np.nan: ""})
    cleaned.columns = [str(column).strip().lower() for column in cleaned.columns]
    columns = list(text_columns or cleaned.select_dtypes(include=["object"]).columns)
    for column in columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].map(clean_text)
    return cleaned.drop_duplicates().reset_index(drop=True)


def build_training_columns(rows: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:
    """Extract text and label arrays from flexible dataset schemas."""
    if not rows:
        return [], []
    frame = clean_dataframe(pd.DataFrame(rows))
    label_column = "label" if "label" in frame.columns else frame.columns[0]
    text_column = "text" if "text" in frame.columns else frame.columns[-1]
    texts = frame[text_column].astype(str).map(clean_text).tolist()
    labels = frame[label_column].astype(str).map(clean_text).str.lower().tolist()
    pairs = [(text, label) for text, label in zip(texts, labels) if text and label]
    return [text for text, _ in pairs], [label for _, label in pairs]
