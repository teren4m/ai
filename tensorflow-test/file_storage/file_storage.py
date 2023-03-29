from pathlib import Path
import numpy as np
import hashlib
import uuid
import cv2 as cv
from .model import FileInfo, Storage

folder = Path('/files_storage')

storage = Storage(folder)
storage.init()

def save_img(key: str, index: int, img: np.ndarray, metadata: dict[str, str] = {}) -> FileInfo:
    hash = hashlib.sha256(img).hexdigest()
    find_file_info = storage.find_info(hash)
    if find_file_info:
        new_info = FileInfo(
            name=find_file_info.name,
            index=index,
            path=find_file_info.path,
            file_hash=hash,
            key=key,
            metadata=metadata,
        )
        storage.update_info(new_info)
        return new_info

    id = uuid.uuid4()
    file_path = folder / (str(id) + '.png')
    file_info = FileInfo(
        name=str(id),
        index=index,
        path=str(file_path),
        file_hash=hash,
        key=key,
        metadata=metadata,
    )
    cv.imwrite(str(file_path), img)
    storage.save_file_info(file_info)
    return file_info


def get_img_by_key(key: str) -> list[FileInfo]:
    return storage.get_info_by_key(key)
