#!/usr/bin/env python3
"""
Stream users from MySQL using a generator that yields one row at a time.

Prototype:
    def stream_users()

Constraints:
    - Use Python's `yield`
    - No more than one loop
"""

from typing import Generator, Dict
import mysql.connector
from mysql.connector import Error
import seed  # local module


def stream_users() -> Generator[Dict, None, None]:
    """
    Generator that yields rows from ALX_prodev.user_data as dictionaries.
    """
    conn = seed.connect_to_prodev()
    if conn is None:
        raise RuntimeError("Could not connect to ALX_prodev database")

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")
        # Single loop yielding row-by-row
        for row in cursor:
            yield row
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass