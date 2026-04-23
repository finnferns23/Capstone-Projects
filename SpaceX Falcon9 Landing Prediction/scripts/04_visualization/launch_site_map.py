"""Build the Folium launch-site map and save it to the assets folder."""

from __future__ import annotations

import folium
import pandas as pd
from folium.plugins import MousePosition

from project_paths import ASSETS_DIR, ensure_directories, find_data_file

OUTPUT_HTML = ASSETS_DIR / "spacex_launch_sites_map.html"


def add_launch_site_markers(site_map: folium.Map, launch_sites_df: pd.DataFrame) -> None:
    for _, row in launch_sites_df.iterrows():
        site_map.add_child(
            folium.Marker(
                [row["Lat"], row["Long"]],
                popup=row["Launch Site"],
                icon=folium.Icon(color="blue", icon="info-sign"),
            )
        )


def add_success_failure_markers(site_map: folium.Map, spacex_df: pd.DataFrame) -> None:
    for _, row in spacex_df.iterrows():
        color = "green" if int(row["class"]) == 1 else "red"
        text = f"{row['Launch Site']} - {'Success' if int(row['class']) == 1 else 'Failure'}"
        site_map.add_child(
            folium.CircleMarker(
                [row["Lat"], row["Long"]],
                radius=5,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=text,
            )
        )


def main() -> None:
    ensure_directories()
    spacex_df = pd.read_csv(find_data_file("spacex_launch_geo.csv"))[["Launch Site", "Lat", "Long", "class"]].copy()
    launch_sites_df = spacex_df.groupby("Launch Site", as_index=False).first()[["Launch Site", "Lat", "Long"]]
    site_map = folium.Map(location=[29.559684888503615, -95.0830971930759], zoom_start=4)
    add_launch_site_markers(site_map, launch_sites_df)
    add_success_failure_markers(site_map, spacex_df)
    site_map.add_child(MousePosition())
    site_map.save(OUTPUT_HTML)
    print(f"Saved {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
