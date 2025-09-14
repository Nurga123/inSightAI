import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "database/users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_path TEXT,
            objects TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def create_user(username, password):
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False

def add_history(user_id, image_path, objects_json):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (user_id, image_path, objects) VALUES (?, ?, ?)",
        (user_id, image_path, objects_json)
    )
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT image_path, objects, timestamp FROM history WHERE user_id=? ORDER BY timestamp DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
