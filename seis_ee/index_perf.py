#! /usr/bin/env python

from datetime import datetime
from pathlib import Path

from seis_ee.index import create_connection, create_index, DB_TABEL


def list_from_fs(location):
    logger.info(f"Listing all files in '{location}'...")
    start = datetime.now()
    path = Path(location)
    files = [x for x in path.rglob("*") if x.is_file()]
    done = datetime.now() - start
    logger.info(f"Done! Took {done} to list all {len(files)} files in '{location}'")


def list_from_db():
    logger.info(f"Fetching all indexes...")
    start = datetime.now()
    connection = create_connection()
    cursor = connection.cursor()

    query = f""" SELECT * from {DB_TABEL};"""

    cursor.execute(query)
    rows = cursor.fetchall()
    done = datetime.now() - start
    logger.info(f"Done! Took {done} to fetch {len(rows)} entries")
    pass


if __name__ == '__main__':
    logger.info("-----------------------------------")
    create_index("/home/stig/speil/Music")
    logger.info("-----------------------------------")
    list_from_db()
    logger.info("-----------------------------------")
    list_from_fs("/home/stig/speil/Music")
    logger.info("-----------------------------------")
