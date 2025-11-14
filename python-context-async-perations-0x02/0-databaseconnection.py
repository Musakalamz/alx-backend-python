#!/usr/bin/env python3
"""
Task 0: Custom class-based context manager for SQLite database connections.

This script defines a DatabaseConnection class that manages the opening, 
committing/rolling back, and closing of an sqlite3 connection using the 'with' 
statement.
"""

import sqlite3
import os

# Define the database file name
DB_NAME = 'alx_database.db'


def setup_database():
    """Initializes the database and creates a mock 'users' table."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Create the users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER
            )
        """)
        
        # Insert mock data if the table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            mock_data = [
                ('Alice', 30),
                ('Bob', 24),
                ('Charlie', 45),
                ('David', 20)
            ]
            cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", mock_data)
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


class DatabaseConnection:
    """
    A context manager class to manage an sqlite3 database connection.
    Ensures the connection is opened on entry and closed on exit.
    """
    def __init__(self, db_name):
        """Initializes the context manager with the database name."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Opens the database connection and creates a cursor.
        Returns:
            sqlite3.Cursor: The database cursor object.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"--- Connection to {self.db_name} opened. ---")
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error opening connection: {e}")
            # Ensure resources are closed if __enter__ fails
            self.conn = None
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles resource cleanup, committing or rolling back transaction.

        Args:
            exc_type (Type[BaseException] | None): Type of exception raised.
            exc_val (BaseException | None): The exception instance.
            exc_tb (TracebackType | None): Traceback object.
        """
        if self.conn:
            try:
                if exc_type is None:
                    # No exception, commit the transaction
                    self.conn.commit()
                    print("Transaction committed.")
                else:
                    # Exception occurred, rollback changes
                    self.conn.rollback()
                    print(f"Transaction rolled back due to error: {exc_type.__name__}")
            finally:
                # Always ensure the connection is closed
                self.conn.close()
                print(f"--- Connection to {self.db_name} closed. ---")
        
        # If we return False (or implicitly None), the exception is re-raised.
        # If we return True, the exception is suppressed.
        return False


if __name__ == "__main__":
    setup_database()
    
    print("Executing query using DatabaseConnection context manager:")
    try:
        # Use the context manager to execute a query
        with DatabaseConnection(DB_NAME) as cursor:
            # The database operation within the 'with' block
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            print("\nQuery Results (SELECT * FROM users):")
            for row in results:
                print(row)

    except Exception as e:
        print(f"\nAn error occurred outside the context manager's __exit__ (if not suppressed): {e}")

    # Check if the file was deleted for cleanup (optional, but good practice)
    # The requirement does not ask for file deletion, just connection closure.

