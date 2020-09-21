from datetime import datetime, timedelta
from pathlib import Path

from find_files.su_header import timerange_of_su_file
from utils import load_requested_times, logger


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


def _find_file(first_file: Path, requested_time: datetime) -> Path:
    found_file = first_file
    file_time = timerange_of_su_file(str(found_file))
    counter = 0

    while not requested_time == file_time:
        # while not requested_time + timedelta(seconds=9) >= file_time >= requested_time - timedelta(seconds=9):
        time_delta = requested_time - file_time
        offset = int((time_delta.total_seconds() / 10))
        file_stem = str(int(found_file.stem) + offset)
        found_file = Path(found_file.parent, f"{file_stem}.su")
        if not found_file.exists():
            logger.warning(f"Missing file {found_file}...Skipping")
            return None, None

        file_time = timerange_of_su_file(str(found_file))
        counter += 1
        if counter > 10:
            logger.warning(f"Missing file {found_file}...Skipping")
            return None, None

    logger.info(f"Found file for {requested_time}: {found_file} with time; {file_time}")
    return found_file, file_time


def datetime_to_oseberg_path(time: datetime, target: Path) -> str:
    """
    The folder structure is static, and the first file in every folder starts at midnight.
    We find name of the first file, calculate requested offset, and find path with requested times.
    """
    month = f"OsebergC-SWIM_{zero_pad_day(time.month)}/su_files"
    day = f"Passive_{str(time.year)}{zero_pad_day(time.month)}{zero_pad_day(time.day)}"

    # The day folder can end with ether 0 or 1, with no way to know
    if zero_or_one_day(Path(target, month, day)):
        day = day + "_000001"
    else:
        day = day + "_000000"

    path_to_start = Path(target, month, day)
    files = path_to_start.rglob("*")
    t = [str(f) for f in files if f.suffix == ".su"]
    t.sort()
    first_file = Path(t[0]).stem

    req_file, file_time = _find_file(Path(t[0]), time)

    return req_file, file_time


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

    return paths


if __name__ == '__main__':
    times = load_requested_times()
    time_chunks = requested_times_to_oseberg_chunks(times)
    paths = requested_times_to_oseberg_paths(time_chunks, "/project")
    print(123)
