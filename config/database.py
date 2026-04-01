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
            (3, "Gamma Industries", "COMP003", "ACT003", "2025-12-31"),
            (4, "Delta Corp", "COMP004", "ACT004", "2026-03-31"),
            (5, "Epsilon Systems", "COMP005", "ACT005", "2024-12-31"),  # expired
            (6, "Zeta Labs", "COMP006", "ACT006", "2027-01-01"),
            (7, "Eta Innovations", "COMP007", "ACT007", "2026-08-15"),
            (8, "Theta Enterprises", "COMP008", "ACT008", "2025-05-01"),
            (9, "Iota Group", "COMP009", "ACT009", "2026-11-20"),
            (10, "Kappa Technologies", "COMP010", "ACT010", "2023-12-31")  # expired
        ])

    conn.commit()
    conn.close()