import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, parent, on_nav):
        super().__init__(parent, bg="#111827", width=220)
        self.pack_propagate(False)
        self.pack(side="left", fill="y")

        brand = tk.Frame(self, bg="#111827")
        brand.pack(fill="x", padx=16, pady=(16, 10))
        tk.Label(
            brand,
            text="VisionInspect",
            bg="#111827",
            fg="#f9fafb",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")
        tk.Label(
            brand,
            text="Pro",
            bg="#111827",
            fg="#9ca3af",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        menu = [
            ("Camera", "camera"),
            ("Manage Jobs", "jobs"),
            ("Logout", "logout")
        ]

        self._buttons = {}
        for text, key in menu:
            btn = tk.Button(
                self,
                text=text,
                fg="#e5e7eb",
                bg="#111827",
                activeforeground="#ffffff",
                activebackground="#1f2937",
                bd=0,
                relief="flat",
                anchor="w",
                padx=16,
                pady=10,
                font=("Segoe UI", 11),
                command=lambda k=key: on_nav(k),
            )
            btn.pack(fill="x", pady=2, padx=10)
            self._buttons[key] = btn

        self.set_active("jobs")

    def set_active(self, key):
        for k, btn in self._buttons.items():
            if k == key:
                btn.configure(bg="#1f2937", fg="#ffffff")
            else:
                btn.configure(bg="#111827", fg="#e5e7eb")
