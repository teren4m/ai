from pathlib import Path
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from numba import cuda
from tensorflow import keras

input_data = np.load('out/input_data.npy')

cuda.select_device(0)
cuda.close()

model = keras.models.load_model('out')
result = model.predict(input_data)
print(result[0])