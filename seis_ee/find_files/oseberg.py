from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from readers.su_header import timerange_of_su_file
from utils import logger


def zero_pad_day(day: int) -> str:
    if day == 0 or day > 31:
        raise ValueError(f"Invalid day or month! Got {day}...")
    as_string = str(day)
    if len(as_string) == 1:
        return f"0{as_string}"

    return as_string


def zero_or_one_day(target: Path) -> bool:
    day0 = "_000000"
    day1 = "_000001"
    zero_exists = Path(str(target) + day0).exists()
    one_exists = Path(str(target) + day1).exists()

    if zero_exists and one_exists:
        raise ValueError(f"Both folders {day0} and {day1} exists at target {target}")

    if zero_exists:
        return False
    if one_exists:
        return True

    raise ValueError(f"No day folder exists for {target}")


def _find_file(first_file: Path, requested_time: datetime, search_path):
    found_file = first_file
    file_time = timerange_of_su_file(str(found_file))
    counter = 0

    while not requested_time == file_time:
        time_delta = requested_time - file_time
        # Files can be placed in wrong folder. Try getting new path with day offset:
        if time_delta > timedelta(days=1):
            new_day_folder = _datetime_to_oseberg_path(requested_time, search_path, 1)
            new_first_file = _find_first_file_in_folder(new_day_folder)
            return _find_file(new_first_file, requested_time, search_path)
        offset = int((time_delta.total_seconds() / 10))
        file_stem = str(int(found_file.stem) + offset)
        found_file = Path(found_file.parent, f"{file_stem}.su")
        if not found_file.exists():
            logger.warning(f"Missing file {found_file}...Skipping")
            return None, None

        file_time = timerange_of_su_file(str(found_file))
        counter += 1
        if counter > 10:
            # Could not find a file with exact time match. Will use best match. (Timedelta < 10sec)
            if offset == 0:
                logger.warning(f"Not exact match. Requested: {requested_time} File-time: {file_time}. Using this...")
                return found_file, file_time
            logger.warning(f"Missing file {found_file}...Skipping")
            return None, None

    logger.info(f"Found file for {requested_time}: {found_file} with time; {file_time}")
    return found_file, file_time


def _datetime_to_oseberg_path(time, prefix, day_offset=0) -> Path:
    # Takes a DateTime object, and return a Path to where the Oseberg su-file should be
    month = f"OsebergC-SWIM_{zero_pad_day(time.month)}/su_files"
    day = f"Passive_{str(time.year)}{zero_pad_day(time.month)}{zero_pad_day(time.day + day_offset)}"

    # The day folder can end with ether 0 or 1, with no way of knowing
    if zero_or_one_day(Path(prefix, month, day)):
        day = day + "_000001"
    else:
        day = day + "_000000"

    path_to_start = Path(prefix, month, day)
    return path_to_start


def _find_first_file_in_folder(folder: Path) -> Path:
    files = folder.rglob("*")
    t = [str(f) for f in files if f.suffix == ".su"]
    t.sort()
    first_file = Path(t[0])
    return first_file


def datetime_to_oseberg_path(time: datetime, target: Path):
    """
    The folder structure is static, and the first file in every folder starts at midnight (NOT CORRECT).
    We find name of the first file, calculate requested offset, and find path with requested times.
    """
    path_to_start = _datetime_to_oseberg_path(time, target)
    first_file = _find_first_file_in_folder(path_to_start)

    req_file, file_time = _find_file(Path(first_file), time, target)

    return req_file, file_time


def oseberg_path_to_date(path: str) -> datetime:
    parts = path.split("/")
    start_index = [i for i, part in enumerate(parts) if 'OsebergC-SWIM' in part][0]
    month = int(parts[start_index].split("_")[1])
    dategroup = parts[start_index + 2].split("_")[1]
    year = int(dategroup[:4])
    day = int(dategroup[6:8])
    return datetime(year=year, month=month, day=day)


def round_to_10_sec_range(time: datetime) -> datetime:
    seconds = time.second
    last_second = int(str(seconds)[-1])
    diff = 9 - last_second
    return time + timedelta(seconds=diff)


def requested_times_to_oseberg_chunks(requested_times):
    new_requested_times = []
    for i in requested_times:
        start = round_to_10_sec_range(i["from"])
        end = round_to_10_sec_range(i["to"])
        chunk = {"event": i["event"], "chunk": start}
        new_requested_times.append(chunk)

        while chunk["chunk"] < end:
            chunk = {"event": i["event"], "chunk": chunk["chunk"] + timedelta(seconds=10)}
            new_requested_times.append(chunk)

    return new_requested_times


def requested_times_to_oseberg_paths(requested_times, target) -> [Path]:
    time_chunks = requested_times_to_oseberg_chunks(requested_times)
    paths = []
    for chunk in time_chunks:
        path, file_time = datetime_to_oseberg_path(chunk["chunk"], target)
        paths.append({"path": path, "file_time": file_time, "event": chunk["event"]})

    return paths, len(paths)


def files_in_todays_directory() -> List[Path]:
    date = datetime.now()
    path = _datetime_to_oseberg_path(date, "/home/stig/git/seis-ee/test_data")
    print(path)
    target = Path(path)
    files = [x for x in target.rglob("*") if x.is_file()]
    return files


if __name__ == '__main__':
    oseberg_path_to_date(
        "/test_data/OsebergC-SWIM_01/su_files/Passive_20210120_000001/production/2.su")
