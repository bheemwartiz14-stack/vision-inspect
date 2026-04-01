import tkinter as tk
from tkinter import ttk
from services.auth_service import AuthService

class LoginScreen(tk.Frame):
    def __init__(self, root, on_login_success):
        super().__init__(root, bg="#f8f9fa")
        self.pack(fill="both", expand=True)

        self.auth = AuthService()
        self.on_login_success = on_login_success

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Login", font=("Segoe UI", 20, "bold")).pack(pady=20)
        self.email = ttk.Entry(self)
        self.email.pack(pady=5)
        self.password = ttk.Entry(self, show="*")
        self.password.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        if self.auth.login(self.email.get(), self.password.get()):
            self.on_login_success()
        else:
            print("Invalid credentials")