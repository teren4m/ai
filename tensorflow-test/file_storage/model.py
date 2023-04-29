from pathlib import Path
import json
from typing import Optional
import cv2 as cv
import hashlib
import uuid
import numpy as np
from .db import DBHelper


class FileInfo():

    def __init__(
            self,
            id:int,
            name: str,
            path: str,
            collection: str,
            metadata: dict[str, str],
    ) -> None:
        self.id = id
        self.name = name
        self.path = path
        self.collection = collection
        self.metadata = metadata

    id:int
    name: str
    path: str
    key: str
    metadata: dict[str, str]

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class FileInfoListMapper:

    def map(self, data: list, collection:str) -> list[FileInfo]:
        temp = {}
        for item in data:
            file_info = FileInfo(id = item[0], name=item[1],path=item[2],collection=collection,metadata={})
            temp[file_info.id] = file_info
        for item in data:
            file_info:FileInfo = temp[item[0]]
            key = item[-2]
            value = item[-1]
            file_info.metadata[key] = json.loads(value)
        return list(temp.values())


class Storage():
    folder: Path
    info_file: str
    collection: str
    db: DBHelper

    def __init__(self, folder: Path, collection: str) -> None:
        self.collection = collection
        self.folder = folder
        self.info_file = str(folder / 'file_info.db')

    def get_info(self) -> list[FileInfo]:
        txt = self.info_file.read_text().replace('\n', '')
        info: list = json.loads(txt)
        return [FileInfo(**item) for item in info]

    def get_info_by_key(self) -> list[FileInfo]:
        mapper = FileInfoListMapper()
        result = self.db.get_list()
        return mapper.map(result, self.collection)

    def get_info_by_key_index(self, key, index) -> FileInfo:
        return list(filter(lambda x: x.key == key and x.index == index, self.info))[0]

    def update_info(self, file_info: FileInfo):
        find_items = list(filter(lambda x: file_info.name ==
                                 x.name and file_info.key == x.key, self.info))
        if len(find_items):
            find_items[0].index = file_info.index
            find_items[0].metadata = file_info.metadata
        else:
            self.info.append(file_info)
        self.update()

    def update_metadata(self, name: str, entry):
        value = json.dumps(entry[1])
        self.db.update_metadata(name, entry[0], value)

    def update_metadata_by_index(self, index: int, entry):
        value = json.dumps(entry[1])
        self.db.update_metadata_by_index(index, entry[0], value)

    def save_file_info(self, new_info: FileInfo):
        self.info.append(new_info)
        self.update()

    def init(self):
        self.db = DBHelper(self.info_file, self.collection)
        self.db.init()

    def close(self):
        self.db.close()

    def create_file(self, img: np.ndarray) -> str:
        id = uuid.uuid4()
        file_path = str(self.folder / (str(id) + '.png'))
        cv.imwrite(file_path, img)
        return file_path

    def save_img(self, img: np.ndarray, metadata: dict[str, str] = {}) -> FileInfo:
        hash = hashlib.sha256(img).hexdigest()
        path = self.db.get_path_by_hash(hash)
        if not path:
            path = self.create_file(img)
            self.db.save_hash(hash, path)
            print('save {}'.format(path))

        p = Path(path)
        name = p.stem
        
        if not len(self.db.get(name)):
            file_info = FileInfo(
                1, name, str(p), self.collection, metadata
            )
            self.db.insert([
                    file_info.__dict__
            ])
        else:
            print('{} exist'.format(name))

    def remove_by_id(self, id:int):
        self.db.remove_by_id(id)
           
