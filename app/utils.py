import logging
import re
from datetime import datetime
from functools import wraps
from pathlib import Path
from shlex import quote
from settings import FieldStorageContainers

from exceptions import BadInputException

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# Azure SDK logger
az_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
az_logger.setLevel(logging.WARNING)


def timeit(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        start = datetime.now()
        result = f(*args, **kwargs)
        end = datetime.now()
        print(f"func: {f.__name__}, args {args}, {kwargs} took: {end - start}")
        return result

    return wrap


def delete_file(path: str):
    try:
        Path(path).unlink()
    except FileNotFoundError:
        logger.error(f"FileNotFoundError: Failed to delete file: '{path}'")


regex = r"[^a-zA-Z0-9\/\_\-\.]"
pattern = re.compile(regex)


def sanitize_shell_arguments(in_arg: str) -> str:
    match = re.search(pattern, in_arg)
    if match:
        raise BadInputException(f"The string {in_arg} contains invalid characters [{match.group()}]")
    return quote(in_arg)


def is_valid_file_format(file_format: str) -> bool:
    if file_format in [item.value for item in FieldStorageContainers]:
        return True
    else:
        return False
