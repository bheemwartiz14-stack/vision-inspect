import os
from dotenv import load_dotenv # type: ignore
import uuid
import hashlib
load_dotenv()
APP_TITLE = os.getenv("APP_TITLE")
APP_NAME = APP_TITLE
DB_PATH = os.path.expanduser(os.getenv("DB_PATH"))
BASE_KEY = os.getenv("APP_DB_KEY")
CAMERA_CONFIG = [
    {
        "name": "USB Camera",
        "source": 0
    },
    {
        "name": "CCTV 1",
        "source": "rtsp://admin:12345@192.168.1.10:554/stream"
    },
    {
        "name": "CCTV 2",
        "source": "rtsp://admin:12345@192.168.1.11:554/stream"
    }
]
# Optional (if you want license / encryption / API key)
CAMERA_ACCESS_KEY = "MY_SECURE_KEY_123"

