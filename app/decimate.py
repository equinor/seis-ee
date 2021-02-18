import json
import os
import subprocess  # nosec
from pathlib import Path
from typing import Dict

from settings import settings
from utils import logger


def call_decimate(file_path: str, destination: str, conf: Dict):
    # Workaround for bug where Decimate crashes with missing dir
    os.makedirs(destination, exist_ok=True)

    try:
        logger.info(f"Decimating {file_path}...")
        decimate_process = subprocess.run(
            args=[
                "decimate",
                "-y",
                "--rotate=false",
                "--ignore-missing",
                "--dst",
                destination,
                "--confstring",
                json.dumps(conf),
                file_path,
            ],
            check=True,
            capture_output=True,
            encoding="UTF-8",
            shell=False,  # nosec
        )
        logger.info(decimate_process.stderr)
    except subprocess.CalledProcessError as e:
        logger.warning(e.stderr)
        raise Exception(e.stderr)


# TODO add the package segdpy with docker. Now, this package is installed manually...
# if this package is not installed you cannot run decimate_grane
# the segdpy package from github is installed locally by just
# unzipping the python files to the local folder app / segdpy
def decimate_grane(file_path: str, destination: str = settings.DECIMATED_FILES_DEST + "/grane"):
    # TODO: Update when segdpy becomes OpenSource
    # samples = number_of_samples_in_segd_file(file_path)
    conf = {
        "name": "ccs-grane",
        "format": "segd-grane",
        "description": f"{len(settings.GRANE_SENSORS)} nodes from Grane",
        "included_nodenames": settings.GRANE_SENSORS,
        "samples": settings.GRANE_SAMPLE_RATE,
        "fileHeaderSize": settings.GRANE_FILE_HEADER_SIZE,
        "traceHeaderSize": 116,
    }
    call_decimate(file_path, destination, conf)
    return f"{destination}/{str(Path(file_path).stem)}.{conf['name']}.dsgd"


def decimate_snorre(file_path: str, destination: str = settings.DECIMATED_FILES_DEST + "/snorre"):
    # TODO: Update when segdpy becomes OpenSource
    # samples = number_of_samples_in_segd_file(file_path)
    conf = {
        "name": "ccs-snorre",
        "format": "segd-grane",
        "description": f"{len(settings.SNORRE_SENSORS)} nodes from Snorre for CCS-Passive",
        "included_nodenames": settings.SNORRE_SENSORS,
        "samples": settings.SNORRE_SAMPLE_RATE,
        "fileHeaderSize": settings.SNORRE_FILE_HEADER_SIZE,
        "traceHeaderSize": 116,
    }
    call_decimate(file_path, destination, conf)
    return f"{destination}/{str(Path(file_path).stem)}.{conf['name']}.dsgd"


def decimate_oseberg(file_path: str, destination: str = "/" + settings.DECIMATED_FILES_DEST + "/oseberg"):
    conf = {
        "name": "ccs-oseberg",
        "format": "su-oseberg",
        "description": "30 nodes from oseberg for CCS",
        "included_nodenames": settings.OSEBERG_SENSORS,
    }

    call_decimate(file_path, destination, conf)
    return f"{destination}/{str(Path(file_path).stem)}.{conf['name']}.segy"
