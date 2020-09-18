from datetime import datetime
from typing import Tuple

import segyio


def timerange_of_su_file(file_path: str) -> Tuple[datetime, datetime]:
    with segyio.su.open(file_path, endian="little", ignore_geometry=True) as f:
        lowest_time = None
        # TODO: This is redundant as we now just assume a 8sec time span
        highest_time = None

        # Documented here; https://segyio.readthedocs.io/en/latest/segyio.html#trace-header-keys
        # TODO: Might not be needed to check every header(?)
        for header in f.header:
            year = header[157]
            day = header[159]
            hour = header[161]
            minute = header[163]
            second = header[165]

            date_string = f"{year}/{day}/{hour}/{minute}/{second}"
            parsed_date = datetime.strptime(date_string, "%Y/%j/%H/%M/%S")

            if not lowest_time or parsed_date < lowest_time:
                lowest_time = parsed_date

            if not highest_time or parsed_date > highest_time:
                highest_time = parsed_date

        return lowest_time, highest_time


if __name__ == '__main__':
    timerange_of_su_file("/home/stig/git/seis-ee/test_data/oseberg/514992.su")
