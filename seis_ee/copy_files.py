import os
import shutil

from extractors.decimate import DECIMATE_FORMAT, get_files


def copy_files(files, format):
    files = get_files(files)
    if format == DECIMATE_FORMAT.SU_OSEBERG.value:
        for f in files:
            name = f.split("/")[-1]
            shutil.copy(f, f"{os.getcwd()}/data/{DECIMATE_FORMAT.SU_OSEBERG.value}/{name}")
    elif format == DECIMATE_FORMAT.SEGD_GRANE.value:
        for f in files:
            name = f.split("/")[-1]
            shutil.copy(f, f"{os.getcwd()}/data/{DECIMATE_FORMAT.SEGD_GRANE.value}/{name}")
    else:
        raise NotImplemented(f"Format {format} is not supported")