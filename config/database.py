import os
import sqlite3
import stat
from config.settings import DB_PATH


def init_db():
    try:
        # 1. Create folder
        folder = os.path.dirname(DB_PATH)
        os.makedirs(folder, exist_ok=True)
        # 2. Set folder permission (Linux only)
        if os.name != "nt":
            os.chmod(folder, stat.S_IRWXU)  # 700
        # 3. Connect DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # 4. Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            status TEXT,
            synced INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()

        # 5. Set DB permission (Linux only)
        if os.name != "nt":
            os.chmod(DB_PATH, stat.S_IRUSR | stat.S_IWUSR)  # 600

        print("✅ DB Ready:", DB_PATH)

    except Exception as e:
        print("❌ DB Init Error:", str(e))