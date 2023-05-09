from tkinter import Frame, TOP, BOTTOM, CENTER, BOTH, NW, Tk, Event, Canvas, Button, Label
from PIL import ImageTk, Image
from collections import namedtuple
from pathlib import Path
import pyperclip as pc
import math
import json
from typing import Optional


def diff(li1, li2):
    li_dif = [item for item in li1 if item not in li2]
    return li_dif


container_name = 'container'
image_name = 'image'
canvas_name = 'canvas'
widget_name = '.{}.{}.{}'.format(container_name, image_name, canvas_name,)

image_frame: Frame

curent_image_index = 0
Size = namedtuple('Size', "width height bar")
Point = namedtuple('Point', "x y")
Line = namedtuple('Line', 'p1 p2')


def get_current_image():
    global curent_image_index
    global top_label
    global count_label
    global images
    name = img_info[curent_image_index][0]
    top_label.configure(text=name)
    count = len(img_info)
    count_filled = len(list(filter(lambda x: x[3], img_info)))
    count_text = ' from {} filled {}'.format(count, count_filled)
    count_label.configure(text=count_text)
    info_label.configure(
        text='  {} from {}  '.format(curent_image_index, count))
    metadata = img_info[curent_image_index][-1]
    print(metadata)
    return img_info[curent_image_index]


def get_next_image() -> str:
    global curent_image_index
    last_index = len(img_info) - 1
    if curent_image_index == last_index:
        curent_image_index = 0
    else:
        curent_image_index = curent_image_index + 1

    return get_current_image()


def get_prev_image() -> str:
    global curent_image_index
    last_index = len(img_info) - 1
    if curent_image_index == 0:
        curent_image_index = last_index
    else:
        curent_image_index = curent_image_index - 1

    return get_current_image()


