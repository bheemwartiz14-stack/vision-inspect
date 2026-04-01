
import hashlib
import uuid
from PyQt5.QtWidgets import QDesktopWidget, QWidget

from config.settings import BASE_KEY

def center_window(window: QWidget) -> None:
    """
    Centers the given window on the screen.
    Args:
        window (QWidget): The window to be centered.
    """
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def generate_secure_key():
    machine_id = str(uuid.getnode())  # unique per machine
    combined = BASE_KEY + machine_id
    return hashlib.sha256(combined.encode()).hexdigest()