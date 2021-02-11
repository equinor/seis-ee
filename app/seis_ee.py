#! /usr/bin/env python

import click

from settings import Settings
from streamer import main
from utils import logger


@click.group()
@click.option(
    "--log-level",
    "-l",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error"], case_sensitive=False),
    help="Log level. One of 'info', 'warning', 'error'",
)
def cli(log_level):
    logger.setLevel(log_level.upper())
    pass


# TODO: If we end up with only one command, make that the main file.
@cli.command()
@click.option("-t", "--target", type=str, help="Target destination to stream new files from")
@click.option(
    "-s",
    "--sensor-list",
    type=str,
    help="Path to a CSV-file containing the sensors to keep. Headers (nodeName, nodeNo)",
)
@click.option(
    "--format",
    type=click.Choice(Settings.REDUCE_FILES_OPTIONS, case_sensitive=False),
    help=f"Format of the files to reduce. One of {Settings.REDUCE_FILES_OPTIONS}",
)
@click.option(
    "--file-detection",
    type=click.Choice(Settings.NEW_FILE_DETECTION, case_sensitive=False),
    help="Use either inotify or regular python code for detecting new files",
)
def stream_files(target, sensor_list, format, file_detection):
    main(target, sensor_list, format, file_detection)


if __name__ == "__main__":
    cli()
