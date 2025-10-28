#!/usr/bin/env python3
"""
Seed script for MySQL: create ALX_prodev.user_data and load CSV data.

Functions:
- connect_db() -> mysql connection to server (no DB selected)
- create_database(connection) -> create DB ALX_prodev if missing
- connect_to_prodev() -> mysql connection to ALX_prodev
- create_table(connection) -> create user_data if missing
- insert_data(connection, data) -> insert rows from CSV idempotently
"""

import os
import csv
from typing import Optional
import mysql.connector
from mysql.connector import Error

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def _mysql_config():
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
    }


def connect_db() -> Optional[mysql.connector.MySQLConnection]:
    """
    Connect to MySQL server (no database selected).
    Returns a connection or None if connection fails.
    """
    cfg = _mysql_config()
    try:
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
    return None


def create_database(connection) -> None:
    """
    Create database ALX_prodev if it doesn't exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev() -> Optional[mysql.connector.MySQLConnection]:
    """
    Connect directly to ALX_prodev database.
    Returns a connection or None on failure.
    """
    cfg = _mysql_config()
    try:
        conn = mysql.connector.connect(database=DB_NAME, **cfg)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to database {DB_NAME}: {e}")
    return None


def create_table(connection) -> None:
    """
    Create user_data table if it doesn't exist.
    Schema:
      - user_id CHAR(36) PRIMARY KEY (UUID string)
      - name VARCHAR(255) NOT NULL
      - email VARCHAR(255) NOT NULL
      - age DECIMAL(5,0) NOT NULL
    """
    ddl = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,0) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(ddl)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data: str) -> None:
    """
    Insert CSV rows into user_data if they don't exist.

    - data: path to CSV (e.g., 'user_data.csv')
    - CSV must have headers: user_id,name,email,age
    - Uses INSERT IGNORE for idempotency
    """
    csv_path = data
    if not os.path.isabs(csv_path):
        # resolve relative to this file's directory
        csv_path = os.path.join(os.path.dirname(__file__), data)

    if not os.path.exists(csv_path):
        print(f"CSV not found at {csv_path}")
        return

    sql = f"""
    INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s);
    """
    inserted = 0
    try:
        cursor = connection.cursor()
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = row.get("user_id")
                name = row.get("name")
                email = row.get("email")
                age_raw = row.get("age")
                # Coerce age to numeric (DECIMAL(5,0) -> integer ok)
                age = int(str(age_raw).strip())
                cursor.execute(sql, (user_id, name, email, age))
                inserted += cursor.rowcount  # rowcount is 1 for new, 0 for ignored
        connection.commit()
        cursor.close()
        print(f"Inserted {inserted} new row(s)")
    except Error as e:
        print(f"Error inserting data: {e}")
    except Exception as e:
        print(f"Error reading CSV: {e}")