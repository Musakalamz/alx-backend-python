#!/usr/bin/env python3
"""
Task 1: Reusable Context Manager for Query Execution.

This script defines an ExecuteQuery class that takes a query and parameters 
as input, manages the database connection, executes the query, and returns 
the results.
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
                ('David', 20),
                ('Eve', 35),
                ('Frank', 50)
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


class ExecuteQuery:
    """
    A context manager to manage database connection and execute a single query.
    The query results are returned upon entering the 'with' block.
    """
    def __init__(self, db_name, query, params=()):
        """
        Initializes the context manager.

        Args:
            db_name (str): The database file name.
            query (str): The SQL query string.
            params (tuple): Parameters to substitute into the query.
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        """
        Opens connection, executes the query, and stores results.

        Returns:
            list: The fetched results from the query execution (e.g., cursor.fetchall()).
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            
            print(f"--- Connection to {self.db_name} opened. ---")
            
            # Execute the query with parameters
            cursor.execute(self.query, self.params)
            
            # Fetch results only if it's a SELECT query
            if self.query.strip().upper().startswith('SELECT'):
                self.results = cursor.fetchall()
            else:
                # For non-SELECT queries (e.g., UPDATE, INSERT), commit immediately
                self.conn.commit()
                self.results = []
                
            return self.results
            
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            # Ensure rollback if execution fails
            if self.conn:
                self.conn.rollback()
            self.conn = None # Set to None to prevent __exit__ from closing a non-existent connection
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles resource cleanup and closes the connection.
        """
        if self.conn:
            # Commit only if there was no exception and it wasn't a SELECT 
            # (non-SELECT queries were committed in __enter__)
            if exc_type is None and not self.query.strip().upper().startswith('SELECT'):
                self.conn.commit()
            
            self.conn.close()
            print(f"--- Connection to {self.db_name} closed. ---")
            
        return False # Do not suppress exceptions


if __name__ == "__main__":
    setup_database()

    # The required query: "SELECT * FROM users WHERE age > ?" with parameter 25
    query = "SELECT * FROM users WHERE age > ?"
    age_limit = (25,) # Note the comma for the single-item tuple

    print(f"Executing query: '{query}' with parameter {age_limit[0]}")
    try:
        # Use the context manager to execute the query
        with ExecuteQuery(DB_NAME, query, age_limit) as filtered_users:
            print("\nQuery Results (Users older than 25):")
            if filtered_users:
                for row in filtered_users:
                    print(row)
            else:
                print("No users found matching the criteria.")

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")

