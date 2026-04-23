import pandas as pd

# Local dataset path used by the original notebook.
file_name = "survey_data.csv"

df = pd.read_csv(file_name)

# Find duplicate rows.
duplicates = df.duplicated()

# Count duplicate rows.
duplicate_count = duplicates.sum()

# Display duplicate summary.
print("Duplicate rows:", duplicate_count)
print(df[duplicates].head())
