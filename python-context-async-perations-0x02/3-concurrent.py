#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries (3-concurrent.py)

This script demonstrates running multiple database queries concurrently using
asyncio.gather() and aiosqlite.
"""

import asyncio
import aiosqlite

DB_NAME = "alx_database.db"


async def async_fetch_users():
    """Fetches all users from the database asynchronously."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """Fetches users older than 40 from the database asynchronously."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Runs both asynchronous fetch functions concurrently using asyncio.gather()."""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    all_users = results[0]
    older_users = results[1]

    for user in all_users:
        print(user)
    print("---")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())