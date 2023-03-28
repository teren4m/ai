from pathlib import Path
import numpy as np
from typing import TypedDict
import hashlib
import uuid
import cv2 as cv
import json

folder = Path('/files_storage')
info_file = folder / 'info.txt'

def init():
    if not info_file.exists():
        with info_file.open('w') as f:
            f.write('[]')

init()


class FileInfo():

    def __init__(
            self,
            name: str,
            path: Path,
            file_hash: str,
            key: str,
            metadata: dict[str, str],
    ) -> None:
        self.name = name
        self.path = path
        self.file_hash = file_hash
        self.key = key
        self.metadata = metadata

    name: str
    path: str
    file_hash: str
    key: str
    metadata: dict[str, str]


def save_file_info(new_info: FileInfo):
    print(new_info.__dict__)
    info = []
    txt = info_file.read_text().replace('\n', '')
    info: list = json.loads(txt)
    info.append(new_info.__dict__)
    info_file.write_text(json.dumps(info, indent=4))
    return new_info

def save_img(key: str, img: np.ndarray, metadata: dict[str, str] = {}) -> FileInfo:
    hash = hashlib.sha256(img).hexdigest()
    id = uuid.uuid4()
    file_path = folder / (str(id) + '.png')
    file_info = FileInfo(
        name=str(id),
        path=str(file_path),
        file_hash=hash,
        key=key,
        metadata=metadata,
    )
    cv.imwrite(str(file_path), img)
    return save_file_info(file_info)
