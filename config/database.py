import os
import stat
from pysqlcipher3 import dbapi2 as sqlite
from config.settings import DB_PATH
from lib.utils import generate_secure_key
def init_db():
    folder = os.path.dirname(DB_PATH)
    os.makedirs(folder, exist_ok=True)
    os.chmod(folder, stat.S_IRWXU)
    conn = sqlite.connect(DB_PATH)
    cursor = conn.cursor()
    secure_key = generate_secure_key()
    cursor.execute(f"PRAGMA key='{secure_key}'")
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
    os.chmod(DB_PATH, stat.S_IRUSR | stat.S_IWUSR)
    print("🔐 Encrypted DB Ready")