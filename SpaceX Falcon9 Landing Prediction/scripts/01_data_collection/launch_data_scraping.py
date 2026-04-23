"""Scrape Falcon 9 launch records from Wikipedia for the IBM capstone project."""

from __future__ import annotations

import re
import unicodedata

import pandas as pd
import requests
from bs4 import BeautifulSoup


WIKI_URL = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"


def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    return "".join(
        [value for i, value in enumerate(table_cells.strings) if i % 2 == 0][0:-1]
    )


def landing_status(table_cells):
    return [value for value in table_cells.strings][0]


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        return mass[: mass.find("kg") + 2]
    return "0kg"


def extract_column_from_header(row):
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
    column_name = " ".join(row.stripped_strings)
    return column_name


def main() -> None:
    response = requests.get(WIKI_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    html_tables = soup.find_all("table", "wikitable")

    first_launch_table = None
    for table in html_tables:
        if "Flight No." in table.text:
            first_launch_table = table
            break

    if first_launch_table is None:
        raise ValueError("Could not find the Falcon 9 launch table on Wikipedia.")

    column_names = []
    headers = first_launch_table.find_all("th")
    for header in headers:
        name = extract_column_from_header(header)
        if name and name not in column_names:
            column_names.append(name)

    print("Detected columns:")
    print(column_names)
    print("\nWikipedia table fetched successfully.")


if __name__ == "__main__":
    main()
