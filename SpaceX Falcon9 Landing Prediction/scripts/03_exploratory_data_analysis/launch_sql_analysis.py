"""Run representative SQL-style queries against the packaged SpaceX dataset."""

from __future__ import annotations

import sqlite3

import pandas as pd

from project_paths import DOCS_DIR, RAW_DATA_DIR, ensure_directories, find_data_file

OUTPUT_DB = RAW_DATA_DIR / "spacex_launch_data.sqlite"
OUTPUT_TXT = DOCS_DIR / "sql_analysis_results.txt"

QUERIES = {
    "distinct_launch_sites": "SELECT DISTINCT Launch_Site FROM SPACEXTBL",
    "nasa_crs_payload_sum": "SELECT SUM(PAYLOAD_MASS__KG_) AS total_payload_kg FROM SPACEXTBL WHERE Payload LIKE 'CRS%'",
    "f9_v11_avg_payload": "SELECT AVG(PAYLOAD_MASS__KG_) AS avg_payload_kg FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'",
    "mission_outcome_counts": "SELECT Mission_Outcome, COUNT(*) AS count FROM SPACEXTBL GROUP BY Mission_Outcome ORDER BY count DESC",
}


def main() -> None:
    ensure_directories()
    csv_path = find_data_file("spacex_sql_dataset.csv")
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(OUTPUT_DB)
    df.to_sql("SPACEXTBL", conn, if_exists="replace", index=False)

    lines = ["SpaceX SQL Query Results", ""]
    for name, query in QUERIES.items():
        result = pd.read_sql_query(query, conn)
        lines.append(f"--- {name} ---")
        lines.append(result.to_string(index=False))
        lines.append("")
        print(f"\n--- {name} ---")
        print(result)

    conn.close()
    OUTPUT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved query results to {OUTPUT_TXT}")


if __name__ == "__main__":
    main()
