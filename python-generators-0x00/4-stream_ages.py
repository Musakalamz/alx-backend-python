#!/usr/bin/env python3
"""
Memory-efficient aggregation:
- stream_user_ages(): generator yielding user ages one by one
- average_age(): computes and prints average age without SQL AVG
"""

from typing import Generator
import seed


def stream_user_ages() -> Generator[int, None, None]:
    """
    Yield user ages one by one from the database.
    Loop #1: iterate over rows yielding ages.
    """
    conn = seed.connect_to_prodev()
    if conn is None:
        raise RuntimeError("Could not connect to ALX_prodev database")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT age FROM user_data;")
        for (age,) in cursor:
            yield int(age)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def average_age() -> None:
    """
    Compute and print the average age without loading entire dataset.
    Loop #2: single pass aggregation.
    """
    count = 0
    total = 0
    for age in stream_user_ages():
        total += age
        count += 1

    avg = (total / count) if count else 0.0
    print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    average_age()