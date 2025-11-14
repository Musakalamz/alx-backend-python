#!/usr/bin/env python3
"""
Task 3: Retry Database Queries
Retry failed database operations a configurable number of times before raising an error.
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """Decorator that handles database connection management."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function if it fails due to transient errors."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            print("All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch users with retry on transient errors."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)