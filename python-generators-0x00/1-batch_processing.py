#!/usr/bin/env python3
"""
Batch processing using generators:
- stream_users_in_batches(batch_size): yields batches of rows
- batch_processing(batch_size): filters age > 25 and prints users
"""

from typing import Generator, List, Dict
from mysql.connector import Error
import seed


def stream_users_in_batches(batch_size: int) -> Generator[List[Dict], None, None]:
    """
    Yield rows in batches from ALX_prodev.user_data as a list of dicts.
    Uses a single loop and MySQL cursor.fetchmany for batching.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    conn = seed.connect_to_prodev()
    if conn is None:
        raise RuntimeError("Could not connect to ALX_prodev database")

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")
        while True:
            batch = cursor.fetchmany(size=batch_size)
            if not batch:
                break
            yield batch
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def batch_processing(batch_size: int) -> None:
    """
    Process each batch: filter users over age 25 and print them.
    Uses no more than 3 loops total in the script (2 explicit loops here).
    """
    for batch in stream_users_in_batches(batch_size):
        processed = [u for u in batch if int(u.get("age", 0)) > 25]
        for user in processed:
            print(user)