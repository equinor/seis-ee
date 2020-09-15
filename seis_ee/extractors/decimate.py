import csv
import json
import os
import subprocess
from enum import Enum

decimate_result_location = "/data/decimated_files"


class DecimateFormat(Enum):
    SEGD_GRANE = "segd-grane"
    SU_OSEBERG = "su-oseberg"


def get_files(path: str):
    with open(path) as file:
        files = file.read().splitlines()
        return files


def get_nodes(path: str):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [int(row["nodeName"]) for row in reader if row]


def decimate_grane(file, nodes):
    conf = {
        "name": "grane-test",
        "format": DecimateFormat.SEGD_GRANE.value,
        "description": "30 nodes from grane for HNET",
        "included_nodenames": nodes

    }
    conf_string = json.dumps(conf)
    try:
        # decimate_process = subprocess.run(args=f"../../decimate -y -confstring '{conf_string}' --ignore-missing {file}",
        decimate_process = subprocess.run(
            args=f"decimate -y --rotate=false  --dst /data/decimated_files --confstring '{conf_string}' {file}",
            shell=True, check=True, capture_output=True, encoding="UTF-8")
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr)
    if decimate_process.returncode:
        print(decimate_process.stderr)
        raise ChildProcessError(decimate_process.stderr)

    print(decimate_process.stderr)


def decimate_oseberg(file, nodes):
    raise NotImplemented("Decimate of oseberg files are not implemented")
    conf = {
        "name": "oseberg-test",
        "format": DecimateFormat.SU_OSEBERG.value,
        "description": "30 nodes from oseberg for HNET",
        "included_nodenames": nodes

    }
    conf_string = json.dumps(conf)
    try:
        decimate_process = subprocess.run(args=f"../../decimate-0.4.0/decimate -y -confstring '{conf_string}' {file}",
                                          shell=True, check=True, capture_output=True, encoding="UTF-8")
    except subprocess.CalledProcessError as e:
        raise Exception(e.stderr)
    if decimate_process.stderr:
        print(decimate_process.stderr)
        raise ChildProcessError(decimate_process.stderr)

    print(decimate_process.stdout)


def decimate_files(files_to_decimate_file, sensor_nodes_file, format):
    # Workaround for bug where Decimate crashes with missing dir
    os.makedirs(decimate_result_location, exist_ok=True)

    files_to_decimate_file = get_files(files_to_decimate_file)
    nodes_to_keep = get_nodes(sensor_nodes_file)

    if format == DecimateFormat.SEGD_GRANE.value:
        for line in files_to_decimate_file:
            decimate_grane(line, nodes_to_keep)
    elif format == DecimateFormat.SU_OSEBERG.value:
        for line in files_to_decimate_file:
            decimate_oseberg(line, nodes_to_keep)
    else:
        raise NotImplemented(f"Format {format} is not supported")


if __name__ == '__main__':
    # files_to_decimate = get_files("../test_result.txt")
    nodes_to_keep = get_nodes("../../../sensors.txt/grane_nodes.csv")

    # for f in files_to_decimate:
    decimate_grane("/private/stoo/git/seis-ee/test_data/grane/full-files/2020-07-24-11-43-47-Grane2128990.sgd",
                   nodes_to_keep)
