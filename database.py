import sqlite3
from pathlib import Path

# Database location
DB_FOLDER = Path("db")
DB_PATH = DB_FOLDER / "asset_requests.db"


def init_db():
    """
    Create the database and asset_requests table if they don't exist.
    """
    DB_FOLDER.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asset_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT UNIQUE NOT NULL,
                employee_id TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                justification TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


def save_request(data):
    """
    Save a new asset request.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO asset_requests (
                request_id,
                employee_id,
                asset_type,
                asset_name,
                justification,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["request_id"],
            data["employee_id"],
            data["asset_type"],
            data["asset_name"],
            data["justification"],
            data["status"]
        ))

        conn.commit()


def get_all_requests():
    """
    Retrieve all asset requests.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM asset_requests
            ORDER BY created_at DESC
        """)

        return cursor.fetchall()


def get_request(request_id):
    """
    Retrieve a single request using Request ID.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM asset_requests
            WHERE request_id = ?
        """, (request_id,))

        return cursor.fetchone()


def update_status(request_id, status):
    """
    Update request status.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE asset_requests
            SET status = ?
            WHERE request_id = ?
        """, (status, request_id))

        conn.commit()

        return cursor.rowcount


def delete_request(request_id):
    """
    Delete a request.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM asset_requests
            WHERE request_id = ?
        """, (request_id,))

        conn.commit()

        return cursor.rowcount


if __name__ == "__main__":

    init_db()

    print("✅ Database initialized successfully.")

    rows = get_all_requests()

    if rows:
        print("\nStored Requests:\n")

        for row in rows:
            print(dict(row))
    else:
        print("\nNo requests found.")