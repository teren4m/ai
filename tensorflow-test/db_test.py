from pathlib import Path
from file_storage.model import Storage, FileInfo
import constant
from file_storage.db import DBHelper

folder = Path('/files_storage')
db_file = str(folder / 'file_info.db')
# storage = Storage(folder, constant.resized_key)
# storage.init()


# def is_mark(x: FileInfo):
#     metadata: dict = x.metadata
#     return 'mark' in metadata.keys()


# images = storage.get_info_by_key(constant.resized_key)
# marked = list(filter(is_mark, images))
# l = len(marked)
# print(marked[0].__dict__)

db = DBHelper(db_file, constant.resized_key)
db.init()
db.update(
    '''
    UPDATE
        resized_metadata
    SET
        key = 'predict',
        value = '[[146, 336], [199, 363], [148, 476], [91, 444]]'
    WHERE
        name = (SELECT name FROM resized WHERE id=1) AND key = 'predict'
    '''
)

# db.insert([item.__dict__ for item in images])
# x = db.get_list()
# x = db.get('0001d700-c532-4b1c-88c9-5601561bd87c')
# print(len(x))

# db.close()
