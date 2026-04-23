from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from project_paths import ASSETS_DIR, BASE_DIR, DATA_DIR, REPORTS_DIR

st.set_page_config(page_title="Technology Survey Capstone", page_icon="📊", layout="wide")


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=str(BASE_DIR), text=True, capture_output=True)


def csv_files() -> list[Path]:
    return sorted(DATA_DIR.rglob("*.csv"))


def asset_files() -> list[Path]:
    return sorted(path for path in ASSETS_DIR.glob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"})


def report_files() -> list[Path]:
    return sorted(path for path in REPORTS_DIR.glob("*") if path.suffix.lower() in {".pdf", ".pptx"})


def show_result(result: subprocess.CompletedProcess[str]) -> None:
    output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
    if result.returncode == 0:
        st.success("Command completed successfully.")
    else:
        st.error(f"Command failed with exit code {result.returncode}.")
    if output:
        st.code(output, language="text")


st.title("Technology Survey Capstone")
st.caption("Clean local package with validated data, summary outputs, reports, and assets.")
tabs = st.tabs(["Overview", "Actions", "Data", "Reports", "Assets"])

with tabs[0]:
    st.markdown("- Terminal launcher: `python main.py --validate` or `python main.py --summary`")
    st.markdown("- Browser launcher: `streamlit run app.py`")
    st.markdown("- Workflow scripts are preserved in `/scripts` with descriptive production-style filenames.")

with tabs[1]:
    action = st.selectbox("Choose an action", ["validate", "summary"])
    if st.button("Run action", type="primary"):
        show_result(run_command("main.py", f"--{action}"))

with tabs[2]:
    files = csv_files()
    selected = st.selectbox("Choose a CSV file", files, format_func=lambda p: str(p.relative_to(BASE_DIR)))
    rows = st.slider("Rows to preview", 5, 100, 20, 5)
    df = pd.read_csv(selected)
    st.caption(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
    st.dataframe(df.head(rows), use_container_width=True)

with tabs[3]:
    for report in report_files():
        st.markdown(f"**{report.name}**")
        with report.open("rb") as fh:
            st.download_button(f"Download {report.name}", fh.read(), file_name=report.name, key=report.name)

with tabs[4]:
    for asset in asset_files():
        st.markdown(f"**{asset.name}**")
        st.image(str(asset), use_container_width=True)
