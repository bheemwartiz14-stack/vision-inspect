import sqlite3
from config.settings import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        register_id TEXT UNIQUE,
        activation_code TEXT,
        activation_expiry TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        password TEXT,
        company_id INTEGER
    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            image_path TEXT,
            status TEXT,
            company_id INTEGER
        )
        """)

    # Sample companies
    cursor.executemany("""
    INSERT OR IGNORE INTO companies (id, name, register_id, activation_code, activation_expiry)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "Alpha Tech", "COMP001", "ACT001", "2026-12-31"),
        (2, "Beta Solutions", "COMP002", "ACT002", "2026-06-30"),
    ])

    conn.commit()
    conn.close()