from ui.img import start_ui
from file_storage import file_storage as fs
import constant
from pathlib import Path

def on_save(item):
    print(item)

images = fs.get_img_by_key(constant.resized_key)

img_data = []
l = len(images)
for i in range(l):
    is_mark_exist = 'mark' in images[i].metadata.keys()
    mark = images[i].metadata['mark'] if is_mark_exist else images[i].metadata['predict']
    img_data.append((Path(images[i].path), images[i].metadata['predict'], mark, is_mark_exist, i))

start_ui(img_data, on_save)