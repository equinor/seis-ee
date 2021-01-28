import os
from enum import Enum


class Config:
    decimated_files_dest = os.getenv("DECIMATED_FILES_DEST", "decimated_files")
    find_files_format = ["filename", "su-header"]
    reduce_files_options = ["segd-grane", "su-oseberg"]
    stream_server_user = "kkje"
    stream_server_host = "hnet.norwayeast.cloudapp.azure.com"
    stream_server_dir = "/data/kjtest"


class FindFilesFormat(Enum):
    FILENAME = "filename"
    SU_HEADER = "su-header"
