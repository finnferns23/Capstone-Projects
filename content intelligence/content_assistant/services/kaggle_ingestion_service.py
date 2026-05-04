from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd

from content_assistant.data_pipeline.kaggle_dataset_registry import KaggleDatasetSpec, load_kaggle_registry
from content_assistant.data_pipeline.kaggle_schema_mapper import normalize_kaggle_frame


class KaggleIngestionService:
    def __init__(self, registry_path: str = "data/kaggle_configs/kaggle_dataset_registry.json") -> None:
        self.registry_path = registry_path
        self.registry: Dict[str, KaggleDatasetSpec] = load_kaggle_registry(registry_path)

    def discover_csv_files(self, dataset_name: str) -> List[Path]:
        spec = self.registry[dataset_name]
        folder = Path(spec.target_folder)
        if not folder.exists():
            return []
        return sorted(folder.rglob("*.csv"))

    def load_dataset(self, dataset_name: str, limit: int | None = None) -> pd.DataFrame:
        spec = self.registry[dataset_name]
        frames: List[pd.DataFrame] = []
        for csv_path in self.discover_csv_files(dataset_name):
            frame = pd.read_csv(csv_path)
            normalized = normalize_kaggle_frame(frame, dataset_name, spec.project_mapping)
            frames.append(normalized)
        if not frames:
            return pd.DataFrame(columns=["source", "title", "content", "category", "channel", "engagement_metric", "conversion_metric", "image_reference"])
        combined = pd.concat(frames, ignore_index=True)
        return combined.head(limit) if limit else combined

    def load_many(self, dataset_names: Iterable[str] | None = None, limit_per_dataset: int | None = 1000) -> pd.DataFrame:
        names = list(dataset_names) if dataset_names else list(self.registry.keys())
        frames = [self.load_dataset(name, limit=limit_per_dataset) for name in names]
        non_empty = [frame for frame in frames if not frame.empty]
        if not non_empty:
            return pd.DataFrame(columns=["source", "title", "content", "category", "channel", "engagement_metric", "conversion_metric", "image_reference"])
        return pd.concat(non_empty, ignore_index=True)

    def export_training_ready_dataset(self, output_path: str = "data/datasets/kaggle_training_ready.csv") -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        dataset = self.load_many()
        dataset.to_csv(output, index=False)
        return output
