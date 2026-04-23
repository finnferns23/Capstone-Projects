"""Launch the SpaceX dashboard lab as a clean standalone Dash application."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def resolve_data_path(filename: str) -> Path:
    """Return a local dataset path from script folder or ./data folder."""
    candidates = [BASE_DIR / filename, DATA_DIR / filename, Path(filename)]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return BASE_DIR / filename

LOCAL_CSV = resolve_data_path("spacex_launch_dash.csv")
REMOTE_CSV = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"


def load_dataset() -> pd.DataFrame:
    if LOCAL_CSV.exists():
        return pd.read_csv(LOCAL_CSV)
    return pd.read_csv(REMOTE_CSV)


def create_app() -> Dash:
    spacex_df = load_dataset()
    min_payload = int(spacex_df["Payload Mass (kg)"].min())
    max_payload = int(spacex_df["Payload Mass (kg)"].max())
    launch_sites = sorted(spacex_df["Launch Site"].dropna().unique())
    site_options = [{"label": "All Sites", "value": "ALL"}] + [
        {"label": site, "value": site} for site in launch_sites
    ]

    app = Dash(__name__)
    app.layout = html.Div(
        children=[
            html.H1(
                "SpaceX Launch Records Dashboard",
                style={"textAlign": "center", "color": "#503D36", "fontSize": 40},
            ),
            dcc.Dropdown(
                id="site-dropdown",
                options=site_options,
                value="ALL",
                placeholder="Select a Launch Site",
                searchable=True,
                style={"width": "100%", "padding": "3px", "fontSize": "16px"},
            ),
            html.Br(),
            dcc.Graph(id="success-pie-chart"),
            html.P("Payload range (Kg):"),
            dcc.RangeSlider(
                id="payload-slider",
                min=min_payload,
                max=max_payload,
                step=1000,
                marks={i: str(i) for i in range(min_payload, max_payload + 1, 2500)},
                value=[min_payload, max_payload],
            ),
            html.Br(),
            dcc.Graph(id="success-payload-scatter-chart"),
        ]
    )

    @app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
    def get_pie_chart(entered_site: str):
        if entered_site == "ALL":
            success_by_site = (
                spacex_df.groupby("Launch Site", as_index=False)["class"]
                .sum()
                .rename(columns={"class": "Success Count"})
            )
            return px.pie(
                success_by_site,
                values="Success Count",
                names="Launch Site",
                title="Total Successful Launches by Site",
            )

        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        outcome_counts = (
            filtered_df["class"]
            .value_counts()
            .rename_axis("class")
            .reset_index(name="count")
        )
        outcome_counts["Outcome"] = outcome_counts["class"].map({1: "Success", 0: "Failure"})
        return px.pie(
            outcome_counts,
            values="count",
            names="Outcome",
            title=f"Launch Outcomes for {entered_site}",
        )

    @app.callback(
        Output("success-payload-scatter-chart", "figure"),
        Input("site-dropdown", "value"),
        Input("payload-slider", "value"),
    )
    def update_scatter_plot(entered_site: str, payload_range: list[int]):
        low, high = payload_range
        payload_filtered_df = spacex_df[
            (spacex_df["Payload Mass (kg)"] >= low)
            & (spacex_df["Payload Mass (kg)"] <= high)
        ]

        if entered_site == "ALL":
            chart_df = payload_filtered_df
            title = "Correlation between Payload and Success for All Sites"
        else:
            chart_df = payload_filtered_df[payload_filtered_df["Launch Site"] == entered_site]
            title = f"Correlation between Payload and Success for {entered_site}"

        return px.scatter(
            chart_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=title,
        )

    return app


if __name__ == "__main__":
    create_app().run(debug=False, port=8050)
