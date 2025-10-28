# Python Generators – Streaming from MySQL

This project introduces efficient data processing using Python generators. You’ll seed a MySQL database and implement a generator that streams rows one by one.

## Files

- `seed.py`: Creates `ALX_prodev` DB, `user_data` table, and inserts from `user_data.csv`.
- `0-stream_users.py`: Provides a `stream_users()` generator that yields dict rows.
- `user_data.csv`: Place the provided CSV in this folder.

## MySQL Setup

- Ensure MySQL Server is running and accessible.
- Optionally set environment variables:
  - `MYSQL_HOST` (`localhost`)
  - `MYSQL_PORT` (`3306`)
  - `MYSQL_USER` (`root`)
  - `MYSQL_PASSWORD` (empty by default)

## Install Driver

```bash
pip install mysql-connector-python
```

## Seed the Database (example harness)

Create `0-main.py` next to `seed.py`:

```python
#!/usr/bin/env python3
seed = __import__('seed')
connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    connection = seed.connect_to_prodev()
    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')

        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
```

Run:

```bash
python c:\Users\USER\OneDrive\Desktop\alx-backend-python\python-generators-0x00\0-main.py
```

## Stream Rows (example harness)

Create `1-main.py` next to `0-stream_users.py`:

```python
#!/usr/bin/env python3
from itertools import islice
stream_users = __import__('0-stream_users').stream_users

# iterate over the generator function and print only the first 6 rows
for user in islice(stream_users(), 6):
    print(user)
```

Run:

```bash
python c:\Users\USER\OneDrive\Desktop\alx-backend-python\python-generators-0x00\1-main.py
```

## Notes

- `insert_data` uses `INSERT IGNORE` for idempotency (skips existing `user_id`s).
- Table schema:
  - `user_id` `CHAR(36)` (UUID string), `PRIMARY KEY`
  - `name` `VARCHAR(255)` `NOT NULL`
  - `email` `VARCHAR(255)` `NOT NULL`
  - `age` `DECIMAL(5,0)` `NOT NULL`
- The generator uses exactly one loop to yield row dictionaries.
