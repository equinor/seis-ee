import os
from typing import List

from decimate import decimate_oseberg
from find_files.oseberg import oseberg_path_to_date


class StreamFile:
    def __init__(self, path: str, database, decimated: bool = False, transferred: bool = False, decimated_path: str = None):
        self.path = path
        self.decimated = decimated
        self.transferred = transferred
        self.decimated_path = decimated_path
        self.database = database

    def decimate(self, nodes: List[int]):
        # TODO: Decimate
        date = oseberg_path_to_date(self.path)
        self.decimated_path = f"{os.getcwd()}/decimated_files/{date.year}/{date.month}"
        decimate_oseberg(self.path, nodes, destination=self.decimated_path)
        self.decimated = True
        self.database.update(self)

    def transfer(self):
        # TODO: Transfer
        self.transferred = True
        self.database.update(self)
        # raise NotImplemented

    def insert(self):
        return self.database.insert(self)

    def update(self):
        return self.database.update(self)

    @classmethod
    def from_dict(cls, a_dict):
        return cls(**a_dict)

    @classmethod
    def from_tuple(cls, a_tuple, database):
        return cls(path=a_tuple[0], database=database, decimated=a_tuple[1], transferred=a_tuple[2], decimated_path=a_tuple[3])

    def to_dict(self):
        return {
            "path": self.path,
            "decimated": self.decimated,
            "transferred": self.transferred,
            "decimated_path": self.decimated_path
        }

    def to_tuple(self):
        return self.path, self.decimated, self.transferred, self.decimated_path

    def __repr__(self):
        return f"Path: {self.path}, Decimated: {self.decimated}, Transferred: {self.transferred}"
