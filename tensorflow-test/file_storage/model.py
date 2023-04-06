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
            name: str,
            index: int,
            path: str,
            collection: str,
            metadata: dict[str, str],
    ) -> None:
        self.name = name
        self.index = index
        self.path = path
        self.collection = collection
        self.metadata = metadata

    name: str
    index: int
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
            file_info = FileInfo(name=item[1],path=item[2],index=item[0],collection=collection,metadata={})
            temp[file_info.index] = file_info
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

    def update(self):
        pass
        # info = list(map(lambda x: x.__dict__, self.info))
        # self.info_file.write_text(json.dumps(info, indent=4))

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

    def find_info(self, hash: str) -> Optional[FileInfo]:
        filtered_info = list(filter(lambda x: x.file_hash == hash, self.info))
        if len(filtered_info):
            return filtered_info[0]
        else:
            return None

    def init(self):
        self.db = DBHelper(self.info_file, self.collection)
        self.db.init()

    def close(self):
        self.db.close()

    def save_img(self, key: str, index: int, img: np.ndarray, metadata: dict[str, str] = {}) -> FileInfo:
        pass
        # hash = hashlib.sha256(img).hexdigest()
        # find_file_info = self.find_info(hash)
        # if find_file_info:
        #     new_info = FileInfo(
        #         name=find_file_info.name,
        #         index=index,
        #         path=find_file_info.path,
        #         file_hash=hash,
        #         key=key,
        #         metadata=metadata,
        #     )
        #     self.update_info(new_info)
        #     return new_info

        # id = uuid.uuid4()
        # file_path = self.folder / (str(id) + '.png')
        # file_info = FileInfo(
        #     name=str(id),
        #     index=index,
        #     path=str(file_path),
        #     file_hash=hash,
        #     key=key,
        #     metadata=metadata,
        # )
        # cv.imwrite(str(file_path), img)
        # self.save_file_info(file_info)
        # return file_info