class DrawFrame(Frame):

    predict_points: list[Point] = []
    mark_points: list[Point] = []
    track_index: Optional[Point]
    is_index_lock: bool = False
    index: Optional[int]

    def __init__(self, frame, width, height, background,):
        self.padding = 0
        self.width = width
        self.height = height
        self.track_point = None
        self.track_index = None
        super().__init__(
            frame,
            name=image_name,
            width=width + self.padding * 2,
            height=height + self.padding * 2,
            background=background,
        )
        self.initUI()

    def initUI(self):
        self.img_canvas = Canvas(
            self, name=canvas_name, bg='black', width=self.width, height=self.height)
        self.img_canvas.place(x=self.padding, y=self.padding, anchor=NW)

    def zero(self):
        self.mark_points.clear()
        self.mark_points.extend([Point(x=0, y=0), Point(
            x=0, y=0), Point(x=0, y=0), Point(x=0, y=0)])
        self.draw()

    def draw_image(self, data):
        img = Image.open(str(data[0]))
        self.photo_image = ImageTk.PhotoImage(img)
        self.img_canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
        self.predict_points.extend(
            [Point(x=item[0], y=item[1]) for item in data[1]])
        mark_index = 1 if data[2] == None else 2
        self.mark_points.extend([Point(x=item[0], y=item[1])
                                for item in data[mark_index]])
        self.draw()

    def draw_rect(self, points: list[Point], first_point_color: str, color: str, type: str, select_index: int = None, draw_lines=True):
        dot_radius = 2
        dot_radius_selected = 4
        l = len(points)
        if l > 1 and draw_lines:
            for i in range(l):
                if i != 0:
                    prev_point = points[i - 1]
                    curr_point = points[i]
                    self.img_canvas.create_line(
                        prev_point.x, prev_point.y,
                        curr_point.x, curr_point.y,
                        fill=color, width=1, tags=type)
                elif i == 0 and l == 4:
                    prev_point = points[l - 1]
                    curr_point = points[i]
                    self.img_canvas.create_line(
                        prev_point.x, prev_point.y,
                        curr_point.x, curr_point.y,
                        fill=color, width=1, tags=type)
        for i in range(l):
            point = points[i]
            point_color = color if i != 0 else first_point_color
            point_color = 'orange' if i == 1 else point_color
            radius = dot_radius_selected if select_index == i else dot_radius
            self.img_canvas.create_oval(
                point.x - radius,
                point.y - radius,
                point.x + radius,
                point.y + radius,
                fill=point_color, width=0, tags=type)

    def draw(self):
        self.draw_rect(
            self.predict_points,
            'blue',
            'yellow',
            'predict'
        )

        self.draw_rect(
            self.mark_points,
            'green',
            'red',
            'mark',
            select_index=self.track_index,
        )

        def center(line):
            x1 = line[0][0]
            x2 = line[1][0]
            y1 = line[0][1]
            y2 = line[1][1]
            return Point(x=int((x1+x2)/2), y=int((y1+y2)/2),)

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

        def merge_points(x: list, y: list):
            all_points = []
            [all_points.extend(line) for line in zip(x, y)]
            return all_points

        def add_points(points):
            lines = get_lines(points)
            center_points = [center(line) for line in lines]
            return merge_points(points, center_points)
        
        def extend_by_point(center, point):
            if point == (0,0):
                return [0,0]
            if center == (0,0):
                return [0,0]
            x1 = center[0]
            y1 = center[1]

            x2 = point[0]
            y2 = point[1]

            v = [x2-x1, y2-y1]

            v_l = math.sqrt(v[0]**2 + v[1]**2)
            v_norm = [v[0]/v_l,v[1]/v_l]
            dist = v_l + 10
            x= int(v_norm[0] * dist + x1)
            y = int(v_norm[1] * dist + y1)
            return [x,y]
        
        def extend_by_points(center, points):
            return [extend_by_point(center, x) for x in points]

        def center_of_lines(points):
            all_points = add_points(points)

            center_of_points = Point(
                x=int((all_points[3][0] + all_points[7][0])/2),
                y=int((all_points[3][1] + all_points[7][1])/2),
            )

            all_points = add_points(all_points)
            all_points = add_points(all_points)
            # all_points = add_points(all_points)

            # mid_points = [center((point, center_of_points)) for point in all_points]

            # mid2_points = [center(line) for line in zip(all_points, mid_points)]

            # mid3_points = [center(line) for line in zip(all_points, mid2_points)]

            extended = [Point(x=p[0],y=p[1],) for p in extend_by_points(center_of_points, all_points)]

            return [center_of_points]

        def extend_points(points):
            return center_of_lines(points)

        def extend_marks():
            self.draw_rect(
                center_of_lines(self.mark_points),
                'yellow',
                'yellow',
                'add',
                draw_lines=False,
            )
        if len(self.mark_points) == 4:
            extend_marks()

        if len(self.mark_points) and self.track_point and not self.is_index_lock:
            prev_point = self.mark_points[-1]
            curr_point = self.track_point
            self.img_canvas.create_line(
                prev_point.x, prev_point.y,
                curr_point.x, curr_point.y,
                fill="red", width=1, tags='mark')
            if len(self.mark_points) == 3:
                prev_point = self.mark_points[0]
                self.img_canvas.create_line(
                    prev_point.x, prev_point.y,
                    curr_point.x, curr_point.y,
                    fill="red", width=1, tags='mark')

    def clear_all(self):
        self.predict_points.clear()
        self.mark_points.clear()
        self.img_canvas.delete('predict')
        self.img_canvas.delete('mark')
        self.track_point = None

    def clear_last(self):
        if len(self.mark_points):
            self.mark_points.pop()
            self.img_canvas.delete('mark')
            self.img_canvas.delete('add')
            self.draw()

    def track(self, point: Point, track_index: Optional[int]):
        if len(self.mark_points) == 0 or len(self.mark_points) > 3:
            self.track_point = None
        else:
            self.track_point = point
        self.img_canvas.delete('mark')
        self.img_canvas.delete('add')

        if not self.is_index_lock:
            self.track_index = track_index

        if self.is_index_lock:
            self.mark_points[self.track_index] = point

        self.draw()

    def add_point(self, point: Point):
        if self.track_index != None and not self.is_index_lock:
            self.is_index_lock = True
            return

        if self.is_index_lock:
            self.is_index_lock = False
            return

        if len(self.mark_points) < 4:
            self.mark_points.append(point)
            self.draw()


def on_mouse_click(x: int, y: int,):
    point = Point(x=x, y=y)
    draw_frame.add_point(point)


def button_left(event: Event):
    if widget_name == str(event.widget):
        on_mouse_click(event.x, event.y,)


def button_right(event: Event):
    draw_frame.clear_last()


