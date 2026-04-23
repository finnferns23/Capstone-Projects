"""Run exploratory analysis and feature engineering on the SpaceX capstone dataset."""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from project_paths import ASSETS_DIR, PROCESSED_DATA_DIR, ensure_directories, find_data_file

REMOTE_CSV = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
OUTPUT_CSV = PROCESSED_DATA_DIR / "dataset_part_3.csv"


def load_dataset() -> pd.DataFrame:
    local_csv = find_data_file("dataset_part_2.csv")
    if local_csv.exists():
        return pd.read_csv(local_csv)
    return pd.read_csv(REMOTE_CSV)


def extract_years(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["Date"] = pd.to_datetime(result["Date"]).dt.year.astype(str)
    return result


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df[[
        "FlightNumber",
        "PayloadMass",
        "Orbit",
        "LaunchSite",
        "Flights",
        "GridFins",
        "Reused",
        "Legs",
        "LandingPad",
        "Block",
        "ReusedCount",
        "Serial",
    ]].copy()
    return pd.get_dummies(features, columns=["Orbit", "LaunchSite", "LandingPad", "Serial"]).astype("float64")


def save_plot(fig: plt.Figure, filename: str) -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def create_visuals(df: pd.DataFrame) -> None:
    fig1 = sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=2.5).fig
    save_plot(fig1, "payload_vs_flightnumber.png")

    fig2 = sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=2.0).fig
    save_plot(fig2, "payload_vs_launchsite.png")

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    df.groupby("Orbit")["Class"].mean().plot(kind="bar", ax=ax3, title="Success Rate by Orbit")
    ax3.set_xlabel("Orbit")
    ax3.set_ylabel("Success Rate")
    save_plot(fig3, "success_rate_by_orbit.png")

    yearly = extract_years(df).groupby("Date")["Class"].mean().reset_index()
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.plot(yearly["Date"], yearly["Class"], marker="o")
    ax4.set_title("Success Rate by Year")
    ax4.set_xlabel("Year")
    ax4.set_ylabel("Success Rate")
    save_plot(fig4, "success_rate_by_year.png")


def main() -> None:
    ensure_directories()
    df = load_dataset()
    create_visuals(df)
    features = build_features(df)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {OUTPUT_CSV} with shape {features.shape}.")


if __name__ == "__main__":
    main()
