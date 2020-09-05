#! /usr/bin/env python
import csv
from datetime import datetime, timedelta
from pathlib import Path

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

def find_file(time_range, file) -> Path:
    f_start = file["from"]
    f_end = file["to"]
    req_start = time_range["from"]
    req_end = time_range["to"]

    # Check if either start of file, or end of file is inside requested time range
    if req_start <= f_start <= req_end or req_start <= f_end <= req_end:
        print(f"Found file! {file['path']} --- Requested: {req_start} ==> {req_end}")
        return file["path"]


def load_requested_times():
    time_objects = []
    with open("test_data/input.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        for i, row in enumerate(reader):
            r_from = datetime.fromisoformat(row[1])
            r_to = datetime.fromisoformat(row[2])

            # Test for invalid range (from larger than to)
            if r_from >= r_to:
               print(f"Warning: row {i} is invalid. From date is ending before to date. Skipping...")
               continue
            time_objects.append({"from": r_from,
                                 "to": r_to})
    return time_objects


def get_needed_files_as_dates(path, requested_times):
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


def main():
    started = datetime.now()

    requested_times = load_requested_times()
    needed_files = get_needed_files_as_dates("test_data/grane/tmp", requested_times)

    path_set = set([f"{x.absolute().parent}/{x.name}" for x in needed_files])
    print("############################################")
    print("               Finished!")
    print(f"    Run took {datetime.now() - started} (dd:hh:mm:ss)")
    print("############################################")
    for i in path_set:
        print(i)


if __name__ == '__main__':
    main()
