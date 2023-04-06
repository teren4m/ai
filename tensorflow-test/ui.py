from ui.img import start_ui
from file_storage import model
import constant
from pathlib import Path
import random


folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

def on_save(item):
    print(item)
    storage.update_metadata(
        name=item[-1],
        entry=('mark', item[2]),
    )


images = storage.get_info_by_key()

l = len(images)
images_shuffle = []

for i in range(l):
    index = random.randrange(len(images))
    images_shuffle.append(images.pop(index))

images = images_shuffle

# images = images[0:1]
# print(images)
# l = len(images)

img_data = []
for i in range(l):
    is_mark_exist = 'mark' in images[i].metadata.keys()
    mark = images[i].metadata['mark'] if is_mark_exist else images[i].metadata['predict']
    img_data.append(
        (Path(images[i].path), images[i].metadata['predict'], mark, is_mark_exist, i, images[i].name))

start_ui(img_data, on_save)

storage.close()
