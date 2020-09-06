import os
import sqlite3
from datetime import datetime
from pathlib import Path
from sqlite3 import Error
from typing import Dict, List

DB_TABEL = "file_index"


def create_connection():
    """ create a database connection to a SQLite database """
    try:
        return sqlite3.connect("./sqlite.db")
    except Error as e:
        print(e)
        raise Exception(e)


def insert_index(connection, index: List[Dict]):
    print(f"Will insert {len(index)} values...")
    values = [f'(\"{i}\", \"test\", \"test\")' for i in index]
    linked = ", ".join(values)

    query = f""" INSERT INTO {DB_TABEL} (path, start_date, end_date) VALUES {linked}; """

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return cursor.lastrowid


def create_index(location):
    print(f"Creating index of files in '{location}'")
    start = datetime.now()
    try:
        os.remove("sqlite.db")
    except FileNotFoundError:
        pass

    connection = create_connection()
    cursor = connection.cursor()

    sql_create_table = f""" CREATE TABLE IF NOT EXISTS {DB_TABEL} (
                                            path text PRIMARY KEY,
                                            start_date text NOT NULL,
                                            end_date text NOT NULL
                                        ); """

    cursor.execute(sql_create_table)
    print("Created SQL tabel")
    path = Path(location)
    index = [str(x.absolute()) for x in path.rglob("*") if x.is_file()]

    insert_index(connection, index)
    done = datetime.now() - start
    print(f"Done! Took {done} to crate index with {len(index)} entries")


if __name__ == '__main__':
    create_index("./test_data")
