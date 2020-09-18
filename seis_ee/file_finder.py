#! /usr/bin/env python
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

from config import Config, FindFilesFormat
from find_files.filename import grane_path_to_dates
from find_files.su_header import su_path_to_dates
from utils import logger, print_help_and_exit

# How long a period each file covers, in seconds
files_time_slices = 9 - 1


# TODO: Optimize: Stop iterating files when the requested time slice has been found.

def find_file(time_range, file) -> Dict:
    f_start = file["from"]
    f_end = file["to"]
    req_start = time_range["from"]
    req_end = time_range["to"]

    # Check if either start of file, or end of file is inside requested time range
    if req_start <= f_start <= req_end or req_start <= f_end <= req_end:
        logger.debug(f"Found file! {file['path']} --- Requested: {req_start} ==> {req_end}")
        return {"path": str(file["path"].absolute()), "event": str(time_range["event"])}


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
                logger.warning(f"row {i} is invalid. From date is ending before to date. Skipping...")
                continue
            time_objects.append({"event": r_event,
                                 "from": r_from,
                                 "to": r_to})
    return time_objects


def timerange_of_files(target, requested_times, format):
    target = Path(target)
    files = [x for x in target.rglob("*") if x.is_file()]

    if format == FindFilesFormat.FILENAME.value:
        files_as_dates = [grane_path_to_dates(f) for f in files]
    elif format == FindFilesFormat.SU_HEADER.value:
        files_as_dates = [su_path_to_dates(f) for f in files]
    else:
        logger.error(f"Invalid format; {format}")
        print_help_and_exit()

    files_as_dates = [x for x in files_as_dates if x]

    needed_files = []
    for i in requested_times:
        for f in files_as_dates:
            result = find_file(i, f)
            if result:
                needed_files.append(result)
    return needed_files


def file_finder(target, requested_times, format):
    if not Path(target).exists():
        logger.error(f"ERROR: Target '{target}' does not exist")
        print_help_and_exit()
    if not Path(requested_times).exists():
        logger.error(f"ERROR: Input file '{requested_times}' does not exist")
        print_help_and_exit()
    if not Path(requested_times).is_file():
        logger.error(f"ERROR: Input target '{requested_times}' is not a file")
        print_help_and_exit()
    if not format.casefold() in Config.find_files_format:
        logger.error(f"ERROR: Invalid format; {format}")
        print_help_and_exit()

    started = datetime.now()
    logger.info(f"Looking for files recursively in {target}. This could take a while...")

    requested_times = load_requested_times(requested_times)
    needed_files = timerange_of_files(target, requested_times, format)

    logger.info("############################################")
    logger.info("               Finished!")
    logger.info(f"    Run took {datetime.now() - started} (dd:hh:mm:ss)")
    logger.info(f"    Found {len(needed_files)} file(s)")
    logger.info("############################################")

    result_file = f"{os.getcwd()}/{Path(target).stem}-result.csv"
    logger.warning(f"Writing result into {result_file}")
    with open(result_file, "w") as res_file:
        writer = csv.DictWriter(res_file, fieldnames=["path", "event"])
        writer.writeheader()
        writer.writerows(needed_files)


if __name__ == '__main__':
    file_finder("./test_data", "./requested-times.csv", "su-header")
