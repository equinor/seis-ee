from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Tuple

import segyio

from utils import load_requested_times, logger


def timerange_of_su_file(file_path: str) -> Tuple[datetime, datetime]:
    logger.debug(f"Finding timerange of {file_path}...")
    with segyio.su.open(file_path, endian="little", ignore_geometry=True) as f:

        # lowest_time = None
        # TODO: This is redundant as we now just assume a 9sec time span
        # highest_time = None

        # Documented here; https://segyio.readthedocs.io/en/latest/segyio.html#trace-header-keys
        # TODO: Might not be needed to check every header(?)
        # for header in f.header:
        year = f.header[0][157]
        day = f.header[0][159]
        hour = f.header[0][161]
        minute = f.header[0][163]
        second = f.header[0][165]

        date_string = f"{year}/{day}/{hour}/{minute}/{second}"
        parsed_date = datetime.strptime(date_string, "%Y/%j/%H/%M/%S")

        #     if not lowest_time or parsed_date < lowest_time:
        #         lowest_time = parsed_date
        #
        #     if not highest_time or parsed_date > highest_time:
        #         highest_time = parsed_date
        # print(lowest_time, highest_time)
        # return lowest_time, highest_time
        return parsed_date

@lru_cache()
def day_from_oseberg_path(path: str):
    parts = path.split("/")
    if parts.count("su_files") != 1:
        logger.debug(f"Invalid oseberg file path. Contains more or less than 1 ocurance of 'su_files' ")
        return False

    day_string = parts[parts.index("su_files") + 1]
    strip_date = day_string.split("_")[1]
    year = strip_date[0:4]
    month = strip_date[4:6]
    day = strip_date[6:]

    return datetime(int(year), int(month), int(day))


DAY_IN_REQ = True
LAST_CHECKED_DAY = None


def day_in_requested(file_day, requested_times):
    global DAY_IN_REQ
    global LAST_CHECKED_DAY
    # Workaround for cache
    if LAST_CHECKED_DAY and file_day == LAST_CHECKED_DAY:
        return DAY_IN_REQ

    for event in requested_times:
        event_from_day = event["from"].strftime("%j")
        event_to_day = event["to"].strftime("%j")
        file_cover_day = file_day.strftime("%j")
        if event_from_day <= file_cover_day <= event_to_day:
            DAY_IN_REQ = True
            LAST_CHECKED_DAY = file_day
            return True

    DAY_IN_REQ = False
    LAST_CHECKED_DAY = file_day
    return False


def filter_oseberg_file_on_day_from_path(path: Path, requested_times) -> bool:
    day = day_from_oseberg_path(str(path.parent.absolute()))
    if not day:
        return False
    return day_in_requested(day, requested_times)

def su_path_to_dates(path: Path):
    # Some simple format checks
    if path.suffix != ".su":
        logger.debug(f"{path.absolute()} is PROBABLY not a seismic unix file. Only checked file suffix.")
        return
    file_from = timerange_of_su_file(str(path.absolute()))

    # TODO: This assumes the su-file spans 9 seconds
    return {"path": path, "from": file_from, "to": file_from + timedelta(seconds=9)}


if __name__ == '__main__':
    requested_times = load_requested_times("../../requested-times.csv")
    # requested_times = {i: value for i, value in enumerate(requested_times)}
    p = str(Path('test_data/oseberg/su_files/Passive_20200624_000000/production/440881.su').parent.absolute())
    day = day_from_oseberg_path(p)
    day_in_req = day_in_requested(day, requested_times)
    print(123)
