# src/db.py
import os
import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

def _dsn():
    return (
        f"dbname={os.getenv('DB_NAME','postgres')} "
        f"user={os.getenv('DB_USER','postgres')} "
        f"password={os.getenv('DB_PASSWORD','postgres')} "
        f"host={os.getenv('DB_HOST','localhost')} "
        f"port={os.getenv('DB_PORT','5432')}"
    )

@contextmanager
def get_cursor():
    with psycopg.connect(_dsn()) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            yield cur
            conn.commit()
