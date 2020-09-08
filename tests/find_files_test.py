import unittest
from datetime import datetime

from seis_ee.file_finder import find_file


class FindGraneFilesTestCase(unittest.TestCase):
    requested_times = [
        # 10 min
        {"from": datetime(year=2020, month=1, day=1),
         "to": datetime(year=2020, month=1, day=1, hour=0, minute=10)},
        # 2 years
        {"from": datetime(year=2024, month=1, day=1),
         "to": datetime(year=2025, month=1, day=1)},
        # 1 second
        {"from": datetime(year=2020, month=1, day=1),
         "to": datetime(year=2020, month=1, day=1, second=1)},
        # intersection of two files
        {"from": datetime(year=2020, month=1, day=1, second=10),
         "to": datetime(year=2020, month=1, day=1, second=20)},
    ]

    def test_find_grane_files_exact_match(self):
        files = [
            # Exact match
            {"path": "10-minutes.segy", "from": datetime(year=2020, month=1, day=1),
             "to": datetime(year=2020, month=1, day=1, hour=0, minute=10)},
            # TODO: Create a index of files at first run
            # No match
            {"path": "no-match.segy",
             "from": datetime(year=2020, month=1, day=2, hour=0, minute=0, second=0),
             "to": datetime(year=2020, month=1, day=3, hour=0, minute=10, second=0)},
        ]

        expected_result = set(["10-minutes.segy"])

        needed_files = []
        for i in self.requested_times:
            for f in files:
                needed_files.append(find_file(i, f))

        actual_result = set([f for f in needed_files if f])

        assert actual_result == expected_result

    def test_find_grane_within_range(self):
        files = [
            # last second
            {"path": "last-second.segy", "from": datetime(year=2019, month=1, day=1),
             "to": datetime(year=2020, month=1, day=1)},
            # subset
            {"path": "subset.segy",
             "from": datetime(year=2024, month=1, day=2, hour=0, minute=0, second=0),
             "to": datetime(year=2024, month=1, day=3, hour=0, minute=10, second=0)},
            # outside
            {"path": "out-1.segy", "from": datetime(year=2019, month=2, day=1),
             "to": datetime(year=2020, month=3, day=1)},
            # outside
            {"path": "out-2.segy",
             "from": datetime(year=2023, month=1, day=2, hour=0, minute=0, second=0),
             "to": datetime(year=2023, month=1, day=3, hour=0, minute=10, second=0)},
        ]

        expected_result = set(["last-second.segy", "subset.segy"])

        needed_files = []
        for i in self.requested_times:
            for f in files:
                needed_files.append(find_file(i, f))

        actual_result = set([f for f in needed_files if f])

        assert actual_result == expected_result