"""Collect SpaceX launch data from the public SpaceX API and build the capstone base dataset."""

from __future__ import annotations

from pathlib import Path

import datetime as dt
from typing import Any

import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def resolve_data_path(filename: str) -> Path:
    """Return a local dataset path from script folder or ./data folder."""
    candidates = [BASE_DIR / filename, DATA_DIR / filename, Path(filename)]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return BASE_DIR / filename

SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/past"
OUTPUT_CSV = resolve_data_path("dataset_part_1.csv")

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)


def fetch_json(url: str) -> Any:
    """Fetch JSON data from a URL with basic error handling."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def get_booster_versions(data: pd.DataFrame) -> list[str]:
    booster_versions: list[str] = []
    for rocket_id in data["rocket"]:
        rocket = fetch_json(f"https://api.spacexdata.com/v4/rockets/{rocket_id}")
        booster_versions.append(rocket["name"])
    return booster_versions


def get_launch_site_details(data: pd.DataFrame) -> tuple[list[float], list[float], list[str]]:
    longitudes: list[float] = []
    latitudes: list[float] = []
    launch_sites: list[str] = []
    for launchpad_id in data["launchpad"]:
        launchpad = fetch_json(f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}")
        longitudes.append(launchpad["longitude"])
        latitudes.append(launchpad["latitude"])
        launch_sites.append(launchpad["name"])
    return longitudes, latitudes, launch_sites


def get_payload_details(data: pd.DataFrame) -> tuple[list[float | None], list[str | None]]:
    payload_masses: list[float | None] = []
    orbits: list[str | None] = []
    for payload_id in data["payloads"]:
        payload = fetch_json(f"https://api.spacexdata.com/v4/payloads/{payload_id}")
        payload_masses.append(payload.get("mass_kg"))
        orbits.append(payload.get("orbit"))
    return payload_masses, orbits


def get_core_details(data: pd.DataFrame) -> dict[str, list[Any]]:
    details = {
        "Outcome": [],
        "Flights": [],
        "GridFins": [],
        "Reused": [],
        "Legs": [],
        "LandingPad": [],
        "Block": [],
        "ReusedCount": [],
        "Serial": [],
    }

    for core in data["cores"]:
        core_id = core.get("core")
        if core_id is not None:
            core_data = fetch_json(f"https://api.spacexdata.com/v4/cores/{core_id}")
            details["Block"].append(core_data.get("block"))
            details["ReusedCount"].append(core_data.get("reuse_count"))
            details["Serial"].append(core_data.get("serial"))
        else:
            details["Block"].append(None)
            details["ReusedCount"].append(None)
            details["Serial"].append(None)

        details["Outcome"].append(f"{core.get('landing_success')} {core.get('landing_type')}")
        details["Flights"].append(core.get("flight"))
        details["GridFins"].append(core.get("gridfins"))
        details["Reused"].append(core.get("reused"))
        details["Legs"].append(core.get("legs"))
        details["LandingPad"].append(core.get("landpad"))

    return details


def build_dataset() -> pd.DataFrame:
    data = pd.json_normalize(fetch_json(SPACEX_API_URL))
    data = data[["rocket", "payloads", "launchpad", "cores", "flight_number", "date_utc"]]
    data = data[data["cores"].map(len) == 1]
    data = data[data["payloads"].map(len) == 1]
    data["cores"] = data["cores"].map(lambda values: values[0])
    data["payloads"] = data["payloads"].map(lambda values: values[0])
    data["date"] = pd.to_datetime(data["date_utc"]).dt.date
    data = data[data["date"] <= dt.date(2020, 11, 13)]

    booster_versions = get_booster_versions(data)
    longitudes, latitudes, launch_sites = get_launch_site_details(data)
    payload_masses, orbits = get_payload_details(data)
    core_details = get_core_details(data)

    launch_dict = {
        "FlightNumber": list(data["flight_number"]),
        "Date": list(data["date"]),
        "BoosterVersion": booster_versions,
        "PayloadMass": payload_masses,
        "Orbit": orbits,
        "LaunchSite": launch_sites,
        "Longitude": longitudes,
        "Latitude": latitudes,
        **core_details,
    }
    launch_df = pd.DataFrame(launch_dict)
    launch_df = launch_df[launch_df["BoosterVersion"] != "Falcon 1"].copy()
    launch_df.loc[:, "FlightNumber"] = range(1, launch_df.shape[0] + 1)
    launch_df["PayloadMass"] = launch_df["PayloadMass"].fillna(launch_df["PayloadMass"].mean())
    return launch_df


def main() -> None:
    dataset = build_dataset()
    dataset.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {OUTPUT_CSV} with {len(dataset)} rows.")
    print(dataset.head())


if __name__ == "__main__":
    main()