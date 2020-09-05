import unittest
from datetime import datetime, timedelta
from pathlib import Path

from ee import grane_path_to_dates


class PathToDates(unittest.TestCase):

    def test_grane_paths_to_dates(self):
        path = Path("/test/2020-01-01-01-01-01-Grane2163059")

        first_date = datetime(2020, 1, 1, 1, 1, 1)
        expected_result = {"path": path, "from": first_date, "to": first_date + timedelta(seconds=8)}

        actual_result = grane_path_to_dates(path)

        assert actual_result == expected_result
