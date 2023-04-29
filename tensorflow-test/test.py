from file_storage import file_storage as fs
import numpy as np
from file_storage import model
from pathlib import Path
import constant

folder = Path('/files_storage')
storage = model.DBHelper(str(folder / 'file_info.db'), constant.resized_key)
storage.init()

storage.cur.execute(
    '''
        SELECT *
        FROM sqlite_sequence
        WHERE name = 'resized'
    '''
    )
all = storage.cur.fetchall()
print(all)

storage.cur.execute(
    '''
        SELECT MAX(id)
        FROM resized
    '''
    )

max = storage.cur.fetchall()

print(max)

# update = '''
#     UPDATE 
#         sqlite_sequence
#     SET 
#         name = 24874
#     WHERE 
#         name = 'resized';
# '''

# storage.cur.execute(update)
# storage.con.commit()

# delete = '''
#     DELETE FROM resized
#     WHERE id > 24874;
# '''
# storage.cur.execute(delete)
# storage.con.commit()

