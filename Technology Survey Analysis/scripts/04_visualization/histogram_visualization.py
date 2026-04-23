import matplotlib.pyplot as plt
import pandas as pd
import sqlite3




conn = sqlite3.connect('survey-data.sqlite')
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

## Write your code here
## Write your code here
## Write your code here
## Write your code here
## Write your code here
## Write your code here
## Write your code here
## Write your code here
conn.close()