from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping


@dataclass(frozen=True)
class KaggleDatasetSpec:
    name: str
    slug: str
    target_folder: str
    task: str
    recommended_use: str
    expected_columns: List[str]
    project_mapping: Mapping[str, str]


def load_kaggle_registry(path: str | Path = "data/kaggle_configs/kaggle_dataset_registry.json") -> Dict[str, KaggleDatasetSpec]:
    registry_path = Path(path)
    with registry_path.open("r", encoding="utf-8") as file:
        raw_registry = json.load(file)
    return {
        name: KaggleDatasetSpec(name=name, **spec)
        for name, spec in raw_registry.items()
    }


def list_kaggle_datasets(path: str | Path = "data/kaggle_configs/kaggle_dataset_registry.json") -> List[str]:
    return sorted(load_kaggle_registry(path).keys())