def circle_index(point: Point) -> Optional[int]:
    def is_in_circle(center: Point, point: Point):
        radius = 10
        dist = math.sqrt((center.x - point.x) ** 2 + (center.y - point.y) ** 2)

        return dist <= radius

    points = draw_frame.mark_points
    points_result = [is_in_circle(center, point) for center in points]
    if any(points_result):
        return points_result.index(True)
    else:
        return None


def motion(event: Event):
    if '.container.image.canvas' == str(event.widget):
        point = Point(x=event.x, y=event.y,)
        draw_frame.track(point, track_index=circle_index(point))


def set_name(name: str):
    global top_label
    top_label.configure(text=name)


def on_prev():
    on_clear()
    draw_frame.draw_image(get_prev_image())


def on_next():
    on_clear()
    draw_frame.draw_image(get_next_image())


def on_zero():
    draw_frame.zero()
    on_save()


def on_whitespace():
    on_save()


def on_key(event: Event):
    print(event.keycode)
    if event.keycode == 32:
        on_whitespace()
    if event.keycode == 39:
        on_next()
    if event.keycode == 37:
        on_prev()


def on_save():
    name = get_current_image()
    (p, x, y, _, i, n, m) = name
    y = [[point.x, point.y] for point in draw_frame.mark_points]
    name = (p, x, y, True, i, n, m)
    img_info[curent_image_index] = name
    on_save_callback(name)
    on_next()


def on_clear():
    draw_frame.clear_all()


def on_copy():
    name = get_current_image()
    pc.copy(str(name[0]))


def start_ui(img_data: list, callback):
    global draw_frame
    global top_label
    global count_label
    global resized_frame_path
    global img_info
    global images_marked
    global size
    global img_height_frame
    global img_height
    global img_width
    global padding
    global info_label
    global on_save_callback

    on_save_callback = callback
    not_updated = filter(lambda x: not x[3], img_data)
    updated = filter(lambda x: x[3], img_data)
    img_info = [*not_updated, *updated]

    size = Size(width=900, height=1300, bar=50)
    img_height_frame = size.height - size.bar - size.bar
    img_height = 1188
    img_width = 800
    padding = 0
    img_height = img_height + padding * 2
    img_width = img_width + padding * 2

    root = Tk()
    root.title("Basic GUI Layout")
    root.config(bg="skyblue")
    root.minsize(size.width, size.height)
    root.maxsize(size.width, size.height)

    top_bar_frame = Frame(
        root, bg='grey',
        width=size.width, height=size.bar
    )
    top_bar_frame.grid(row=0, column=0, sticky="NW")

    top_label = Label(top_bar_frame)
    top_label.grid(row=0, column=2,)
    Button(top_bar_frame, text="copy", command=on_copy).grid(row=0, column=1,)
    Button(top_bar_frame, text="clear", command=on_clear).grid(row=0, column=0,)

    image_frame = Frame(
        root, bg='bisque',
        name=container_name,
        width=size.width, height=img_height_frame,)
    image_frame.grid(row=1, column=0, sticky="NW")

    bottom_bar_frame = Frame(
        root, bg='grey',
        width=size.width, height=size.bar
    )
    bottom_bar_frame.grid(row=2, column=0, sticky="NW")

    Button(bottom_bar_frame, text="prev",
           command=on_prev).grid(row=0, column=0)
    Button(bottom_bar_frame, text="save",
           command=on_save).grid(row=0, column=1)
    Button(bottom_bar_frame, text="next",
           command=on_next).grid(row=0, column=3)
    Button(bottom_bar_frame, text="zero",
           command=on_zero).grid(row=0, column=4)
    count_label = Label(bottom_bar_frame)
    count_label.grid(row=0, column=5)
    info_label = Label(bottom_bar_frame)
    info_label.grid(row=0, column=6)

    x = (size.width / 2) - (img_width / 2)
    y = (img_height_frame / 2) - (img_height / 2)

    draw_frame = DrawFrame(image_frame, width=img_width,
                           height=img_height, background="blue")
    draw_frame.place(x=0, y=0,)

    draw_frame.draw_image(get_current_image())

    root.bind('<ButtonPress-1>', button_left)
    root.bind('<ButtonPress-3>', button_right)
    root.bind('<Motion>', motion)
    root.bind('<Key>', on_key)
    root.mainloop()


# start()
