from pathlib import Path
import numpy as np
import cv2 as cv
from file_storage import model
from numba import cuda
from tensorflow import keras
import constant

input_data = np.load('data/predict_input.npy')
folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

cuda.select_device(0)
cuda.close()

model = keras.models.load_model('out')
result_list = model.predict(input_data)

l = result_list.shape[0]
for i in range(l):
    result = result_list[i]
    index = i + 1
    result = list(zip(*(iter(result),) * 2))
    result_predict = [[int(item[0]), int(item[1])] for item in result][0:4]
    key = 'predict'
    storage.update_metadata_by_index(index, (key, result_predict))
    print('{} from {}'.format(i, l-1))
