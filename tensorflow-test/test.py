import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt
from model_profiler import model_profiler
import pathlib
from pathlib import Path
import cv2 as cv
import json
import pandas as pd
import nvidia_smi
from numba import cuda

adapt_data = np.array([1., 2., 3., 4., 5.], dtype='float32')
input_data = np.array([0,1., 2., 5.,10.], dtype='float32')
layer = tf.keras.layers.Normalization(axis=None)
layer.adapt([0,10])
out = layer(input_data)
print(out)