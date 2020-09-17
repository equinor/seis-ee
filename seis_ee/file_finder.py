#! /usr/bin/env python
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict


from utils import print_help_and_exit, logger

# How long a period each file covers, in seconds
files_time_slices = 9 - 1


def grane_path_to_dates(path: Path):
    # Try splitting the filename
    elements = path.name.split("-")
    if len(elements) < 5:
        print(f"Skipping file; {str(path)}")
        return

    try:
        first_date = datetime(year=int(elements[0]), month=int(elements[1]), day=int(elements[2]),
                              hour=int(elements[3]), minute=int(elements[4]), second=int(elements[5]))
    except Exception as e:
        print(f"Failed to parse filename into date; {path.name}")
        print(e)
        return
    res = {"path": path, "from": first_date, "to": first_date + timedelta(seconds=8)}
    return res


# TODO: Optimize: Stop iterating files when the requested time slice has been found.

def find_file(time_range, file) -> Dict:
    f_start = file["from"]
    f_end = file["to"]
    req_start = time_range["from"]
    req_end = time_range["to"]

    # Check if either start of file, or end of file is inside requested time range
    if req_start <= f_start <= req_end or req_start <= f_end <= req_end:
        print(f"Found file! {file['path']} --- Requested: {req_start} ==> {req_end}")
        return {"path": str(file["path"].absolute()), "event": str(time_range["event"])}


def get_timerange_from_filename(path, requested_times):
    path = Path(path)
    files = [x for x in path.rglob("*") if x.is_file()]
    files_as_dates = [grane_path_to_dates(f) for f in files]
    files_as_dates = [x for x in files_as_dates if x]

    needed_files = []
    for i in requested_times:
        for f in files_as_dates:
            result = find_file(i, f)
            if result:
                needed_files.append(result)
    return needed_files


def get_timerange_from_segy_header(path, requested_times):
    raise NotImplemented


def load_requested_times(input):
    time_objects = []
    with open(input) as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        for i, row in enumerate(reader):
            # Skip empty rows
            if not row:
                continue
            r_event = datetime.fromisoformat(row[0])
            r_from = datetime.fromisoformat(row[1])
            r_to = datetime.fromisoformat(row[2])

            # Test for invalid range (from larger than to)
            if r_from >= r_to:
                print(f"Warning: row {i} is invalid. From date is ending before to date. Skipping...")
                continue
            time_objects.append({"event": r_event,
                                 "from": r_from,
                                 "to": r_to})
    return time_objects


def file_finder(target, requested_times, format):
    if not Path(target).exists():
        print(f"ERROR: Target '{target}' does not exist")
        print_help_and_exit()
    if not Path(requested_times).exists():
        print(f"ERROR: Input file '{requested_times}' does not exist")
        print_help_and_exit()
    if not Path(requested_times).is_file():
        print(f"ERROR: Input target '{requested_times}' is not a file")
        print_help_and_exit()
    if not format.casefold() in ("filename", "segy"):
        print(f"ERROR: Invalid format; {format}")
        print_help_and_exit()

    started = datetime.now()
    logger.info(f"Looking for files recursively in {target}. This could take a while...")

    requested_times = load_requested_times(requested_times)
    needed_files = get_timerange_from_filename(target, requested_times)

    print("############################################")
    print("               Finished!")
    print(f"    Run took {datetime.now() - started} (dd:hh:mm:ss)")
    logger.info(f"    Found {len(needed_files)} files")
    print("############################################")

    result_file = f"{os.getcwd()}/{Path(target).stem}-result.csv"
    print(f"Writing result into {result_file}")
    with open(result_file, "w") as res_file:
        writer = csv.DictWriter(res_file, fieldnames=["path", "event"])
        writer.writeheader()
        writer.writerows(needed_files)


if __name__ == '__main__':
    file_finder("./test_data", "./requested-times.txt", "filename")
