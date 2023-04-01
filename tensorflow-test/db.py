import sqlite3
import db.sql_queries as sq
from pathlib import Path

sql_query = """SELECT name FROM sqlite_master  
  WHERE type='table';"""

folder = Path('/files_storage')
info_file = folder / 'info.txt'

txt = info_file.read_text()
# print(txt)

con = sqlite3.connect("db/tutorial.db")

cur = con.cursor()
cur.execute(sql_query)
print(cur.fetchall())
