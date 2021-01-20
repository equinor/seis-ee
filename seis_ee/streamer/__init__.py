from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from typing import List, Set

from decimate import get_nodes
from find_files.oseberg import _datetime_to_oseberg_path
from streamer.db_service import Database
from streamer.stream_file import StreamFile


def files_in_todays_directory(target_dir: str) -> Set[str]:
    date = datetime.now()
    path = _datetime_to_oseberg_path(date, target_dir)
    # path = _datetime_to_oseberg_path(date, "/home/stig/git/seis-ee/test_data")
    target = Path(path)
    files = [str(x.resolve()) for x in target.rglob("*") if x.is_file()]
    return set(files)


def work_file(file: StreamFile, sensors: List[int]) -> StreamFile:
    if not file.decimated:
        file.decimate(nodes=sensors)
    if not file.transferred:
        file.transfer()
    return file


def continue_unfinished(sensors: List[int]):
    database = Database()
    unfinished = database.all_unfinished()
    for file in unfinished:
        work_file(file, sensors)


# {
#   "path": { "decimated": bool, "decimated_path": "path/to/decimated/file", "transferred": bool }
# }
def main(target_dir, sensor_list, format):
    database = Database()
    # Delete all records older than x(2) days, as they are not relevant
    database.delete_old_rows()

    # Load sensors to keep traces from
    sensors = get_nodes(sensor_list, format)

    # Complete any unfinished file transfers that was started on a previous run
    continue_unfinished(sensors)

    # On first loop, load existing files from database
    processed: Set = set(database.select_all_paths())
    print("Looking for new files...")
    new_files: Set = files_in_todays_directory(target_dir).difference(processed)
    print(f"Found {len(new_files)} new files")

    minimum_time_loop = timedelta(seconds=30)

    # Loop indefinitely, streaming any new files
    while True:
        start = datetime.now()
        for path in new_files:
            file = StreamFile(path, database)
            file.insert()
            work_file(file, sensors)

        processed.update(new_files)
        print(f"Transferred {len(new_files)}")

        # If loop took shorter than x(2)min, wait till x minutes has passed
        elapsed = datetime.now() - start
        if elapsed < minimum_time_loop:
            sleep((minimum_time_loop - elapsed).seconds)

        print("Looking for new files...")
        new_files: Set = files_in_todays_directory(target_dir).difference(processed)
        print(f"Found {len(new_files)} new files")


if __name__ == '__main__':
    main()
