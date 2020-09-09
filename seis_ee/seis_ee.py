#! /usr/bin/env python
import os

import click

from extractors.decimate import decimate_files
from file_finder import file_finder
from copy_files import copy_files as _copy_files


@click.group()
def cli():
    pass


@cli.command()
@click.option("--target", "-t", default=os.getcwd(), type=str, help="Location of files to find. Default '.'")
@click.option("--input", "-i", required=True, type=str, help="CSV-file with time ranges to find.")
@click.option("--format", type=str, default="filename",
              help="How to find the time range covered by the file. Valid formats are 'filename' or 'segy'")
def find_files(target, input, format):
    file_finder(target, input, format)


@cli.command()
@click.option("-f", "--file-list", type=str,
              help="Path to a file containing files to copy. Every file separated with newline")
@click.option("--format", type=str,
              help="Format of the files to reduce. One of (segd-grane, su-oseberg)")
def copy_files(file_list, format):
    _copy_files(file_list, format)

@cli.command()
@click.option("-s", "--sensor-list", type=str,
              help="Path to a file containing the sensors to keep. Separated with newline.")
@click.option("-f", "--file-list", type=str,
              help="Path to a file containing files to reduce. Every file separated with newline")
@click.option("--format", type=str,
              help="Format of the files to reduce. One of (segd-grane, su-oseberg)")
def reduce_files(file_list, sensor_list, format):
    decimate_files(file_list, sensor_list, format)


if __name__ == '__main__':
    cli()
