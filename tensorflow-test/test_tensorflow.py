from tensorflow import keras
from keras import layers
import tensorflow as tf

# Create a network with 1 linear unit
model = keras.Sequential([
    layers.Dense(units=1, input_shape=[3])
])