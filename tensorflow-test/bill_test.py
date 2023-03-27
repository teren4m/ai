import numpy as np
import tensorflow as tf

from tensorflow.keras import datasets, layers, models, activations
import matplotlib.pyplot as plt
from model_profiler import model_profiler
import pathlib
from pathlib import Path
import cv2 as cv
import json
import pandas as pd
import nvidia_smi
from numba import cuda

cuda.select_device(0)
cuda.close()

nvidia_smi.nvmlInit()





def flatten(l):
    return [item for sublist in l for item in sublist]


def get_txt_data(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8") as f:
        result: list = json.loads(f.readline())
        return np.array(flatten(result))


p = pathlib.Path('../../openCV_python/data/out/resized_frames/resized')
txt_files = list(p.glob('*.txt'))
img_files = [item.parent.resolve() / item.stem for item in txt_files]
txt_files[0].stem
image = txt_files[0].parent.resolve() / txt_files[0].stem

img_count = len(txt_files)
img_shape = cv.imread(str(image)).shape

txt_shape = get_txt_data(txt_files[0]).shape

input_shape = (img_count, *img_shape)
output_shape = (img_count, *txt_shape)
input_data = np.zeros(input_shape)
output_data = np.zeros(output_shape)
data = []

for i in range(len(img_files)):
    input_data[i] = cv.imread(str(img_files[i]))
    output_data[i] = get_txt_data(txt_files[i])

print('input shape')
print(input_shape)
print()
print('output shape')
print(output_shape)


def load_data():
    train_images = input_data[0:154]
    train_labels = output_data[0:154]

    test_images = input_data[154:254]
    test_labels = output_data[154:254]

    return (train_images, train_labels), (test_images, test_labels)



(train_images, train_labels), (test_images, test_labels) = load_data()

model = models.Sequential()
model.add(layers.Input((118, 80, 3)))
# model.add(layers.Conv2D(32, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(32, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(32, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.ReLU())
model.add(layers.Dense(15000))
model.add(layers.ReLU())
model.add(layers.Dense(15000))
model.add(layers.Dense(8))

print(model.summary())

# from model_profiler import model_profiler

Batch_size = 10
profile = model_profiler(model, Batch_size)

print(profile)


# handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
# # card id 0 hardcoded here, there is also a call to get all available card ids, so we could iterate

# info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
# print("Total memory:", info.total / 1024 / 1024 / 1024)
# print("Free memory:", info.free / 1024 / 1024 / 1024)
# print("Used memory:", info.used / 1024 / 1024 / 1024)

# nvidia_smi.nvmlShutdown()

model.compile(optimizer='adam',
              loss="mae",)

history = model.fit(
    train_images, train_labels, 
    epochs=100, 
    batch_size=10,
    validation_data=(test_images, test_labels)
    )

history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss']].plot();
print("Minimum validation loss: {}".format(history_df['val_loss'].min()))