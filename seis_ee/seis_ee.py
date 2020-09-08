#! /usr/bin/env python
import os

import click

from extractors.decimate import decimate_files
from file_finder import file_finder


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
@click.option("-s", "--sensor-list", type=str,
              help="Path to a file containing the sensors to keep. Separated with newline.")
@click.option("-f", "--file-list", type=str,
              help="Path to a file containing files to reduce. Every file separated with newline")
def reduce_files(file_list, sensor_list):
    decimate_files(file_list, sensor_list)


if __name__ == '__main__':
    cli()
