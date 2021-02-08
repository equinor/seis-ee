import os
from enum import Enum


class FileDetectionTypes(Enum):
    INOTIFY = "inotify"
    REGULAR = "regular"


class FilesFormat(Enum):
    SEGD_GRANE = "segd-grane"
    SU_OSEBERG = "su-oseberg"
    SEGD_SNORRE = "segd-snorre"


class Config:
    DECIMATED_FILES_DEST = os.getenv("DECIMATED_FILES_DEST", "decimated_files")
    REDUCE_FILES_OPTIONS = [FilesFormat.SEGD_GRANE.value, FilesFormat.SU_OSEBERG.value, FilesFormat.SEGD_SNORRE.value]
    NEW_FILE_DETECTION = [FileDetectionTypes.INOTIFY.value, FileDetectionTypes.REGULAR.value]
    STREAM_TARGET_USER = os.getenv("STREAM_TARGET_USER", "kkje")
    STREAM_TARGET_HOST = os.getenv("STREAM_TARGET_HOST", "hnet.norwayeast.cloudapp.azure.com")
    STREAM_TARGET_DIR = os.getenv("STREAM_TARGET_DIR", "/data/kjtest")


class InotifyEvents(Enum):
    IN_CREATE = "IN_CREATE"
    IN_CLOSE_WRITE = "IN_CLOSE_WRITE"
