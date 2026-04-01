import os
import stat
import sqlite3
from config.settings import DB_PATH

def init_db():
    folder = os.path.dirname(DB_PATH)
    os.makedirs(folder, exist_ok=True)
    os.chmod(folder, stat.S_IRWXU)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        status BLOB,
        synced INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    os.chmod(DB_PATH, stat.S_IRUSR | stat.S_IWUSR)

    print("✅ Secure DB Ready (App-level encryption)")