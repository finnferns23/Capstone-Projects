"""Download Kaggle datasets listed in the project registry.

This script is optional and only needs Kaggle credentials when you want to
replace the bundled sample datasets with larger external datasets.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from content_assistant.data_pipeline.kaggle_dataset_registry import load_kaggle_registry


def download_dataset(slug: str, target_folder: Path, unzip: bool = True) -> None:
    target_folder.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "kaggle",
        "datasets",
        "download",
        "-d",
        slug,
        "-p",
        str(target_folder),
    ]
    if unzip:
        command.append("--unzip")
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download datasets defined in data/kaggle_configs/kaggle_dataset_registry.json")
    parser.add_argument("--registry", default="data/kaggle_configs/kaggle_dataset_registry.json", help="Path to Kaggle registry JSON")
    parser.add_argument("--dataset", action="append", help="Dataset key to download. Repeat for multiple keys. Defaults to all.")
    parser.add_argument("--no-unzip", action="store_true", help="Keep downloaded archives compressed")
    args = parser.parse_args()

    registry = load_kaggle_registry(args.registry)
    selected = args.dataset or list(registry.keys())

    for name in selected:
        if name not in registry:
            raise KeyError(f"Unknown dataset key: {name}. Available: {', '.join(sorted(registry))}")
        spec = registry[name]
        print(f"Downloading {name}: {spec.slug} -> {spec.target_folder}")
        download_dataset(spec.slug, Path(spec.target_folder), unzip=not args.no_unzip)


if __name__ == "__main__":
    main()
