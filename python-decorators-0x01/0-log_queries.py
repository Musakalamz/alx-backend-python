#!/usr/bin/env python3
"""
Task 0: Logging Database Queries

Create a decorator log_queries that logs SQL queries before executing them.
"""

import sqlite3
import functools


def log_queries(func):
    """Decorator that logs SQL queries before execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else "")
        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)