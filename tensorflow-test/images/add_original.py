from pathlib import Path

video_path = Path('../../openCV_python/data/video')


def load():
    img_list: list[Path] = [x for x in list(
        video_path.glob(str('**/*.png'))) if x.is_file()]
    
    print(img_list)
