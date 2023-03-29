import file_storage.file_storage as fs
from file_storage.model import FileInfo
from pathlib import Path
import cv2 as cv
import constant
import numpy as np


video_path = Path('../../openCV_python/data/video')


def resize_img(path: str):
    path = str(path)
    img = cv.imread(path, cv.IMREAD_UNCHANGED)

    width = img.shape[1]
    height = img.shape[0]

    if height < width:
        img = np.rot90(img, k=1, axes=(0, 1))

    width = img.shape[1]
    height = img.shape[0]

    resized_width = 500
    factor = resized_width / width
    resized_height = int(height * factor)
    dim = (resized_width, resized_height)

    # resize image
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    padding = 150
    blank_height = resized_height + padding * 2
    blank_width = resized_width + padding * 2
    blank_image = np.zeros((blank_height, blank_width, 3), np.uint8)
    blank_image[:, :] = (0, 0, 0)      # (B, G, R)

    w_start = padding
    w_end = resized_width + padding
    h_start = padding
    h_end = resized_height + padding
    blank_image[h_start:h_end, w_start:w_end] = resized

    # blank_image = cv.cvtColor(blank_image, cv.COLOR_BGR2GRAY)
    # plot_img(gray)
    return blank_image


def load_original():
    img_list: list[Path] = [x for x in list(
        video_path.glob(str('**/*.png'))) if x.is_file()]
    l = len(img_list)
    for i in range(l):
        img = cv.imread(str(img_list[i]), cv.IMREAD_UNCHANGED)
        fs.save_img(constant.original_key, i, img)
        print('{} {} from {}'.format(constant.original_key, i, l - 1))


def resize_images():
    original_images: list[FileInfo] = fs.get_img_by_key(constant.original_key)

    l = len(original_images)
    for i in range(l):
        img_info = original_images[i]
        img = resize_img(img_info.path)
        fs.save_img(constant.resized_key, img_info.index, img)
        print(str(i) + ' from ' + str(l - 1))


# load_original()
resize_images()
