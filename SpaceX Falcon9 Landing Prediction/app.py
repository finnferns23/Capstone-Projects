from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

import main as cli_main
from project_paths import ASSETS_DIR, BASE_DIR, DATA_DIR, REPORTS_DIR

st.set_page_config(page_title="SpaceX Falcon 9 Project", page_icon="🚀", layout="wide")


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=str(BASE_DIR), text=True, capture_output=True)


def available_csv_files() -> list[Path]:
    return sorted(DATA_DIR.rglob("*.csv"))


def available_assets() -> list[Path]:
    return sorted(path for path in ASSETS_DIR.glob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".html"})


def available_reports() -> list[Path]:
    return sorted(path for path in REPORTS_DIR.glob("*") if path.suffix.lower() in {".pdf", ".pptx"})


def render_command_result(result: subprocess.CompletedProcess[str]) -> None:
    output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
    if result.returncode == 0:
        st.success("Command completed successfully.")
    else:
        st.error(f"Command failed with exit code {result.returncode}.")
    if output:
        st.code(output, language="text")


st.title("SpaceX Falcon 9 Landing Prediction")
st.caption("Production-ready local package with command-line and browser entry points.")

tab_overview, tab_launcher, tab_data, tab_assets, tab_reports = st.tabs(["Overview", "Launcher", "Data", "Assets", "Reports"])

with tab_overview:
    st.markdown("- Terminal launcher: `python main.py --validate` or `python main.py --pipeline`")
    st.markdown("- Browser launcher: `streamlit run app.py`")
    st.markdown("- Core workflow: wrangling, EDA, SQL, Folium map, machine learning")
    st.markdown("- Optional legacy web stages: API collection, scraping, Dash app")

with tab_launcher:
    command = st.selectbox("Choose an action", ["validate", "pipeline", *cli_main.ALIASES.keys()])
    if st.button("Run action", type="primary"):
        if command == "validate":
            render_command_result(run_command("main.py", "--validate"))
        elif command == "pipeline":
            render_command_result(run_command("main.py", "--pipeline"))
        else:
            render_command_result(run_command("main.py", "--run", command))

with tab_data:
    csv_files = available_csv_files()
    selected_csv = st.selectbox("Choose a CSV file", csv_files, format_func=lambda p: str(p.relative_to(BASE_DIR)))
    preview_rows = st.slider("Rows to preview", 5, 100, 20, 5)
    df = pd.read_csv(selected_csv)
    st.caption(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    st.dataframe(df.head(preview_rows), use_container_width=True)

with tab_assets:
    assets = available_assets()
    if not assets:
        st.info("No generated assets found yet.")
    for asset in assets:
        st.markdown(f"**{asset.name}**")
        if asset.suffix.lower() == ".html":
            st.caption(str(asset.relative_to(BASE_DIR)))
        else:
            st.image(str(asset), use_container_width=True)

with tab_reports:
    reports = available_reports()
    if not reports:
        st.info("No report files found.")
    for report in reports:
        st.markdown(f"**{report.name}**")
        with report.open("rb") as fh:
            st.download_button(f"Download {report.name}", fh.read(), file_name=report.name, key=report.name)
