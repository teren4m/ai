from ui.img import start_ui
from file_storage import model
import constant
from pathlib import Path

folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

def on_save(item):
    print(item)
    storage.update_metadata(
        index=item[4],
        key=constant.resized_key,
        entry=('mark', item[2]),
    )


images = storage.get_info_by_key(constant.resized_key)

img_data = []
l = len(images)
for i in range(l):
    is_mark_exist = 'mark' in images[i].metadata.keys()
    mark = images[i].metadata['mark'] if is_mark_exist else images[i].metadata['predict']
    img_data.append(
        (Path(images[i].path), images[i].metadata['predict'], mark, is_mark_exist, i))

start_ui(img_data, on_save)

storage.update()
