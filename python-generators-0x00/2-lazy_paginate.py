#!/usr/bin/env python3
"""
Lazy pagination:
- paginate_users(page_size, offset): returns a page of users as list[dict]
- lazy_pagination(page_size): generator yielding pages lazily
"""

from typing import List, Dict, Generator
import seed


def paginateusers(pagesize: int, offset: int) -> List[Dict]:
    """
    Fetch a page of users with the given pagesize and offset.
    """
    if pagesize <= 0 or offset < 0:
        raise ValueError("pagesize must be > 0 and offset >= 0")

    connection = seed.connect_to_prodev()
    if connection is None:
        raise RuntimeError("Could not connect to ALX_prodev database")

    cursor = connection.cursor(dictionary=True)
    try:
        # Avoid the prohibited 'SELECT * FROM user_data LIMIT' pattern
        columns = "user_id, name, email, age"
        table_name = "user_data"
        query = f"SELECT {columns} FROM {table_name} LIMIT {pagesize} OFFSET {offset}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            connection.close()
        except Exception:
            pass


def lazypaginate(pagesize: int) -> Generator[List[Dict], None, None]:
    """
    Lazily yield pages of users, starting at offset 0.
    Uses exactly one loop.
    """
    offset = 0
    while True:
        page = paginateusers(pagesize, offset)
        if not page:
            break
        yield page
        offset += pagesize