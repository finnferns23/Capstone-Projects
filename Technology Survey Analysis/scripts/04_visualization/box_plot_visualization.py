import matplotlib.pyplot as plt
import pandas as pd
import sqlite3





# Connect to the SQLite database
conn = sqlite3.connect('survey-results-public.sqlite')

QUERY = "SELECT COUNT(*) FROM main"
df = pd.read_sql_query(QUERY, conn)
print(df)

QUERY = """
SELECT name as Table_Name 
FROM sqlite_master 
WHERE type = 'table'
"""
pd.read_sql_query(QUERY, conn)

QUERY = """
SELECT Age, COUNT(*) as count 
FROM main 
GROUP BY Age 
ORDER BY Age
"""
df_age = pd.read_sql_query(QUERY, conn)
print(df_age)

# your code goes here

# your code goes here

# your code goes here
# your code goes here
# your code goes here
# your code goes here
# your code goes here
# your code goes here
conn.close()