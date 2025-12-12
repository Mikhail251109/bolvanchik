import sqlite3
from datetime import datetime

DB_NAME = "stories.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        prompt TEXT,
        story TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_story(user_id, username, prompt, story):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO stories (user_id, username, prompt, story, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, prompt, story, datetime.now().isoformat()))
    conn.commit()
    conn.close()