from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

from utils import logger


def grane_path_to_dates(path: Path):
    # Try splitting the filename
    elements = path.name.split("-")
    if len(elements) < 5:
        logger.debug(f"Skipping file; {str(path)}")
        return

    try:
        first_date = datetime(year=int(elements[0]), month=int(elements[1]), day=int(elements[2]),
                              hour=int(elements[3]), minute=int(elements[4]), second=int(elements[5]))
    except Exception as e:
        logger.info(f"Failed to parse filename into date; {path.name}")
        logger.info(e)
        return
    return {"path": path, "from": first_date, "to": first_date + timedelta(seconds=8)}


def needed_files(target, requested_times):
    target = Path(target)

    files = [x for x in target.rglob("*") if x.is_file()]
    files_as_dates = [grane_path_to_dates(f) for f in files]

    files_as_dates = [x for x in files_as_dates if x]

    needed_files = []
    for i in requested_times:
        for f in files_as_dates:
            result = find_file(i, f)
            if result:
                needed_files.append(result)
    return needed_files


def find_file(time_range, file) -> Dict:
    f_start = file["from"]
    f_end = file["to"]
    req_start = time_range["from"]
    req_end = time_range["to"]

    # Check if either start of file, or end of file is inside requested time range
    if req_start <= f_start <= req_end or req_start <= f_end <= req_end:
        logger.debug(f"Found file! {file['path']} --- Requested: {req_start} ==> {req_end}")
        return {"path": str(file["path"].absolute()), "event": str(time_range["event"])}