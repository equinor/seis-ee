#! /usr/bin/env python
import csv
import os
from datetime import datetime
from pathlib import Path

from config import Config, FindFilesFormat
from find_files.oseberg import requested_times_to_oseberg_paths
from utils import load_requested_times, logger, print_help_and_exit

# How long a period each file covers, in seconds
files_time_slices = 9 - 1


# TODO: Optimize: Stop iterating files when the requested time slice has been found.


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
    number_missing_events, number_found_files = 0, 0
    if format == FindFilesFormat.FILENAME.value:
        from find_files.grane import needed_files
        needed_files, number_found_files, number_missing_events = needed_files(target, requested_times)
    elif format == FindFilesFormat.SU_HEADER.value:
        needed_files, number_found_files = requested_times_to_oseberg_paths(requested_times, target)

    logger.info("############################################")
    logger.info("               Finished!")
    logger.info(f"    Run took {datetime.now() - started} (dd:hh:mm:ss)")
    logger.info(f"    Found {number_found_files} file(s)")
    logger.info("############################################")

    if number_missing_events > 0:
        logger.info(f"    A total of {number_missing_events} event(s) not found in any files.")
        logger.info("############################################")

    result_file = f"{os.getcwd()}/{Path(target).stem}-result.csv"
    logger.warning(f"Writing result into {result_file}")
    with open(result_file, "w") as res_file:
        writer = csv.DictWriter(res_file, fieldnames=["event", "file_time", "path"])
        writer.writeheader()
        writer.writerows(needed_files)


if __name__ == '__main__':
    file_finder("/project/grane-passive/", "./requested-times-pri.csv", "filename")
