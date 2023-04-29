from ui.img import start_ui
from file_storage import model
import constant
from pathlib import Path
import random
import add_images as img_util
import numpy as np
import math

point_count = 66

def center(line):
    x1 = line[0][0]
    x2 = line[1][0]
    y1 = line[0][1]
    y2 = line[1][1]
    return [int((x1+x2)/2), int((y1+y2)/2)]

def get_lines(points):
    l = len(points)
    last_index = l - 1
    lines = []
    for i in range(l):
        if i == last_index:
            lines.append((points[i], points[0]))
        else:
            lines.append((points[i], points[i + 1]))
    return lines

def merge_points(x:list,y:list):
    all_points = []
    [all_points.extend(line) for line in zip(x, y)]
    return all_points

def add_points(points):
    lines = get_lines(points)
    center_points = [center(line) for line in lines]
    return merge_points(points, center_points)

def extend_by_point(center, point):
    if point == [0,0]:
        return [0,0]
    x1 = center[0]
    y1 = center[1]

    x2 = point[0]
    y2 = point[1]

    v = [x2-x1, y2-y1]

    v_l = math.sqrt(v[0]**2 + v[1]**2)
    v_norm = [v[0]/v_l, v[1]/v_l]
    dist = v_l + 10
    x= int(v_norm[0] * dist + x1)
    y = int(v_norm[1] * dist + y1)
    return [x,y]
        
def extend_by_points(center, points):
    return [extend_by_point(center, x) for x in points]

def center_of_lines(points):
    all_points = add_points(points)

    center_of_points = (
        int((all_points[3][0] + all_points[7][0])/2),
        int((all_points[3][1] + all_points[7][1])/2),
    )

    # all_points = add_points(all_points)
    # all_points = add_points(all_points)
    # all_points = add_points(all_points)

    mid_points = [center((point, center_of_points)) for point in all_points]

    mid2_points = [center(line) for line in zip(all_points, mid_points)]

    mid3_points = [center(line) for line in zip(all_points, mid2_points)]

    extended = [[p[0],p[1]] for p in extend_by_points(center_of_points, all_points)]

    return [*points, *extended, *all_points, *mid3_points, center_of_points]

def extend_points(points):
    return center_of_lines(points)

folder = Path('/files_storage')
storage = model.Storage(folder, constant.resized_key)
storage.init()

images = storage.get_info_by_key()

mark_images = [item for item in images if 'mark' in item.metadata.keys()]
l = len(mark_images)

mixed_mark_images: list[model.FileInfo] = []
for i in range(l):
    index = random.randrange(len(mark_images))
    mixed_mark_images.append(mark_images.pop(index))

img: np.ndarray = img_util.resize_img_predict(
    mixed_mark_images[0].path, constant.factor)

shape = (l, *img.shape)
train_input = np.zeros(shape)
train_output = np.zeros((l, point_count))
for i in range(l):
    img_info = mixed_mark_images[i]
    # print(img_info.name)
    # print(img_info.id)
    # print(img_info.metadata)
    train_input[i] = img_util.resize_img_predict(
        img_info.path, constant.factor)
    mark = img_info.metadata['mark']

    extended_marks = [*mark, *extend_points(mark)]

    mark_array = []
    [mark_array.extend(item) for item in extended_marks]

    train_output[i] = np.array(mark_array)
    print('{} from {}'.format(i, l - 1))

l = len(images)
predict_input_shape = (l, *img.shape)
predict_input = np.zeros(predict_input_shape)
# for i in range(l):
#     img_info = images[i]
#     index = img_info.id - 1
#     predict_input[index] = img_util.resize_img_predict(
#             img_info.path, constant.factor)
#     print('{} index {}'.format(i, l-1))

print(predict_input_shape)
print(train_input.shape)

# np.save('data/predict_input', predict_input, allow_pickle=False)
np.save('data/train_input', train_input, allow_pickle=False)
np.save('data/train_output', train_output, allow_pickle=False)
