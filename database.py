import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ocorrencias.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_ocorrencia TEXT NOT NULL,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                solucao_provisoria TEXT DEFAULT '',
                solucao_definitiva TEXT DEFAULT '',
                nome_usuario TEXT NOT NULL,
                data_hora_registro TEXT NOT NULL
            )
            """
        )