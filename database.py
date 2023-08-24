import sqlite3
import os

DB_PATH = "users_data.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def setup_db():
    if not os.path.exists(DB_PATH):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    app_id TEXT,
                    app_hash TEXT,
                    phone TEXT,
                    session_file TEXT
                )
            """)

def add_user(username, password):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

def get_user(username):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return cursor.fetchone()

def update_user_data(username, app_id, app_hash, phone, session_file):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET app_id = ?, app_hash = ?, phone = ?, session_file = ?
            WHERE username = ?
        """, (app_id, app_hash, phone, session_file, username))
