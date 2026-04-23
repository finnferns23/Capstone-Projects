# Technology Survey Capstone

## Overview

This project is a cleaned and GitHub-ready local package for the IBM Technology Survey capstone. It is structured for easy extraction, local validation, browser viewing, and GitHub upload. The package preserves the original notebook-derived workflow files while providing a cleaner top-level project layout.

## What this project contains

- the packaged survey dataset used in the capstone
- processed CSV outputs for quick review and summary analysis
- preserved notebook-to-Python scripts grouped by workflow stage
- dashboard image assets
- final report deliverables in PDF and PowerPoint format
- a simple terminal launcher through `main.py`
- a browser launcher through `app.py`

## Directory structure

```text
technology_survey_capstone/
├── README.md
├── requirements.txt
├── main.py
├── app.py
├── project_paths.py
├── assets/
│   ├── technology_survey_dashboard.png
│   ├── technology_survey_dashboard_layout.png
│   └── technology_survey_spacex_dashboard_reference.jpeg
├── data/
│   ├── raw/
│   │   └── survey_data.csv
│   └── processed/
│       ├── age_distribution.csv
│       ├── age_by_education.csv
│       ├── country_distribution.csv
│       ├── current_database_distribution.csv
│       ├── future_database_distribution.csv
│       ├── education_distribution.csv
│       ├── current_framework_distribution.csv
│       ├── future_framework_distribution.csv
│       ├── current_language_distribution.csv
│       ├── future_language_distribution.csv
│       ├── current_platform_distribution.csv
│       ├── future_platform_distribution.csv
│       ├── top_countries.csv
│       ├── top_languages.csv
│       └── top_education_levels.csv
├── docs/
│   ├── file_index.txt
│   ├── GENERATED_SUMMARY.txt
│   ├── project_summary.json
│   └── setup_and_github_steps.txt
├── reports/
│   ├── technology_survey_report.pdf
│   └── technology_survey_report.pptx
└── scripts/
    ├── 01_data_collection/
    ├── 02_data_wrangling/
    ├── 03_exploratory_data_analysis/
    ├── 04_visualization/
    └── 05_dashboard/
```

## What each directory does

### `assets/`
Stores dashboard screenshots and related image outputs used for presentation, review, or portfolio display.

### `data/raw/`
Stores the packaged raw survey dataset used by the capstone.

### `data/processed/`
Stores derived CSV outputs and summary files that can be reviewed quickly without rerunning every original notebook stage.

### `docs/`
Stores helper documentation such as the generated summary, file index, and setup notes.

### `reports/`
Stores the final deliverables for submission and presentation.

### `scripts/`
Stores the notebook-derived Python files grouped by stage. These are preserved as reference artifacts from the course workflow. Their filenames remain course-style and verbose by design so the original lab flow is easy to trace.

## Main runnable files

### `main.py`
Use this for local validation and summary generation.

Supported commands:

```bash
python main.py --validate
python main.py --summary
```

### `app.py`
Use this to launch a lightweight Streamlit interface for reviewing data, reports, and assets in the browser.

```bash
streamlit run app.py
```

### `project_paths.py`
Centralizes folder locations used by the launcher files.

## Installation

From Command Prompt or terminal inside the project folder:

```bash
pip install -r requirements.txt
```

## Recommended local validation flow

```bash
python main.py --validate
python main.py --summary
```

## GitHub workflow after extraction

Open Command Prompt in the `technology_survey_capstone` folder and run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Notes

- This package is set up for local use, submission, and portfolio upload.
- The preserved scripts are intentionally kept as reference/source material and not renamed into a tighter production naming convention.
- The project validation command was run successfully before this final zip was created.
