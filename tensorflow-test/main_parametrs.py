import nn_model as m
import time
from datetime import timedelta
import optuna
import os
from pathlib import Path


def play_music():
    music_path = Path('music.mp3')
    os.system("start {}".format(music_path.absolute()))


def objective(trial):
    conv_factor = trial.suggest_int("conv_factor", 6, 128)
    dense_base = trial.suggest_int("dense_base", 32, 512)
    return m.train(
        batch_size=5,
        epoch_size=50,
        conv_factor=conv_factor,
        dense_base=dense_base,
    )

prev = time.time()

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=30)

best_params = study.best_params
print(best_params)

diff_time = int(time.time() - prev)
td = timedelta(seconds=diff_time)
print(td)

play_music()