import os
from dotenv import load_dotenv # type: ignore
import uuid
import hashlib
load_dotenv()
APP_TITLE = os.getenv("APP_TITLE")
APP_NAME = APP_TITLE
DB_PATH = os.path.expanduser(os.getenv("DB_PATH"))
BASE_KEY = os.getenv("APP_DB_KEY")

