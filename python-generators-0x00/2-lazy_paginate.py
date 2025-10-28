#!/usr/bin/env python3
"""
Lazy pagination:
- paginate_users(page_size, offset): returns a page of users as list[dict]
- lazy_pagination(page_size): generator yielding pages lazily
"""

from typing import List, Dict, Generator
import seed


def paginate_users(page_size: int, offset: int) -> List[Dict]:
    """
    Fetch a page of users with given page_size and offset.
    """
    if page_size <= 0 or offset < 0:
        raise ValueError("page_size must be > 0 and offset >= 0")

    connection = seed.connect_to_prodev()
    if connection is None:
        raise RuntimeError("Could not connect to ALX_prodev database")

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}")
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


def lazy_pagination(page_size: int) -> Generator[List[Dict], None, None]:
    """
    Lazily yield pages of users, one page at a time.
    Uses exactly one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size