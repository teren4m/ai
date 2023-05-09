import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt
from model_profiler import model_profiler
from pathlib import Path
import json
import pandas as pd
import os

test_len = 8


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_txt_data(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8") as f:
        result: list = json.loads(f.readline())
        return np.array(flatten(result))


def create_model(
    input_shape,
    labels_shape,
    dense_base,
    conv_factor,
):
    normalization = tf.keras.layers.Normalization(axis=None)
    normalization.adapt([0, 255.0])

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Input((79, 53)))
    model.add(normalization)

    model.add(tf.keras.layers.Conv1D(conv_factor, 8, activation='relu'))
    model.add(tf.keras.layers.MaxPooling1D(
        pool_size=7, strides=1, padding='valid'))

    model.add(tf.keras.layers.Conv1D(
        conv_factor * 2, 4, activation='relu'))
    model.add(tf.keras.layers.MaxPooling1D(
        pool_size=7, strides=1, padding='valid'))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(int(dense_base / 25), 'relu'))
    model.add(tf.keras.layers.Dense(dense_base, 'relu'))
    model.add(tf.keras.layers.Dense(82))

    model.summary()
    return model


def train_model(
    batch_size=90,
    epoch_size=3500,
    conv_factor=8,
    dense_base=1000,
):
    X: np.ndarray = np.load('data/train_input.npy')
    y: np.ndarray = np.load('data/train_output.npy')
    input_shape = X.shape[1:]
    output_shape = y.shape[1:][0]

    print()
    print('input shape: {}'.format(input_shape))
    print('output shape: {}'.format(output_shape))
    print()

    dataset = tf.data.Dataset.from_tensor_slices((X, y)).shuffle(
        buffer_size=100000,
        reshuffle_each_iteration=True,
    ).batch(batch_size)

    train_ds, test_ds = tf.keras.utils.split_dataset(dataset, left_size=0.75)

    model = create_model(input_shape, output_shape, dense_base, conv_factor)
    model.compile(optimizer='adam',
                  loss="mae",)

    history = model.fit(
        x=train_ds,
        epochs=epoch_size,
        validation_data=test_ds,
        verbose=1,
    )
    model.save('out')
    return history


def plot_train(sma, history):
    figsize = (20, 10)
    history: dict = history.history
    loss = history['loss']
    val_loss = history['val_loss']
    l = int(len(loss) / 8)
    history['loss'] = loss[l:]
    history['val_loss'] = val_loss[l:]
    history_df = pd.DataFrame(history)
    X = list(range(len(history_df)))
    a = history_df.loss
    b = history_df.val_loss
    c = history_df.loss = history_df.loss.rolling(sma).mean()
    d = history_df.val_loss = history_df.val_loss.rolling(sma).mean()

    plt.figure(figsize=figsize)
    plt.plot(X, a, color='r')
    plt.plot(X, b, color='b')
    plt.plot(X, c, color='k')
    plt.plot(X, d, color='k')
    plt.grid()
    plt.savefig('train.png')
    train_mae_file_path = Path('train.png')
    os.system("start {}".format(train_mae_file_path.absolute()))


def train(
    batch_size,
    epoch_size,
    conv_factor,
    dense_base,
    sma,
):
    history = train_model(batch_size, epoch_size, conv_factor, dense_base)
    plot_train(sma, history)
