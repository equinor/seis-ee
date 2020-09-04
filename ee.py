#! /usr/bin/env python
import csv
from datetime import datetime
from pathlib import Path


def path_to_dates(path: Path):
    # Try splitting the filename
    elements = path.name.split("-")
    if len(elements) < 5:
        print(f"Skipping file; {str(path)}")
        return

    try:
        first_hour = int(elements[3][:2])
        first_minute = int(elements[3][2:4])
        second_hour = int(elements[4][:2])
        second_minute = int(elements[4][2:4])

        first_date = datetime(int(elements[0]), int(elements[1]), int(elements[2]), first_hour, first_minute)
        second_date = datetime(int(elements[0]), int(elements[1]), int(elements[2]), second_hour, second_minute)
    except Exception as e:
        print(f"Failed to parse filename into date; {path.name}")
        print(e)
        return

    return {"path": path, "from": first_date, "to": second_date, "range": second_date - first_date}


def find_file(time_range, files) -> Path:
    for f in files:
        # check if input range 'from' is between the dates in file
        if f["from"] <= time_range["from"] < f["to"]:
            print(f"Found file! {f['path'].name}")
            return f["path"]

        # check if input range 'to' is between the dates in file
        if f["from"] <= time_range["to"] < f["to"]:
            print(f"Found file! {f['path'].name}")
            return f["path"]


def main():
    started = datetime.now()
    time_objects = []

    with open("test_data/input.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ")
        for row in reader:
            time_objects.append({"event": datetime.fromisoformat(row[0]),
                                 "to": datetime.fromisoformat(row[1]),
                                 "from": datetime.fromisoformat(row[2])})

    path = Path("./test_data")
    files = [x for x in path.rglob("*") if x.is_file()]
    files_as_dates = [path_to_dates(f) for f in files]
    files_as_dates = [x for x in files_as_dates if x]

    needed_files = [find_file(i, files_as_dates) for i in time_objects]
    needed_files = [x for x in needed_files if x]

    path_set = set([f"{x.absolute().parent}/{x.name}" for x in needed_files])
    print("############################################")
    print("               Finnished!")
    print(f"    Run took {datetime.now() - started} (dd:hh:mm:ss)")
    print("############################################")
    for i in path_set:
        print(i)


if __name__ == '__main__':
    main()
