import os
import shutil

from extractors.decimate import DecimateFormat, get_files


def copy_files(files, format):
    files = get_files(files)
    if format == DecimateFormat.SU_OSEBERG.value:
        for f in files:
            name = f.split("/")[-1]
            shutil.copy(f, f"{os.getcwd()}/data/{DecimateFormat.SU_OSEBERG.value}/{name}")
    elif format == DecimateFormat.SEGD_GRANE.value:
        for f in files:
            name = f.split("/")[-1]
            shutil.copy(f, f"{os.getcwd()}/data/{DecimateFormat.SEGD_GRANE.value}/{name}")
    else:
        raise NotImplemented(f"Format {format} is not supported")