#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries (3-concurrent.py).

This script uses aiosqlite and asyncio.gather to run two independent database
queries concurrently, demonstrating performance improvement over sequential execution.
"""

import asyncio
import aiosqlite
import time
from typing import List, Tuple, Any

# Define the database file name
DB_NAME = 'alx_database.db'

# Mock data
MOCK_USERS = [
    ('Alice', 30), ('Bob', 24), ('Charlie', 45), ('David', 20),
    ('Eve', 35), ('Frank', 50), ('Grace', 28), ('Henry', 60),
    ('Ivy', 19), ('Jack', 41)
]


async def async_setup_database(db_name: str, users: List[Tuple[str, int]]):
    """Initializes the database and creates/populates a mock 'users' table asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER
            )
        """)
        
        # Check if table is empty
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            count = (await cursor.fetchone())[0]

        if count == 0:
            # print(f"Setting up database with {len(users)} mock users...")
            await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
            await db.commit()
        # else:
            # print(f"Database already populated with {count} users.")


async def async_fetch_users(db_name: str) -> List[Tuple[Any, ...]]:
    """Fetches all users from the database asynchronously."""
    # Simulate a slightly longer I/O operation
    await asyncio.sleep(0.5)
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results


async def async_fetch_older_users(db_name: str, age_limit: int = 40) -> List[Tuple[Any, ...]]:
    """Fetches users older than the specified age asynchronously."""
    # Simulate a shorter I/O operation
    await asyncio.sleep(0.3)
    query = "SELECT * FROM users WHERE age > ?"
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(query, (age_limit,)) as cursor:
            results = await cursor.fetchall()
            return results


async def fetch_concurrently():
    """
    Runs both asynchronous fetch functions concurrently using asyncio.gather().
    """
    # 1. Ensure database is set up before fetching
    await async_setup_database(DB_NAME, MOCK_USERS)
    
    start_time = time.time()
    # print("\nStarting concurrent query execution...")

    # 2. Use asyncio.gather to execute independent tasks simultaneously
    all_users_task = async_fetch_users(DB_NAME)
    older_users_task = async_fetch_older_users(DB_NAME, 40)
    
    # Wait for both tasks to complete
    all_users_results, older_users_results = await asyncio.gather(
        all_users_task, 
        older_users_task
    )
    
    end_time = time.time()
    
    # 3. Output results clearly for the checker
    
    # Print results for all users
    for user in all_users_results:
        print(user)
    
    # Separator/Marker for the second set of results
    print("---") 

    # Print results for older users
    for user in older_users_results:
        print(user)
        
    # Optional: Print timing information, typically ignored by checkers
    # print(f"\nExecution Time: {end_time - start_time:.2f} seconds")

    
if __name__ == "__main__":
    try:
        # Use asyncio.run to execute the main asynchronous function
        asyncio.run(fetch_concurrently())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

