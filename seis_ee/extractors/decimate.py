import csv
import json
import subprocess


def get_files(path: str):
    with open(path) as file:
        files = file.read().splitlines()
        return files


def get_nodes(path: str):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [int(row["nodeName"]) for row in reader if row]


def decimate(file, nodes):
    conf = {
        "name": "grane-test",
        "format": "segd-grane",
        "description": "30 nodes from grane",
        "included_nodenames": [100289]

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


def decimate_files(files_to_decimate_file, sensor_nodes_file):
    files_to_decimate_file = get_files(files_to_decimate_file)
    nodes_to_keep = get_nodes(sensor_nodes_file)
    for line in files_to_decimate_file:
        decimate(line, nodes_to_keep)


if __name__ == '__main__':
    # files_to_decimate = get_files("../test_result.txt")
    nodes_to_keep = get_nodes("../../papers/grane_nodes.csv")

    # for f in files_to_decimate:
    decimate("/private/stoo/git/seis-ee/test_data/grane/full-files/2020-07-24-11-43-47-Grane2128990.sgd",
             nodes_to_keep)
