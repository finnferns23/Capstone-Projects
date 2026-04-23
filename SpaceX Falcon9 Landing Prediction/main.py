"""Production-ready launcher for the SpaceX Falcon 9 landing prediction project."""

from __future__ import annotations

import argparse
import compileall
import os
import subprocess
import sys

import pandas as pd

from project_paths import ASSETS_DIR, BASE_DIR, DOCS_DIR, REPORTS_DIR, ensure_directories, find_data_file

SCRIPTS: list[tuple[str, str]] = [
    ("api", "scripts/01_data_collection/api_data_collection.py"),
    ("scrape", "scripts/01_data_collection/launch_data_scraping.py"),
    ("wrangle", "scripts/02_data_wrangling/launch_data_wrangling.py"),
    ("eda", "scripts/03_exploratory_data_analysis/launch_eda.py"),
    ("sql", "scripts/03_exploratory_data_analysis/launch_sql_analysis.py"),
    ("folium", "scripts/04_visualization/launch_site_map.py"),
    ("ml", "scripts/06_machine_learning/landing_prediction_model.py"),
    ("dash", "scripts/05_dashboard/dashboard_app.py"),
]
ALIASES = {name: relpath for name, relpath in SCRIPTS}
DEFAULT_PIPELINE = ["wrangle", "eda", "sql", "folium", "ml"]


def run_script(stage: str) -> int:
    script_path = BASE_DIR / ALIASES[stage]
    if not script_path.exists():
        raise FileNotFoundError(f"Missing script: {script_path}")
    print(f"[RUNNING] {stage} -> {script_path.relative_to(BASE_DIR)}")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BASE_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run([sys.executable, str(script_path)], cwd=BASE_DIR, env=env)
    print(f"[DONE] {stage} -> exit code {result.returncode}\n")
    return result.returncode


def validate_project() -> int:
    ensure_directories()
    required_files = [
        "dataset_part_1.csv",
        "dataset_part_2.csv",
        "dataset_part_3.csv",
        "spacex_launch_dash.csv",
        "spacex_launch_geo.csv",
        "spacex_sql_dataset.csv",
    ]
    for filename in required_files:
        path = find_data_file(filename)
        if not path.exists():
            print(f"Missing required data file: {filename}")
            return 1
        pd.read_csv(path, nrows=5)
        print(f"Validated data file: {path.relative_to(BASE_DIR)}")

    if not compileall.compile_dir(str(BASE_DIR), quiet=1):
        print("Python compilation failed.")
        return 1

    generated_assets = sorted(p.name for p in ASSETS_DIR.glob("*"))
    generated_reports = sorted(p.name for p in REPORTS_DIR.glob("*"))
    print(f"Assets directory: {generated_assets or 'ready'}")
    print(f"Reports directory: {generated_reports or 'ready'}")
    print("Validation completed successfully.")
    return 0


def build_file_index() -> None:
    lines = ["SpaceX Falcon 9 Landing Prediction - File Index", ""]
    for path in sorted(BASE_DIR.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            lines.append(str(path.relative_to(BASE_DIR)))
    (DOCS_DIR / "file_index.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or validate the SpaceX capstone project.")
    parser.add_argument("--list", action="store_true", help="Show available stages.")
    parser.add_argument("--run", choices=sorted(ALIASES), help="Run a single stage.")
    parser.add_argument("--pipeline", action="store_true", help="Run the default local pipeline.")
    parser.add_argument("--validate", action="store_true", help="Validate files and Python compilation.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_directories()
    build_file_index()

    if args.list:
        for name, relpath in SCRIPTS:
            print(f"{name:<7} {relpath}")
        return 0
    if args.validate:
        return validate_project()
    if args.run:
        return run_script(args.run)
    if args.pipeline:
        for stage in DEFAULT_PIPELINE:
            code = run_script(stage)
            if code != 0:
                return code
        return 0

    print("Use --list, --validate, --run <stage>, or --pipeline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
