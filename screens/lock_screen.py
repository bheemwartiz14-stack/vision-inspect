import tkinter as tk
from tkinter import ttk

class LockScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.configure(bg="#f5f7fa")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Lock.TFrame", background="#f5f7fa")
        style.configure("LockCard.TFrame", background="#ffffff")
        style.configure("LockTitle.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 20, "bold"))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 8))

        outer = ttk.Frame(self, style="Lock.TFrame")
        outer.pack(fill="both", expand=True)

        shadow = tk.Frame(outer, bg="#e5e7eb")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=420, height=220)
        card = ttk.Frame(outer, style="LockCard.TFrame", padding=24)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=220)
        card.pack_propagate(False)

        ttk.Label(card, text="Locked", style="LockTitle.TLabel", anchor="center").pack(fill="x", pady=(10, 8))
        ttk.Label(card, text="Please unlock to continue", background="#ffffff", foreground="#6b7280").pack(fill="x")
        ttk.Button(card, text="Unlock", style="Primary.TButton", command=lambda: controller.show_frame("AuthScreen")).pack(
            fill="x", pady=(18, 0)
        )
