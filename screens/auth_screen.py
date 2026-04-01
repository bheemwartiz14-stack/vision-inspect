import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService
from components.placeholder_entry import PlaceholderEntry


class AuthScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.auth = AuthService()

        self.configure(bg="#f5f7fa")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Auth.TFrame", background="#f5f7fa")
        style.configure("AuthCard.TFrame", background="#ffffff")
        style.configure("AuthTitle.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 20, "bold"))
        style.configure("AuthSub.TLabel", background="#ffffff", foreground="#6b7280", font=("Segoe UI", 10))
        style.configure("AuthLink.TButton", font=("Segoe UI", 10), padding=0)
        style.configure("Auth.TEntry", padding=(10, 8))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 8))
        style.map(
            "Primary.TButton",
            foreground=[("!disabled", "#ffffff"), ("pressed", "#ffffff"), ("active", "#ffffff")],
            background=[("!disabled", "#2563eb"), ("pressed", "#1d4ed8"), ("active", "#1d4ed8")],
        )

        outer = ttk.Frame(self, style="Auth.TFrame")
        outer.pack(fill="both", expand=True)

        # simple shadow + centered card
        self._shadow = tk.Frame(outer, bg="#e5e7eb")
        self._shadow.place(relx=0.5, rely=0.5, anchor="center", width=470, height=520)

        self.card = ttk.Frame(outer, style="AuthCard.TFrame", padding=26)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=470, height=520)
        self.card.pack_propagate(False)

        self.container = ttk.Frame(self.card, style="AuthCard.TFrame")
        self.container.pack(fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_login()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()

        ttk.Label(self.container, text="Welcome back", style="AuthTitle.TLabel", anchor="center", justify="center").grid(
            row=0, column=0, sticky="ew", pady=(6, 0)
        )
        ttk.Label(self.container, text="Login to continue", style="AuthSub.TLabel", anchor="center", justify="center").grid(
            row=1, column=0, sticky="ew", pady=(4, 18)
        )

        self.email = PlaceholderEntry(self.container, placeholder="Email", style="Auth.TEntry")
        self.email.grid(row=2, column=0, sticky="ew", pady=7)

        self.password = PlaceholderEntry(self.container, placeholder="Password", style="Auth.TEntry", show="*")
        self.password.grid(row=3, column=0, sticky="ew", pady=7)

        self.company = PlaceholderEntry(self.container, placeholder="Company ID (e.g. COMP001)", style="Auth.TEntry")
        self.company.grid(row=4, column=0, sticky="ew", pady=7)

        ttk.Button(self.container, text="Login", style="Primary.TButton", command=self.login).grid(
            row=5, column=0, sticky="ew", pady=(16, 10)
        )
        ttk.Button(self.container, text="Create account", style="AuthLink.TButton", command=self.show_signup).grid(
            row=6, column=0, sticky="ew"
        )
        ttk.Label(self.container, text=" ", style="AuthSub.TLabel").grid(row=7, column=0, sticky="ew")

    def show_signup(self):
        self.clear()

        ttk.Label(self.container, text="Create account", style="AuthTitle.TLabel", anchor="center", justify="center").grid(
            row=0, column=0, sticky="ew", pady=(6, 0)
        )
        ttk.Label(
            self.container,
            text="Use your company activation details",
            style="AuthSub.TLabel",
            anchor="center",
            justify="center",
        ).grid(row=1, column=0, sticky="ew", pady=(4, 18))

        self.name = PlaceholderEntry(self.container, placeholder="Full name", style="Auth.TEntry")
        self.name.grid(row=2, column=0, sticky="ew", pady=7)

        self.email = PlaceholderEntry(self.container, placeholder="Email", style="Auth.TEntry")
        self.email.grid(row=3, column=0, sticky="ew", pady=7)

        self.password = PlaceholderEntry(self.container, placeholder="Password", style="Auth.TEntry", show="*")
        self.password.grid(row=4, column=0, sticky="ew", pady=7)

        self.code = PlaceholderEntry(self.container, placeholder="Activation code (e.g. ACT001)", style="Auth.TEntry")
        self.code.grid(row=5, column=0, sticky="ew", pady=7)

        self.company = PlaceholderEntry(self.container, placeholder="Company ID (e.g. COMP001)", style="Auth.TEntry")
        self.company.grid(row=6, column=0, sticky="ew", pady=7)

        ttk.Button(self.container, text="Register", style="Primary.TButton", command=self.signup).grid(
            row=7, column=0, sticky="ew", pady=(16, 10)
        )
        ttk.Button(self.container, text="Back to login", style="AuthLink.TButton", command=self.show_login).grid(
            row=8, column=0, sticky="ew"
        )

        ttk.Label(self.container, text=" ", style="AuthSub.TLabel").grid(row=9, column=0, sticky="ew")

    def login(self):
        email = self.email.get_value() if hasattr(self.email, "get_value") else self.email.get()
        password = self.password.get_value() if hasattr(self.password, "get_value") else self.password.get()
        company = self.company.get_value() if hasattr(self.company, "get_value") else self.company.get()

        ok, session = self.auth.login(email, password, company)
        if ok:
            messagebox.showinfo("Success", "Login Success")
            self.controller.session = session or {}
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showerror("Error", "Login Failed")

    def signup(self):
        ok, msg = self.auth.register(
            self.name.get_value() if hasattr(self.name, "get_value") else self.name.get(),
            self.email.get_value() if hasattr(self.email, "get_value") else self.email.get(),
            self.password.get_value() if hasattr(self.password, "get_value") else self.password.get(),
            self.code.get_value() if hasattr(self.code, "get_value") else self.code.get(),
            self.company.get_value() if hasattr(self.company, "get_value") else self.company.get(),
        )
        if ok:
            messagebox.showinfo("Success", msg)
            self.show_login()
        else:
            messagebox.showerror("Error", msg)
