
import hashlib
import uuid
from config.settings import BASE_KEY

def generate_secure_key():
    machine_id = str(uuid.getnode())  # unique per machine
    combined = BASE_KEY + machine_id
    return hashlib.sha256(combined.encode()).hexdigest()

