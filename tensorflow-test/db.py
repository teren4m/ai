import sqlite3
import db.sql_queries as sq
from pathlib import Path

folder = Path('/files_storage')
info_file = folder / 'info.txt'

txt = info_file.read_text()
print(txt)

# con = sqlite3.connect("db/tutorial.db")

# cur = con.cursor()
# cur.execute(sq.create_table())
