import logging

import click

logger = logging.getLogger("logger")


def print_help_and_exit():
    ctx = click.get_current_context()
    print(ctx.get_help())
    exit(1)
