import sqlite3
import time

DB_NAME = 'test_perf.db'
NUM_RECORDS = 1_000_000

def setup_database():
    """Create a fresh database and populate with dummy tasks."""
    conn = sqlite3.connect(DB_NAME)
    with conn:
        conn.execute('DROP TABLE IF EXISTS tasks')
        conn.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        tasks = [(f"Task {i}",) for i in range(NUM_RECORDS)]
        conn.executemany('INSERT INTO tasks (task) VALUES (?)', tasks)
    conn.close()

def fetch_without_row_factory():
    conn = sqlite3.connect(DB_NAME)
    start = time.perf_counter()
    rows = conn.execute('SELECT id, task, completed FROM tasks').fetchall()
    total = 0
    for row in rows:
        # Access by index
        total += row[0] + row[2]
    end = time.perf_counter()
    conn.close()
    return end - start

def fetch_with_row_factory():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    start = time.perf_counter()
    rows = conn.execute('SELECT id, task, completed FROM tasks').fetchall()
    total = 0
    for row in rows:
        # Access by column name
        total += row["id"] + row["completed"]
    end = time.perf_counter()
    conn.close()
    return end - start

if __name__ == '__main__':
    setup_database()

    time_no_factory = fetch_without_row_factory()
    print(f"Without row_factory: {time_no_factory:.5f} seconds")

    time_with_factory = fetch_with_row_factory()
    print(f"With row_factory: {time_with_factory:.5f} seconds")

    if time_with_factory > time_no_factory:
        slowdown = ((time_with_factory / time_no_factory) - 1) * 100
        print(f"Row factory is about {slowdown:.2f}% slower.")
    else:
        print("Row factory was faster (rare).")
