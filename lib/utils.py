
from PyQt5.QtWidgets import QDesktopWidget, QWidget
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

