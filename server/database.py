"""Simple SQLite-backed Database helper exposing a Database class.

This module keeps backwards-compatible module-level functions (`init_db`,
`save_message`, `get_messages`) which delegate to a default `Database`
instance. Callers that prefer an explicit instance can use `Database()`.
"""
from __future__ import annotations

import sqlite3
import pathlib
from typing import List, Tuple, Optional


DEFAULT_DB_NAME = 'chat_app.db'


class Database:
    def __init__(self, db_path: Optional[str] = None):
        base = pathlib.Path(__file__).resolve().parent
        if db_path:
            self.db_path = pathlib.Path(db_path)
        else:
            self.db_path = base / DEFAULT_DB_NAME

    def _connect(self):
        return sqlite3.connect(str(self.db_path))

    def init_db(self) -> None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'''
        )
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS messages
               (id INTEGER PRIMARY KEY, sender TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)'''
        )
        conn.commit()
        conn.close()

    def save_message(self, sender: str, content: str) -> None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (sender, content) VALUES (?, ?)", (sender, content)
        )
        conn.commit()
        conn.close()

    def get_messages(self, limit: int = 100) -> List[Tuple[int, str, str, str]]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, sender, content, timestamp FROM messages ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
    def init_db() -> None:
        return _default_db.init_db()


    def save_message(sender: str, content: str) -> None:
        return _default_db.save_message(sender, content)


    def get_messages(limit: int = 100) -> List[Tuple[int, str, str, str]]:
        return _default_db.get_messages(limit)


# tạo một instance mặc định để các hàm module-level có thể sử dụng
_default_db = Database()




if __name__ == "__main__":
    _default_db.init_db()
    print("Database initialized!")