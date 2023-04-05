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
        key = 'mark',
        value = '[[84, 245], [233, 390], [151, 689], [114, 323]]'
    WHERE
        name = '0f346758-60b7-46c6-a05c-ec8f0e7979f7' AND key = 'mark'
    '''
)

# db.insert([item.__dict__ for item in images])
# x = db.get_list()
# x = db.get('0001d700-c532-4b1c-88c9-5601561bd87c')
# print(len(x))

# db.close()
