from pathlib import Path
import pandas as pd


pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

csv_path = Path('survey_data_updated.csv')

if not csv_path.exists():
    alt_paths = [
        Path('survey_data_updated 5.csv'),
        Path('/mnt/data/survey_data_updated.csv'),
        Path('/mnt/data/survey_data_updated 5.csv')
    ]
    for path in alt_paths:
        if path.exists():
            csv_path = path
            break

df = pd.read_csv(csv_path)
print(f'Loaded file: {csv_path}')
print(f'Shape: {df.shape}')
df.head()

df.columns.tolist()
def clean_multivalue_series(series: pd.Series) -> pd.Series:
    """Split semicolon-separated values, trim whitespace, drop blanks/nulls."""
    return (
        series.dropna()
        .astype(str)
        .str.split(';')
        .explode()
        .str.strip()
        .replace('', pd.NA)
        .dropna()
    )


def get_top_10_multivalue(df: pd.DataFrame, column: str, label_name: str) -> pd.DataFrame:
    cleaned = clean_multivalue_series(df[column])
    result = (
        cleaned.value_counts()
        .head(10)
        .rename_axis(label_name)
        .reset_index(name='Count')
    )
    return result


def get_single_value_counts(df: pd.DataFrame, column: str, label_name: str, top_n=None) -> pd.DataFrame:
    result = (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
        .replace('', pd.NA)
        .dropna()
        .value_counts()
    )
    if top_n is not None:
        result = result.head(top_n)
    return result.rename_axis(label_name).reset_index(name='Count')


def export_csv(dataframe: pd.DataFrame, filename: str) -> None:
    dataframe.to_csv(filename, index=False)
    print(f'Saved: {filename}')

lang_current = get_top_10_multivalue(df, 'LanguageHaveWorkedWith', 'Language')
db_current = get_top_10_multivalue(df, 'DatabaseHaveWorkedWith', 'Database')
platform_current = get_top_10_multivalue(df, 'PlatformHaveWorkedWith', 'Platform')
framework_current = get_top_10_multivalue(df, 'WebFrameHaveWorkedWith', 'Web Framework')

print('Top 10 Languages Used')
display(lang_current)

print('Top 10 Databases Used')
display(db_current)

print('Top 10 Platforms Used')
display(platform_current)

print('Top 10 Web Frameworks Used')
display(framework_current)

lang_future = get_top_10_multivalue(df, 'LanguageWantToWorkWith', 'Language')
db_future = get_top_10_multivalue(df, 'DatabaseWantToWorkWith', 'Database')
platform_future = get_top_10_multivalue(df, 'PlatformWantToWorkWith', 'Platform')
framework_future = get_top_10_multivalue(df, 'WebFrameWantToWorkWith', 'Web Framework')

print('Top 10 Languages Desired Next Year')
display(lang_future)

print('Top 10 Databases Desired Next Year')
display(db_future)

print('Top 10 Desired Platforms')
display(platform_future)

print('Top 10 Desired Web Frameworks')
display(framework_future)

age_dist = get_single_value_counts(df, 'Age', 'Age')
country_dist = get_single_value_counts(df, 'Country', 'Country')
edu_dist = get_single_value_counts(df, 'EdLevel', 'Education Level')

age_edu = (
    df[['Age', 'EdLevel']]
    .dropna()
    .assign(
        Age=lambda x: x['Age'].astype(str).str.strip(),
        EdLevel=lambda x: x['EdLevel'].astype(str).str.strip()
    )
)

age_edu = (
    age_edu[(age_edu['Age'] != '') & (age_edu['EdLevel'] != '')]
    .groupby(['Age', 'EdLevel'])
    .size()
    .reset_index(name='Count')
)

print('Respondents by Age')
display(age_dist)

print('Respondent Count by Country')
display(country_dist.head(20))

print('Respondent Distribution by Education Level')
display(edu_dist)

print('Respondent Count by Age and Education Level')
display(age_edu.head(20))

# Current Technology Usage
export_csv(lang_current, 'lang_current.csv')
export_csv(db_current, 'db_current.csv')
export_csv(platform_current, 'platform_current.csv')
export_csv(framework_current, 'framework_current.csv')

# Future Technology Trends
export_csv(lang_future, 'lang_future.csv')
export_csv(db_future, 'db_future.csv')
export_csv(platform_future, 'platform_future.csv')
export_csv(framework_future, 'framework_future.csv')

# Demographics
export_csv(age_dist, 'age_dist.csv')
export_csv(country_dist, 'country_dist.csv')
export_csv(edu_dist, 'edu_dist.csv')
export_csv(age_edu, 'age_edu.csv')

dashboard_mapping = pd.DataFrame({
    'Dashboard Tab': [
        'Current Technology Usage', 'Current Technology Usage', 'Current Technology Usage', 'Current Technology Usage',
        'Future Technology Trends', 'Future Technology Trends', 'Future Technology Trends', 'Future Technology Trends',
        'Demographics', 'Demographics', 'Demographics', 'Demographics'
    ],
    'Panel': [
        'Panel 1', 'Panel 2', 'Panel 3', 'Panel 4',
        'Panel 1', 'Panel 2', 'Panel 3', 'Panel 4',
        'Panel 1', 'Panel 2', 'Panel 3', 'Panel 4'
    ],
    'Chart Type': [
        'Stacked Bar / Bar', 'Stacked Column / Column', 'Word Cloud', 'Scatter Bubble / Hierarchy Bubble',
        'Stacked Bar / Bar', 'Stacked Column / Column', 'Tree Map', 'Scatter Bubble / Hierarchy Bubble',
        'Pie Chart', 'Map Chart', 'Line / Line Bar Chart', 'Stacked Bar Chart'
    ],
    'Input CSV': [
        'lang_current.csv', 'db_current.csv', 'platform_current.csv', 'framework_current.csv',
        'lang_future.csv', 'db_future.csv', 'platform_future.csv', 'framework_future.csv',
        'age_dist.csv', 'country_dist.csv', 'edu_dist.csv', 'age_edu.csv'
    ]
})

dashboard_mapping

generated_files = [
    'lang_current.csv', 'db_current.csv', 'platform_current.csv', 'framework_current.csv',
    'lang_future.csv', 'db_future.csv', 'platform_future.csv', 'framework_future.csv',
    'age_dist.csv', 'country_dist.csv', 'edu_dist.csv', 'age_edu.csv'
]

status = pd.DataFrame({
    'File': generated_files,
    'Exists': [Path(file).exists() for file in generated_files]
})

status
