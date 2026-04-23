"""Wrangle launch outcome data and create the binary landing class label."""

from __future__ import annotations

import pandas as pd

from project_paths import PROCESSED_DATA_DIR, ensure_directories, find_data_file

REMOTE_CSV = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
OUTPUT_CSV = PROCESSED_DATA_DIR / "dataset_part_2.csv"


def load_dataset() -> pd.DataFrame:
    local_csv = find_data_file("dataset_part_1.csv")
    if local_csv.exists():
        return pd.read_csv(local_csv)
    return pd.read_csv(REMOTE_CSV)


def add_class_label(df: pd.DataFrame) -> pd.DataFrame:
    bad_outcomes = {"False Ocean", "False ASDS", "False RTLS", "None ASDS", "None None"}
    result = df.copy()
    result["Class"] = result["Outcome"].apply(lambda value: 0 if value in bad_outcomes else 1)
    return result


def main() -> None:
    ensure_directories()
    df = add_class_label(load_dataset())
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {OUTPUT_CSV} with {len(df)} rows.")
    print(df[["Outcome", "Class"]].head())
    print("Class success rate:", round(float(df["Class"].mean()), 4))


if __name__ == "__main__":
    main()
