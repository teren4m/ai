from pathlib import Path
import json
from typing import Optional


class FileInfo():

    def __init__(
            self,
            name: str,
            index: int,
            path: str,
            file_hash: str,
            key: str,
            metadata: dict[str, str],
    ) -> None:
        self.name = name
        self.index = index
        self.path = path
        self.file_hash = file_hash
        self.key = key
        self.metadata = metadata

    name: str
    index: int
    path: str
    file_hash: str
    key: str
    metadata: dict[str, str]

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Storage():
    folder: Path
    info_file: Path

    info: list[FileInfo]

    def __init__(self, folder: Path) -> None:
        self.folder = folder
        self.info_file = folder / 'info.txt'

    def get_info(self) -> list[FileInfo]:
        txt = self.info_file.read_text().replace('\n', '')
        info: list = json.loads(txt)
        return [FileInfo(**item) for item in info]

    def get_info_by_key(self, key) -> list[FileInfo]:
        return list(filter(lambda x: x.key == key, self.info))

    def update(self):
        info = list(map(lambda x: x.__dict__, self.info))
        self.info_file.write_text(json.dumps(info, indent=4))

    def update_info(self, file_info: FileInfo):
        find_items = list(filter(lambda x: file_info.name ==
                                 x.name and file_info.key == x.key, self.info))
        if len(find_items):
            find_items[0].index = file_info.index
            find_items[0].metadata = file_info.metadata
        else:
            self.info.append(file_info)
        self.update()

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
        if not self.info_file.exists():
            self.info_file.write_text('[]')
            self.info = []
        else:
            self.info = self.get_info()
