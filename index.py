import os
import sqlite3
from pathlib import Path
from sqlite3 import Error
from typing import Dict, List

import click

DB_TABEL = "file_index"


def create_connection():
    """ create a database connection to a SQLite database """
    try:
        return sqlite3.connect("./sqlite.db")
    except Error as e:
        print(e)
        raise Exception(e)


def insert_index(connection, index: List[Dict]):
    print(f"Will insert values; {index}")
    values = [f'(\"{i}\", \"test\", \"test\")' for i in index]
    linked = ", ".join(values)

    query = f""" INSERT INTO {DB_TABEL} (path, start_date, end_date) VALUES {linked}; """

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    print("Done!")
    return cursor.lastrowid


@click.command()
def create_index():
    os.remove("sqlite.db")

    connection = create_connection()
    cursor = connection.cursor()

    sql_create_table = f""" CREATE TABLE IF NOT EXISTS {DB_TABEL} (
                                            path text PRIMARY KEY,
                                            start_date text NOT NULL,
                                            end_date text NOT NULL
                                        ); """

    cursor.execute(sql_create_table)
    print("Created SQL tabel")
    path = Path("./test_data")
    index = [str(x.absolute()) for x in path.rglob("*") if x.is_file()]

    insert_index(connection, index)


if __name__ == '__main__':
    create_index()
