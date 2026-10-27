import os
import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection():
    path = os.environ.get("DATABASE_PATH", "data/comercio_exterior.db")
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()
