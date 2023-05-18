import nn_predict as p
import nn_model as m
import nn_train as t
from pathlib import Path
from file_storage import model
import constant
import os
import time
from datetime import timedelta
import winsound

def play_music():
    music_path = Path('music.mp3')
    os.system("start {}".format(music_path.absolute()))

prev = time.time()

folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

images = storage.get_info_by_key()


# t.save_train_data(images)
# t.save_predict_data(images)

m.train(
    batch_size=160,
    epoch_size=10000,
    conv_factor=512,
    dense_base=1024,
    sma=50,
    remove = 100,
)

p.predict(storage)


winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
# play_music()

diff_time = int(time.time() - prev)
td = timedelta(seconds=diff_time)
print(td)