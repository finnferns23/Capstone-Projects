"""Normalize downloaded Kaggle CSV files into the capstone training format."""
from __future__ import annotations

import argparse

from content_assistant.services.kaggle_ingestion_service import KaggleIngestionService


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a training-ready CSV from downloaded Kaggle datasets")
    parser.add_argument("--registry", default="data/kaggle_configs/kaggle_dataset_registry.json", help="Path to Kaggle registry JSON")
    parser.add_argument("--output", default="data/datasets/kaggle_training_ready.csv", help="Output CSV path")
    args = parser.parse_args()

    service = KaggleIngestionService(registry_path=args.registry)
    output_path = service.export_training_ready_dataset(output_path=args.output)
    print(f"Exported training-ready dataset: {output_path}")


if __name__ == "__main__":
    main()
