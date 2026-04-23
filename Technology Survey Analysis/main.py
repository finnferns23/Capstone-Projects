"""Production-ready launcher for the Technology Survey capstone package."""

from __future__ import annotations

import argparse
import compileall

import pandas as pd

from project_paths import ASSETS_DIR, BASE_DIR, DOCS_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR, REPORTS_DIR, ensure_directories

RAW_DATASET = RAW_DATA_DIR / "survey_data.csv"


def validate_project() -> int:
    ensure_directories()
    if not RAW_DATASET.exists():
        print(f"Missing dataset: {RAW_DATASET}")
        return 1
    df = pd.read_csv(RAW_DATASET, nrows=50)
    print(f"Validated dataset: {RAW_DATASET.relative_to(BASE_DIR)}")
    print(f"Columns preview: {list(df.columns[:10])}")
    for folder in [ASSETS_DIR, REPORTS_DIR, DOCS_DIR, PROCESSED_DATA_DIR]:
        print(f"Validated folder: {folder.relative_to(BASE_DIR)}")
    if not compileall.compile_dir(str(BASE_DIR), quiet=1):
        print("Python compilation failed.")
        return 1
    print("Validation completed successfully.")
    return 0


def build_summary_outputs() -> int:
    ensure_directories()
    df = pd.read_csv(RAW_DATASET)
    top_countries = df["Country"].dropna().astype(str).value_counts().head(10).rename_axis("Country").reset_index(name="Count")
    top_languages = (
        df["LanguageHaveWorkedWith"]
        .dropna()
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(10)
        .rename_axis("Language")
        .reset_index(name="Count")
    )
    education = df["EdLevel"].dropna().astype(str).value_counts().head(10).rename_axis("Education Level").reset_index(name="Count")
    top_countries.to_csv(PROCESSED_DATA_DIR / "top_countries.csv", index=False)
    top_languages.to_csv(PROCESSED_DATA_DIR / "top_languages.csv", index=False)
    education.to_csv(PROCESSED_DATA_DIR / "top_education_levels.csv", index=False)
    summary = [
        "Technology Survey Capstone - Generated Summary Outputs",
        f"Rows: {len(df):,}",
        f"Columns: {len(df.columns):,}",
        "",
        "Top processed files:",
        "- top_countries.csv",
        "- top_languages.csv",
        "- top_education_levels.csv",
    ]
    (DOCS_DIR / "GENERATED_SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("Generated processed summary outputs.")
    return 0


def build_file_index() -> None:
    lines = ["Technology Survey Capstone - File Index", ""]
    for path in sorted(BASE_DIR.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            lines.append(str(path.relative_to(BASE_DIR)))
    (DOCS_DIR / "file_index.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate or summarize the Technology Survey capstone project.")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--list", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_file_index()
    if args.list:
        print("Available commands: --validate, --summary")
        return 0
    if args.validate:
        return validate_project()
    if args.summary:
        return build_summary_outputs()
    print("Use --list, --validate, or --summary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
