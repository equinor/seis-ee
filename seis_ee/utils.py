import csv
import logging
import os
from datetime import datetime
from functools import wraps

import click

logger = logging.getLogger("seis_ee")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def print_help_and_exit():
    ctx = click.get_current_context()
    print(ctx.get_help())
    exit(1)


def timeit(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        start = datetime.now()
        result = f(*args, **kwargs)
        end = datetime.now()
        print(f"func: {f.__name__}, args {args}, {kwargs} took: {end - start}")
        return result

    return wrap


def load_requested_times(input = f"{os.getcwd()}/requested-times.csv"):
    time_objects = []
    with open(input) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=" ")
        for i, row in enumerate(reader):
            # Skip empty rows
            if not row:
                continue
            r_event = datetime.fromisoformat(row["event"])
            r_from = datetime.fromisoformat(row["from"])
            r_to = datetime.fromisoformat(row["to"])

            # Test for invalid range (from larger than to)
            if r_from >= r_to:
                logger.warning(f"row {i} is invalid. From date is ending before to date. Skipping...")
                continue
            time_objects.append({"event": r_event,
                                 "from": r_from,
                                 "to": r_to})
    return time_objects