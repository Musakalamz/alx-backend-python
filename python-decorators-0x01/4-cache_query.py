#!/usr/bin/env python3
"""
Task 4: Cache Database Queries
Cache results of SQL queries to avoid redundant database calls.
"""

import sqlite3
import functools

query_cache = {}


def with_db_connection(func):
    """Decorator to automatically manage database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator that caches query results based on the SQL string."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or ""
        if query in query_cache:
            print("Fetching from cache...")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("Query result cached.")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users with caching support."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)