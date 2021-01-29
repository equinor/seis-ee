import inotify.adapters
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from typing import List, Set

from decimate import get_nodes
from find_files.oseberg import _datetime_to_oseberg_path
from streamer.db_service import Database
from streamer.stream_file import StreamFile
from config import InotifyEvents


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

def transfer_new_files(new_files: Set, database: Database, sensors: [], processed: Set):
    # the parameter set new_files contains path for the new files to stream
    for path in new_files:
        file = StreamFile(path, database)
        file.insert()
        work_file(file, sensors)
    processed.update(new_files)
    print(f"Transferred {len(new_files)}")
    return processed

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

    # stream new files not already in database
    if (len(new_files) > 0):
        processed = transfer_new_files(new_files, database, sensors, processed)

    # create an Inotify watcher to detect changes in target directory
    watcher = inotify.adapters.Inotify()

    date = datetime.now()
    todays_path = str(_datetime_to_oseberg_path(date, target_dir))
    watcher.add_watch(todays_path)

    # add functionality for watching tree of folders instead of only one folder
    watcher = inotify.adapters.InotifyTree(target_dir)

    # check if events in target directory occur
    for event in watcher.event_gen(yield_nones=False):
        (_, event_type_names, path, filename) = event
        filepath: str = f"{path}/{filename}"

        #Transfer file if new file is created
        if (InotifyEvents.IN_CREATE.value in event_type_names and Path(filepath).is_file() ):
            new_files: Set = files_in_todays_directory(target_dir).difference(processed)
            if (len(new_files) > 0):
                processed = transfer_new_files(new_files, database, sensors, processed)

    '''
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
    '''


if __name__ == '__main__':
    main()
