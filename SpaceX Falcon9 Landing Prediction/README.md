# SpaceX Falcon 9 Landing Prediction

## Overview

This project is a cleaned and GitHub-ready local package for the IBM Applied Data Science Capstone SpaceX landing prediction work. It is arranged for local execution from Command Prompt, browser review through Streamlit, and straightforward upload to GitHub after extraction.

## What this project contains

- raw and processed SpaceX datasets used across the capstone workflow
- stage-based Python scripts with descriptive workflow names for data collection, wrangling, EDA, SQL, visualization, dashboarding, and machine learning
- generated visual outputs such as charts, model summaries, and the Folium map artifact
- final report deliverables in PDF and PowerPoint format
- a terminal launcher through `main.py`
- a browser launcher through `app.py`

## Directory structure

```text
spacex_falcon9_landing_prediction/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── app.py
├── project_paths.py
├── assets/
│   ├── confusion_matrix.png
│   ├── spacex_dashboard_reference.jpeg
│   ├── model_scores.csv
│   ├── payload_vs_flightnumber.png
│   ├── payload_vs_launchsite.png
│   ├── spacex_launch_sites_map.html
│   ├── success_rate_by_orbit.png
│   └── success_rate_by_year.png
├── data/
│   ├── raw/
│   │   ├── dataset_part_1.csv
│   │   ├── spacex_sql_dataset.csv
│   │   ├── spacex_launch_dash.csv
│   │   ├── spacex_launch_geo.csv
│   │   └── spacex_launch_data.sqlite
│   └── processed/
│       ├── dataset_part_2.csv
│       └── dataset_part_3.csv
├── docs/
│   ├── file_index.txt
│   └── sql_analysis_results.txt
├── reports/
│   ├── spacex_report.pdf
│   └── spacex_report.pptx
└── scripts/
    ├── 01_data_collection/
    ├── 02_data_wrangling/
    ├── 03_exploratory_data_analysis/
    ├── 04_visualization/
    ├── 05_dashboard/
    └── 06_machine_learning/
```

## What each directory does

### `assets/`
Stores generated charts, the model score summary, reference dashboard image, and the Folium map HTML output.

### `data/raw/`
Stores source files used throughout the capstone, including the course CSV files and SQLite database.

### `data/processed/`
Stores cleaned and feature-engineered datasets used in later analysis and modeling stages.

### `docs/`
Stores helper text outputs such as the generated file index and SQL summary notes.

### `reports/`
Stores final deliverables used for submission and presentation.

### `scripts/`
Stores the stage-based Python files grouped in the same order as the capstone workflow.

## Main runnable files

### `main.py`
Use this for validation or stage execution from Command Prompt.

Supported examples:

```bash
python main.py --validate
python main.py --pipeline
python main.py --run ml
python main.py --run eda
```

### `app.py`
Use this to launch a lightweight Streamlit interface for data preview, asset review, and report downloads.

```bash
streamlit run app.py
```

### `project_paths.py`
Centralizes project paths used by the launcher and stage scripts.

## Installation

From Command Prompt or terminal inside the project folder:

```bash
pip install -r requirements.txt
```

## Recommended local validation flow

```bash
python main.py --validate
```

Optional stage execution:

```bash
python main.py --pipeline
```

## GitHub workflow after extraction

Open Command Prompt in the `spacex_falcon9_landing_prediction` folder and run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Notes

- This package is arranged for local use, submission, and portfolio upload.
- Duplicate root-level output files were removed in this final cleanup because the same artifacts already exist in the correct folders.
- The project validation command was run successfully before this final zip was created.
