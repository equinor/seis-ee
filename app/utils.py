import logging
from datetime import datetime
from functools import wraps

import click

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