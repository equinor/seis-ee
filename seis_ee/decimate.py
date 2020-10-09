import csv
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import Dict, List

from config import Config
from readers.segd import number_of_samples_in_segd_file
from utils import logger

decimate_result_location = "/data/decimated_files"


class DecimateFormat(Enum):
    SEGD_GRANE = "segd-grane"
    SU_OSEBERG = "su-oseberg"


def get_files(path: str) -> List[Dict]:
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row["path"]]


def event_as_directory_name(event: str) -> str:
    return event.replace(" ", "-").replace(":", "-")


def get_nodes(path: str, format):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        if format == DecimateFormat.SEGD_GRANE.value:
            return [int(row["nodeName"]) for row in reader if row]
        else:
            return [int(row["nodeNumber"]) for row in reader if row]


def decimate_grane(file_dict, nodes):
    samples = number_of_samples_in_segd_file(file_dict["path"])
    conf = {
        "name": "hnet",
        "format": DecimateFormat.SEGD_GRANE.value,
        "description": "30 nodes from grane for HNET",
        "included_nodenames": nodes,
        "samples": samples
    }
    conf_string = json.dumps(conf)

    destination = f"{Config.decimated_files_dest}/{event_as_directory_name(file_dict['event'])}"

    # Workaround for bug where Decimate crashes with missing dir
    os.makedirs(destination, exist_ok=True)

    try:
        logger.info(f"Decimating {file_dict['path']}...")
        logger.info(f"Samples per trace: {samples}")
        decimate_process = subprocess.run(
            args=f"decimate -y --rotate=false --ignore-missing --dst {destination} --confstring '{conf_string}' {file_dict['path']}",
            shell=True, check=True, capture_output=True, encoding="UTF-8")

        logger.info(decimate_process.stderr)
    except subprocess.CalledProcessError as e:
        logger.warning(e.stderr)
        raise Exception(e.stderr)


def decimate_oseberg(file_dict, nodes):
    conf = {
        "name": "hnet",
        "format": DecimateFormat.SU_OSEBERG.value,
        "description": "30 nodes from oseberg for HNET",
        "included_nodenames": nodes
    }
    conf_string = json.dumps(conf)

    destination = f"{Config.decimated_files_dest}/{event_as_directory_name(file_dict['event'])}"

    # Workaround for bug where Decimate crashes with missing dir
    os.makedirs(destination, exist_ok=True)

    if not Path(file_dict["path"]).exists():
        raise FileNotFoundError(file_dict["path"])

    try:
        decimate_process = subprocess.run(
            args=f"decimate -y --rotate=false --ignore-missing --dst {destination} --confstring '{conf_string}' {file_dict['path']}",
            shell=True, check=True, capture_output=True, encoding="UTF-8")

        logger.info(decimate_process.stderr)
    except subprocess.CalledProcessError as e:
        logger.warning(e.stderr)
        raise Exception(e.returncode)


def decimate_files(files_to_decimate_file, sensor_nodes_file, format):
    start = datetime.now()

    files_to_decimate_file = get_files(files_to_decimate_file)
    nodes_to_keep = get_nodes(sensor_nodes_file, format)

    failed_in_some_way = []
    if format == DecimateFormat.SEGD_GRANE.value:
        for line in files_to_decimate_file:
            try:
                decimate_grane(line, nodes_to_keep)
            except Exception as e:
                failed_in_some_way.append(f"{line['path']};exit_code: {str(e)}")

    elif format == DecimateFormat.SU_OSEBERG.value:
        for line in files_to_decimate_file:
            try:
                decimate_oseberg(line, nodes_to_keep)
            except FileNotFoundError:
                logger.warning(f"{line['path']};exit_code: File not found!")
                failed_in_some_way.append(f"{line['path']};exit_code: File not found!")
            except Exception as e:
                logger.warning(f"{line['path']};exit_code: {str(e)}")
                failed_in_some_way.append(f"{line['path']};exit_code: {str(e)}")
    else:
        raise NotImplemented(f"Format {format} is not supported")

    if failed_in_some_way:
        with open(file="./error-log.txt", mode='w') as error_file:
            for i in failed_in_some_way:
                error_file.write(i + "\n")
        logger.warning(f"Wrote error log to {os.getcwd()}/error-log.txt")

    done = datetime.now() - start
    logger.info("#######################################")
    logger.info(
        f"Done! Took {done} to decimate {len(files_to_decimate_file)} files. {len(failed_in_some_way)} failed in some way.")
    logger.info("#######################################")


if __name__ == '__main__':

    decimate_files("/test-files.csv", "/sensors-oseberg.csv",
                   "su-oseberg")

    # # for f in files_to_decimate:
    # decimate_grane("/private/stoo/git/seis-ee/test_data/grane/full-files/2020-07-24-11-43-47-Grane2128990.sgd",
    #                nodes_to_keep)
