from ui.img import start_ui
from file_storage import model
import constant
from pathlib import Path
import random
import json
import add_images as img_util
import numpy as np

index_map_file = Path('data/index_map.txt')
folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

images = storage.get_info_by_key()

mark_images = [item for item in images if 'mark' in item.metadata.keys()]
l = len(mark_images)

mixed_mark_images: list[model.FileInfo] = []
for i in range(l):
    index = random.randrange(len(mark_images))
    mixed_mark_images.append(mark_images.pop(index))


index_map = {}
for i in range(l):
    index_map[i] = mixed_mark_images[i].index

# index_map_file.write_text(
#     json.dumps(index_map, indent=4)
# )

img: np.ndarray = img_util.resize_img_predict(
    mixed_mark_images[0].path, constant.factor)

shape = (l, *img.shape)
train_input = np.zeros(shape)
train_output = np.zeros((l, 8))
for i in range(l):
    img_info = mixed_mark_images[i]
    train_input[i] = img_util.resize_img_predict(
        img_info.path, constant.factor)
    mark = img_info.metadata['mark']
    mark_array = []
    [mark_array.extend(item) for item in mark]

    train_output[i] = np.array(mark_array)
    print('{} from {}'.format(i, l - 1))

print(train_input.shape)

np.save('data/train_input', train_input, allow_pickle=False)
np.save('data/train_output', train_output, allow_pickle=False)
