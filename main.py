import tkinter as tk
from config.settings import APP_TITLE
from config.database import init_db
from screens.lock_screen import LockScreen
from screens.auth_screen import AuthScreen
from screens.dashboard import Dashboard


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.session = {}
        self.title(APP_TITLE or "VisionInspect Pro")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (LockScreen, AuthScreen, Dashboard):
            name = F.__name__
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LockScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
