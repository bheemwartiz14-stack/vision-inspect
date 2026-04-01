import tkinter as tk
from tkinter import ttk

class CameraView(ttk.Frame):
    def __init__(self, parent, source=0):
        super().__init__(parent)
        self._source = source
        self._cap = None
        self._running = False
        self._after_id = None
        self._current_frame = None
        self._cv2 = None
        self._Image = None
        self._ImageTk = None

        self.preview = tk.Label(self, bg="black")
        self.preview.pack(fill="both", expand=True)

    def _load_deps(self):
        if self._cv2 is not None and self._Image is not None and self._ImageTk is not None:
            return True
        try:
            import cv2  # type: ignore
            from PIL import Image, ImageTk  # type: ignore
        except Exception:
            return False
        self._cv2 = cv2
        self._Image = Image
        self._ImageTk = ImageTk
        return True

    def start(self):
        if self._running:
            return
        if not self._load_deps():
            self.preview.configure(text="Camera dependencies not available", fg="white", image="")
            return

        self._cap = self._cv2.VideoCapture(self._source)
        if not self._cap.isOpened():
            self.preview.configure(text="Camera not available", fg="white", image="")
            self._cap.release()
            self._cap = None
            return

        self._running = True
        self._tick()

    def stop(self):
        self._running = False
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None

    def capture_to_file(self, path):
        if not self._load_deps():
            return False
        if self._current_frame is None:
            return False
        return bool(self._cv2.imwrite(path, self._current_frame))

    def _tick(self):
        if not self._running or self._cap is None:
            return

        ret, frame = self._cap.read()
        if ret:
            self._current_frame = frame
            frame = self._cv2.cvtColor(frame, self._cv2.COLOR_BGR2RGB)
            img = self._Image.fromarray(frame)
            imgtk = self._ImageTk.PhotoImage(image=img)
            self.preview.imgtk = imgtk
            self.preview.configure(image=imgtk, text="")

        self._after_id = self.after(30, self._tick)
