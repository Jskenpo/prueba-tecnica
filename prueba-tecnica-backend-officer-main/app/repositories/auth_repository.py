from datetime import datetime, timezone

from app.database.engine import get_connection


def init_users_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def create_user(username: str, hashed_password: str):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, hashed_password, datetime.now(timezone.utc).isoformat()),
        )
        return {"id": cursor.lastrowid, "username": username}


def find_user_by_username(username: str):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    return dict(row) if row else None


def find_user_by_id(user_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return dict(row) if row else None
