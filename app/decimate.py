import csv
import json
import os
import subprocess  # nosec
from pathlib import Path
from typing import Dict, List

from settings import FileFormat, settings

# from readers.segd import number_of_samples_in_segd_file
from utils import logger


def get_files(path: str) -> List[Dict]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row["path"]]


def event_as_directory_name(event: str) -> str:
    return event.replace(" ", "-").replace(":", "-")


def get_nodes(path: str, format):
    with open(path, encoding="utf-8-sig") as csvfile:  # on windows, you might need to use the utf-8-sig encoding
        reader = csv.DictReader(csvfile)
        if format == FileFormat.SEGD_GRANE.value:
            return [int(row["nodeName"]) for row in reader if row]
        else:
            return [int(row["nodeNumber"]) for row in reader if row]


# TODO add the package segdpy with docker. Now, this package is installed manually...
# if this package is not installed you cannot run decimate_grane
# the segdpy package from github is installed locally by just
# unzipping the python files to the local folder app / segdpy
def decimate_grane(file_path: str, destination: str = settings.DECIMATED_FILES_DEST + "/grane"):
    # TODO: Update when segdpy becomes OpenSource
    samples = 4000
    # samples = number_of_samples_in_segd_file(file_path)
    conf = {
        "name": "hnet",
        "format": FileFormat.SEGD_GRANE.value,
        "description": "30 nodes from grane for HNET",
        "included_nodenames": settings.GRANE_SENSORS,
        "samples": samples,
    }
    conf_string = json.dumps(conf)

    # Workaround for bug where Decimate crashes with missing dir
    os.makedirs(destination, exist_ok=True)

    try:
        logger.info(f"Decimating {file_path}...")
        logger.info(f"Samples per trace: {samples}")
        decimate_process = subprocess.run(
            args=f"decimate -y --rotate=false --ignore-missing --dst {destination} --confstring '{conf_string}' {file_path}",  # noqa
            shell=True,
            check=True,
            capture_output=True,
            encoding="UTF-8",
        )

        logger.info(decimate_process.stderr)
    except subprocess.CalledProcessError as e:
        logger.warning(e.stderr)
        raise Exception(e.stderr)


def decimate_oseberg(file_path: str, destination: str = "/" + settings.DECIMATED_FILES_DEST + "/oseberg"):
    conf = {
        "name": "ccs",
        "format": FileFormat.SU_OSEBERG.value,
        "description": "30 nodes from oseberg for CCS",
        "included_nodenames": settings.OSEBERG_SENSORS,
    }
    conf_string = json.dumps(conf)

    # Workaround for bug where Decimate crashes with missing dir
    os.makedirs(destination, exist_ok=True)

    if not Path(file_path).exists():
        raise FileNotFoundError(file_path)

    try:
        subprocess.run(
            args=f"decimate -y --rotate=false --ignore-missing --dst {destination} --confstring '{conf_string}' {file_path}",  # noqa
            shell=True,
            check=True,
            encoding="UTF-8",
        )

    except subprocess.CalledProcessError as e:
        logger.warning(e.stderr)
        raise e