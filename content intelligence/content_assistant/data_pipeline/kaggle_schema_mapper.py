from __future__ import annotations

from typing import Mapping

import pandas as pd


STANDARD_COLUMNS = ["source", "title", "content", "category", "channel", "engagement_metric", "conversion_metric", "image_reference"]


def normalize_kaggle_frame(frame: pd.DataFrame, dataset_name: str, column_mapping: Mapping[str, str]) -> pd.DataFrame:
    normalized = pd.DataFrame()
    for source_column, target_column in column_mapping.items():
        if source_column in frame.columns:
            normalized[target_column] = frame[source_column]
    if "content" not in normalized.columns:
        text_columns = [column for column in ["description", "short_description", "headline", "text", "title"] if column in frame.columns]
        normalized["content"] = frame[text_columns].astype(str).agg(" ".join, axis=1) if text_columns else ""
    if "title" not in normalized.columns:
        normalized["title"] = normalized["content"].astype(str).str.slice(0, 80)
    if "category" not in normalized.columns:
        normalized["category"] = "unknown"
    normalized["source"] = dataset_name
    for column in STANDARD_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = ""
    normalized = normalized[STANDARD_COLUMNS]
    normalized["content"] = normalized["content"].fillna("").astype(str).str.strip()
    return normalized[normalized["content"].str.len() > 0].reset_index(drop=True)
