from ui.img import start_ui
from file_storage import model
import constant
from pathlib import Path
import random

import tensorflow as tf


folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

def on_save_mark(item):
    storage.update_metadata(
        name=item[-2],
        entry=('mark', item[2]),
    )

def on_save_predict_as_mark(item):
    pred = item[-1]['predict']
    storage.update_metadata(
        name=item[-2],
        entry=('mark', pred),
    )

def on_save_good(item):
    storage.update_metadata(
        name=item[-2],
        entry=('condition', 'good'),
    )

def on_save_bad(item):
    storage.update_metadata(
        name=item[-2],
        entry=('condition', 'bad'),
    )

def on_save(item):
    print(item)
    on_save_mark(item)
    

images = storage.get_info_by_key()
# images = [i for i in images if 'mark' in i.metadata.keys()]
l = len(images)
# for img in images:
#     if 'mark' in img.metadata.keys():
#         error = tf.keras.metrics.mean_absolute_error(img.metadata['mark'], img.metadata['predict'])
#         img.metadata['error'] = error.numpy()

# images_shuffle = []

# for i in range(l):
#     index = random.randrange(len(images))
#     images_shuffle.append(images.pop(index))

# images = images_shuffle

# images = [img for img in images if 'condition' in img.metadata.keys() and img.metadata['condition'] == 'bad']
# images = [img for img in images if 'condition' not in img.metadata.keys()]
# images = [img for img in images if 'mark' not in img.metadata.keys()]
images = [img for img in images if 'epoch' in img.metadata.keys() and 'mark' not in img.metadata.keys()]
# images = [img for img in images if 'mark' in img.metadata.keys()]


l = len(images)
img_data = []
for i in range(l):
    is_mark_exist = 'mark' in images[i].metadata.keys()
    mark = images[i].metadata['mark'] if is_mark_exist else images[i].metadata['predict']
    img_data.append(
        (Path(images[i].path), images[i].metadata['predict'], mark, is_mark_exist, i, images[i].name, images[i].metadata))

start_ui(img_data, on_save)

storage.close()

