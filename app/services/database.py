import os
import sqlite3
from sqlite3 import Error
from typing import List

from classes.stream_file import StreamFile


class Database:
    DB_TABLE = "stream_files"

    def __init__(self):
        try:
            self.connection = sqlite3.connect(f"{os.getcwd()}/sqlite.db")
            cursor = self.connection.cursor()
            sql_create_table = f""" CREATE TABLE IF NOT EXISTS {self.DB_TABLE} (
                                                        path text PRIMARY KEY,
                                                        decimated BOOLEAN,
                                                        transferred BOOLEAN,
                                                        decimated_path text,
                                                        format text,
                                                        file_date text
                                                    ); """
            cursor.execute(sql_create_table)
        except Error as e:
            raise Exception(e)

    def insert(self, file: StreamFile):
        print(f"Inserting '{file.path}'")
        query = f""" INSERT INTO {self.DB_TABLE} (path, decimated, transferred, decimated_path, format, file_date)
                    VALUES(?,?,?,?,?,datetime('now')); """

        cursor = self.connection.cursor()
        cursor.execute(query, file.to_tuple())
        self.connection.commit()
        return cursor.lastrowid

    def update(self, file: StreamFile):
        sql = f''' UPDATE {self.DB_TABLE}
                  SET decimated = ? ,
                      transferred = ?,
                      decimated_path = ?
                  WHERE path = ?'''
        cursor = self.connection.cursor()
        cursor.execute(sql, (file.decimated, file.transferred, file.decimated_path, file.path))
        self.connection.commit()

    def select(self, path: str):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {self.DB_TABLE} WHERE path=?", (path,))

        rows = cursor.fetchall()

        return rows

    def select_all_paths(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT path FROM {self.DB_TABLE}")

        rows = cursor.fetchall()

        return [r[0] for r in rows]

    def delete_old_rows(self, days: int = 2):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {self.DB_TABLE} WHERE file_date < date('now', '-{days} days');")
        except sqlite3.OperationalError as e:
            print(e)
        self.connection.commit()

    def all_unfinished(self) -> List[StreamFile]:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {self.DB_TABLE} WHERE transferred=FALSE", )

        rows = cursor.fetchall()

        return [StreamFile.from_tuple(row, self) for row in rows]
