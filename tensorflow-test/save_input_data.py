import numpy as np
import file_storage.file_storage as fs
import constant
import cv2 as cv

images = fs.get_img_by_key(constant.resized_predict_key)
img = cv.imread(images[0].path, cv.IMREAD_UNCHANGED)
l = len(images)
shape = (l, *img.shape)
input_data = np.zeros(shape)

for i in range(l):
    file_info = images[i]
    path = file_info.path
    img_index = file_info.index
    img = cv.imread(path, cv.IMREAD_UNCHANGED)
    input_data[img_index] = img
    print('{} from {} index {}'.format(i, l - 1, img_index))

array_file = 'out/input_data'
np.save(array_file, input_data, allow_pickle=False)
