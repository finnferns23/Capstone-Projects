from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ASSETS_DIR = BASE_DIR / "assets"
REPORTS_DIR = BASE_DIR / "reports"
DOCS_DIR = BASE_DIR / "docs"

def ensure_directories() -> None:
    for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, ASSETS_DIR, REPORTS_DIR, DOCS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

def find_data_file(filename: str) -> Path:
    candidates = [
        BASE_DIR / filename,
        DATA_DIR / filename,
        RAW_DATA_DIR / filename,
        PROCESSED_DATA_DIR / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    recursive = list(DATA_DIR.rglob(filename))
    if recursive:
        return recursive[0]
    return PROCESSED_DATA_DIR / filename
