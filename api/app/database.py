import os
import sqlite3
from pathlib import Path

from .models import SCHEMA

ROOT = Path(__file__).resolve().parents[2]


def connect():
    path = Path(os.environ.get("FLOODRISK_DB", "storage/floodrisk.db"))
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize():
    connection = connect()
    try:
        with connection:
            connection.executescript(SCHEMA)
    finally:
        connection.close()


def fetch_all(sql, parameters=()):
    connection = connect()
    try:
        return [dict(row) for row in connection.execute(sql, parameters).fetchall()]
    finally:
        connection.close()
