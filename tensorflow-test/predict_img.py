from pathlib import Path
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from numba import cuda
from tensorflow import keras
from file_storage import file_storage as fs
import constant

input_data = np.load('out/input_data.npy')

cuda.select_device(0)
cuda.close()

model = keras.models.load_model('out')
result_list = model.predict(input_data)

l = result_list.shape[0]
for i in range(l):
    result = result_list[i]
    result = list(zip(*(iter(result),) * 2))
    result_predict = [[int(item[0]), int(item[1])] for item in result]
    result_resized = [[int(item[0] * constant.factor),
                       int(item[1] * constant.factor)] for item in result]
    predict_info = fs.get_info_by_key_index(constant.resized_predict_key, i)
    predict_info.metadata['predict'] = result_predict
    resized_info = fs.get_info_by_key_index(constant.resized_key, i)
    resized_info.metadata['predict'] = result_resized
    print('{} from {}'.format(i, l-1))

fs.update()
