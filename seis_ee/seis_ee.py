#! /usr/bin/env python
import os

import click

from config import Config
from extractors.decimate import decimate_files
from file_finder import file_finder
from utils import logger


@click.group()
@click.option("--log-level", "-l", default="info", type=click.Choice(['info', 'warning', 'error'], case_sensitive=False),
              help="Log level. One of 'info', 'warning', 'error'")
def cli(log_level):
    logger.setLevel(log_level.upper())
    pass


@cli.command()
@click.option("--target", "-t", default=os.getcwd(), type=str, help="Location of files to find. Default '.'")
@click.option("--events", "-e", required=True, type=str, help="CSV-file with time ranges for the events to find.")
@click.option("--format", type=click.Choice(Config.find_files_format, case_sensitive=False), default="filename",
              help=f"How to find the time range covered by the file. Valid formats are {Config.find_files_format}")
def find_files(target, events, format):
    file_finder(target, events, format)


# @cli.command()
# @click.option("-f", "--file-list", type=str,
#               help="Path to a file containing files to copy. Every file separated with newline")
# @click.option("--format", type=click.Choice(["segd-grane", "su-oseberg"], case_sensitive=False),
#               help="Format of the files to reduce. One of (segd-grane, su-oseberg)")
# def copy_files(file_list, format):
#     _copy_files(file_list, format)


@cli.command()
@click.option("-f", "--file-list", type=str,
              help="Path to a file containing files to reduce. Every file separated with newline")
@click.option("-s", "--sensor-list", type=str,
              help="Path to a file containing the sensors to keep. Separated with newline.")
@click.option("--format", type=click.Choice(Config.reduce_files_options, case_sensitive=False),
              help=f"Format of the files to reduce. One of {Config.reduce_files_options}")
def reduce_files(file_list, sensor_list, format):
    decimate_files(file_list, sensor_list, format)


if __name__ == '__main__':
    cli()
