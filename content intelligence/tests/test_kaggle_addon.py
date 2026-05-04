from pathlib import Path

from content_assistant.data_pipeline.kaggle_dataset_registry import load_kaggle_registry
from content_assistant.data_pipeline.kaggle_schema_mapper import normalize_kaggle_frame

import pandas as pd


def test_kaggle_registry_loads():
    registry = load_kaggle_registry("data/kaggle_configs/kaggle_dataset_registry.json")
    assert "ecommerce_text" in registry
    assert registry["ecommerce_text"].slug == "saurabhshahane/ecommerce-text-classification"


def test_schema_mapper_outputs_standard_columns():
    frame = pd.DataFrame({"label": ["Books"], "text": ["A beginner friendly AI book"]})
    mapped = normalize_kaggle_frame(frame, "ecommerce_text", {"label": "category", "text": "content"})
    assert mapped.loc[0, "source"] == "ecommerce_text"
    assert mapped.loc[0, "category"] == "Books"
    assert mapped.loc[0, "content"] == "A beginner friendly AI book"


def test_addon_files_exist():
    assert Path("scripts/download_kaggle_datasets.py").exists()
    assert Path("scripts/ingest_kaggle_assets.py").exists()
