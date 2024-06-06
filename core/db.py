"""
db.py
"""

import sqlite3


DEFAULT_DB_PATH = "../data/speech_database.db"


class SQLiteConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()


def execute_query(query, params=(), db_file=DEFAULT_DB_PATH):
    if db_file is None:
        db_file = DEFAULT_DB_PATH

    with SQLiteConnection(db_file) as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
