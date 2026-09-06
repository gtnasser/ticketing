import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "occurrences.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS occurrences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                occurrence_date TEXT NOT NULL,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                temporary_solution TEXT DEFAULT '',
                definitive_solution TEXT DEFAULT '',
                username TEXT NOT NULL,
                registered_at TEXT NOT NULL
            )
            """
        )
