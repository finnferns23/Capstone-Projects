"""Dataset insight helpers for Streamlit and capstone reporting."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from content_assistant.data_pipeline.data_loader import dataset_profile, load_dataframe


class DataInsightService:
    """Generate lightweight analytical summaries from CSV datasets."""

    def summarize_csv(self, path: str | Path) -> Dict[str, object]:
        frame = load_dataframe(path)
        profile = dataset_profile(frame)
        object_columns = frame.select_dtypes(include=["object"]).columns.tolist()
        profile["text_columns"] = object_columns
        if "label" in frame.columns:
            profile["label_distribution"] = frame["label"].astype(str).value_counts().to_dict()
        numeric_frame = frame.select_dtypes(include=["number"])
        numeric_summary = numeric_frame.describe().to_dict() if not numeric_frame.empty else {}
        profile["numeric_summary"] = numeric_summary
        return profile

    def combine_summaries(self, dataset_dir: str | Path) -> Dict[str, object]:
        root = Path(dataset_dir)
        summaries = {}
        for path in sorted(root.glob("*.csv")):
            summaries[path.name] = self.summarize_csv(path)
        return summaries
