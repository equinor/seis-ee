import os
from enum import Enum


class FileDetectionTypes(Enum):
    INOTIFY = "inotify"
    REGULAR = "regular"

class Config:
    decimated_files_dest = os.getenv("DECIMATED_FILES_DEST", "decimated_files")
    find_files_format = ["filename", "su-header"]
    reduce_files_options = ["segd-grane", "su-oseberg"]
    detection_types = [FileDetectionTypes.INOTIFY.value, FileDetectionTypes.REGULAR.value]
    stream_server_user = "kkje"   #"root"
    stream_server_host = "hnet.norwayeast.cloudapp.azure.com"   #"192.168.1.5"
    stream_server_dir = "/data/kjtest"   #"/data/css"


class FindFilesFormat(Enum):
    FILENAME = "filename"
    SU_HEADER = "su-header"


class InotifyEvents(Enum):
    IN_CREATE = "IN_CREATE"

