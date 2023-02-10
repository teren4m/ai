import json
from datetime import datetime
from time import gmtime, strftime
import os


def create_file(file):
    if not os.path.isfile(file):
        with open(file, "w") as write:
            json.dump({}, write)


def get_data(num):
    return {
        'time': get_time_now(),
        'num': num,
    }


def get_time_now():
    now = datetime.now()
    return now.strftime("%d %b %Y %H:%M:%S.%f")


def save_result(data, file):
    with open(file, "w") as write:
        json.dump(data, write)


def get_results(file):
    data = open(file)
    return json.load(data)


def statistics(data: dict):
    vals = [item['num'] for item in list(data.values())]
    prev = None if len(vals) == 1 else vals[-2]
    curr = vals[-1]
    best = min(vals)
    return {
        'prev': prev,
        'curr': curr,
        'best': best,
    }


def result(num, file):
    create_file(file)
    data: dict = get_results(file)
    keys = data.keys()
    index = 1 if len(keys) == 0 else int(max(keys)) + 1
    data[index] = get_data(num)
    save_result(data, file)
    return statistics(data)
