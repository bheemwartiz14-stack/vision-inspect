from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from config.settings import BASE_KEY
load_dotenv()
# Ensure proper length
KEY = BASE_KEY[:32].ljust(32, b'0')
fernet = Fernet(KEY)
def encrypt(data: str) -> bytes:
    return fernet.encrypt(data.encode())

def decrypt(data: bytes) -> str:
    return fernet.decrypt(data).decode()