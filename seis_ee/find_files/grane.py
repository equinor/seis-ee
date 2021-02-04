from datetime import datetime, timedelta
from operator import itemgetter
from pathlib import Path
from typing import Dict

from utils import logger

def grane_path_to_date(path: Path) -> datetime:
    #assume grane file name is on the format: 2019-10-26-07-43-59-Grane1035406.sgd
    filename = path.name
    filename_parts = filename.split("-")
    if (len(filename_parts) < 5):
        logger.debug(f"Skipping file; {str(path)}")
        return

    year, month, day, hour, min, sec = filename_parts[0], filename_parts[1], filename_parts[2], filename_parts[3], filename_parts[4], filename_parts[5]
    return datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(min), second=int(sec))

def grane_path_to_dates(path: Path):
    try:
        first_date = grane_path_to_date(path)

    except Exception as e:
        logger.info(f"Failed to parse filename into date; {path.name}")
        logger.info(e)
        return
    return {"path": path, "from": first_date, "to": first_date + timedelta(seconds=8)}


def needed_files(target, requested_times):
    target = Path(target)

    files = [x for x in target.rglob("*") if x.is_file()]
    # Filter out already decimated files
    files = [x for x in files if not x.name.endswith("_dec.sgd")]
    files_as_dates = [grane_path_to_dates(f) for f in files]

    files_as_dates = sorted([x for x in files_as_dates if x], key=itemgetter("from"))

    needed_files = []

    for i in requested_times:
        for f in files_as_dates:
            result = find_file(i, f)
            if result:
                needed_files.append(result)
    number_of_found_files = len(needed_files)

    missing_events = find_missing_events(needed_files, requested_times)
    events_and_file_times_not_found = include_missing_events_in_result(missing_events)

    all_events_and_file_times = needed_files + [event_and_file_time for event_and_file_time in
                                                events_and_file_times_not_found]
    return all_events_and_file_times, number_of_found_files, len(missing_events)


def find_missing_events(files, requested_times):
    events_in_needed_files = [x["event"] for x in files]
    event_in_requested_times = [x for x in requested_times]
    return [x for x in event_in_requested_times if str(x["event"]) not in events_in_needed_files]


def find_missing_file_times(missing_event):
    missing_file_times = []
    f_start = missing_event["from"]
    f_end = missing_event["to"]

    while f_start <= f_end:
        missing_file_times.append(f_start)
        f_start += timedelta(0, 5)
    return sorted(missing_file_times)


def include_missing_events_in_result(missing_events):
    events_and_file_time_increments = []

    for missing_event in missing_events:
        missing_file_times = find_missing_file_times(missing_event)
        events_and_file_time_increments = events_and_file_time_increments + [
            {"event": str(missing_event["event"]), "file_time": str(missing_file_time),
             "path": "### Event not found in any files ###"}
            for missing_file_time in missing_file_times]

    return events_and_file_time_increments


def find_file(time_range, file) -> Dict:
    f_start = file["from"]
    f_end = file["to"]
    req_start = time_range["from"]
    req_end = time_range["to"]

    # Check if either start of file, or end of file is inside requested time range
    if req_start <= f_start <= req_end or req_start <= f_end <= req_end:
        logger.debug(f"Found file! {file['path']} --- Requested: {req_start} ==> {req_end}")

        return {"event": str(time_range["event"]),"file_time": str(f_start),"path": str(file["path"].absolute())}

