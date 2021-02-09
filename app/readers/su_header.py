from datetime import datetime

import segyio

from utils import logger


def timerange_of_su_file(file_path: str) -> datetime:
    logger.debug(f"Finding timerange of {file_path}...")
    with segyio.su.open(file_path, endian="little", ignore_geometry=True) as f:
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

        return parsed_date
