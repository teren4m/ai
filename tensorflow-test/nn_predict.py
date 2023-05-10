import numpy as np
import cv2 as cv
from file_storage import model
from numba import cuda
from tensorflow import keras

def denormalize(x, max):
    std = np.std([0, max])
    mean = np.mean([0, max])
    return x * std + mean

def predict(storage: model.Storage):
    print('')
    input_data = np.load('data/predict_input.npy')

    model = keras.models.load_model('out')
    result_list = model.predict(input_data)
    print(result_list)
    l = result_list.shape[0]
    for i in range(l):
        result = result_list[i]
        index = i + 1
        result = list(zip(*(iter(result),) * 2))
        result_predict = [[int(denormalize(item[0], 800)), int(denormalize(item[1], 1188))] for item in result][0:4]
        key = 'predict'
        storage.update_metadata_by_index(index, (key, result_predict))
        print('{} predict from {}'.format(i, l-1), end="\r")

