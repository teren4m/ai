from pathlib import Path
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from numba import cuda
from tensorflow import keras

input_data_file = np.load('out/input_data')

cuda.select_device(0)
cuda.close()

input_data_file
# result = model.predict(input_data)
# for result 
# print(result[0])