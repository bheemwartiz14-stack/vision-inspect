import tkinter as tk
from tkinter import ttk
import sys

from config.database import init_db
from config.settings import APP_NAME, APP_TITLE
# Dummy config
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("500x400")
        self.root.configure(bg="#f8f9fa")

        self.build_ui()

    def build_ui(self):
        # Container
        container = tk.Frame(self.root, bg="#f8f9fa")
        container.pack(expand=True)

        # Title
        title = tk.Label(
            container,
            text=APP_NAME,
            font=("Segoe UI", 20, "bold"),
            bg="#f8f9fa",
            fg="#212529"
        )
        title.pack(pady=20)

        # Card Frame (form box)
        card = tk.Frame(container, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=10)

        form = tk.Frame(card, bg="white")
        form.pack(padx=20, pady=20)

        # Email
        tk.Label(form, text="Email", bg="white", fg="#212529").grid(row=0, column=0, sticky="w")
        self.email_input = ttk.Entry(form, width=30)
        self.email_input.grid(row=1, column=0, pady=5)

        # Password
        tk.Label(form, text="Password", bg="white", fg="#212529").grid(row=2, column=0, sticky="w")
        self.password_input = ttk.Entry(form, width=30, show="*")
        self.password_input.grid(row=3, column=0, pady=5)

        # Button
        login_btn = ttk.Button(form, text="Sign In", command=self.handle_login)
        login_btn.grid(row=4, column=0, pady=15)

    def handle_login(self):
        email = self.email_input.get()
        password = self.password_input.get()

        print("Email:", email)
        print("Password:", password)


# Run app
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    # Modern theme
    style = ttk.Style()
    style.theme_use("clam")
    app = MainApp(root)
    root.mainloop()