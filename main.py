import sys
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from config.database import init_db
from config.settings import APP_NAME, APP_TITLE
from lib.utils import center_window
bootstrap_style = """
QWidget { font-family: Arial, sans-serif; font-size: 14px; }
QMainWindow { background-color: #f8f9fa; }
QLabel { color: #212529; }
QLineEdit { border: 1px solid #ced4da; border-radius: 4px; padding: 5px; font-size: 14px; color: #495057; }
QLineEdit:focus { border-color: #80bdff; outline: 0; background-color: rgba(0, 123, 255, 0.1); }
QPushButton { background-color: #007bff; border: 1px solid #007bff; border-radius: 4px; color: white; padding: 5px 10px; font-size: 14px; }
QPushButton:hover { background-color: #0056b3; border-color: #0056b3; }
QPushButton:disabled { background-color: #6c757d; border-color: #6c757d; color: white; }
QTextEdit { border: 1px solid #ced4da; border-radius: 4px; padding: 5px; font-size: 14px; color: #495057; background-color: white; }
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    # Initlize  The main Screen  
    def initUI(self):
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(500, 600, 800, 500)
        center_window(self)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        # App Title
        app_title_label = QLabel(f"<h1>{APP_NAME}</h1>")
        app_title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_title_label)
        # Form Layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addSpacing(20)
        # Email Label + Input
        email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        # Password Label + Input
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Sign In Button
        login_button = QPushButton("Sign In")
        login_button.clicked.connect(self.handle_login)

        # Add to form layout
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_button)
        # Center form
        layout.addLayout(form_layout)
    
    def handle_login(self):
        print('zxc')
        


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(bootstrap_style)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    print('zxcxzcxzcxzc')