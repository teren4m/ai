from tensorflow import keras
import pathlib
import cv2 as cv
import numpy as np
from numba import cuda

cuda.select_device(0)
cuda.close()

p = pathlib.Path('../../openCV_python/data/out/resized_frames/resized/20230317_152242-43_frame_raw.png')
img = cv.imread(str(p))
input_shape = (1, *img.shape)
input_data = np.zeros(input_shape)
input_data[0] = img
model = keras.models.load_model('out')
result = model.predict(input_data)
result = [int(item * 20) for item in result[0]]
print('------------------------------------------------')
print(result)
result = list(zip(*(iter(result),) * 2))
result = [list(item) for item in result]
print('------------------------------------------------')
print(result)
print('------------------------------------------------')