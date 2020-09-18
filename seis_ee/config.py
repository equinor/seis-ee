import os
from enum import Enum


class Config:
    decimated_files_dest = os.getenv("DECIMATED_FILES_DEST", "decimated_files")
    find_files_format = ["filename", "su-header"]
    reduce_files_options = ["segd-grane", "su-oseberg"]


class FindFilesFormat(Enum):
    FILENAME = "filename"
    SU_HEADER = "su-header"
