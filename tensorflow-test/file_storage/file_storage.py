from pathlib import Path
import numpy as np
import hashlib
import uuid
import cv2 as cv
from .model import FileInfo, Storage

folder = Path('/files_storage')

# storage = Storage(folder)
# storage.init()

# def save_img(key: str, index: int, img: np.ndarray, metadata: dict[str, str] = {}) -> FileInfo:
#     return storage.save_img(
#         key,
#         index,
#         img,
#         metadata,
#     )

# def get_img_by_key(key: str) -> list[FileInfo]:
#     return storage.get_info_by_key(key)


# def get_info_by_key_index(key: str, index: int) -> FileInfo:
#     return storage.get_info_by_key_index(key, index)


# def update_info(file_info: FileInfo):
#     storage.update_info(file_info)


# def update_metadata(key: str, index: int, entry):
#     storage.update_metadata(key, index, entry)


# def update():
#     storage.update()
