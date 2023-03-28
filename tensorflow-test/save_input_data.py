from pathlib import Path
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from numba import cuda
from tensorflow import keras
import json
import time

images_folder = Path('../../openCV_python/data/out/resized_frames_predict')
images_path = list(images_folder.glob('*.png'))
factor = 20
input_shape = (59, 40, 3)
input_shape = (len(images_path), *input_shape)
input_data = np.zeros(input_shape)


def plot_img(img: np.ndarray) -> None:
    plt.figure(figsize=(20, 6))
    plt.imshow(img)
    plt.show()


def resize_img(path: str) -> np.ndarray:
    img = cv.imread(str(path), cv.IMREAD_UNCHANGED)

    width = img.shape[1]
    height = img.shape[0]

    resized_width = int(width / factor)
    resized_height = int(height / factor)
    dim = (resized_width, resized_height)

    # resize image
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    # blank_image = cv.cvtColor(blank_image, cv.COLOR_BGR2GRAY)
    # plot_img(gray)
    return resized


l = len(images_path)
for i in range(l):
    p = images_path[i]
    img_index = int(p.stem)
    img = resize_img(p)
    input_data[img_index] = img
    print('{} from {} index {}'.format(i, l - 1, img_index))

array_file = 'out/input_data'
np.save(array_file, input_data, allow_pickle=False)
