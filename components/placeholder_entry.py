import tkinter as tk
from tkinter import ttk

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", color="grey", **kwargs):
        self._real_show = kwargs.get("show", "")
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["foreground"]

        if self._real_show:
            self.configure(show="")

        self.insert(0, self.placeholder)
        self["foreground"] = self.placeholder_color
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
    def _clear_placeholder(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self["foreground"] = self.default_fg_color
            if self._real_show:
                self.configure(show=self._real_show)

    def _add_placeholder(self, e):
        if not self.get():
            if self._real_show:
                self.configure(show="")
            self.insert(0, self.placeholder)
            self["foreground"] = self.placeholder_color

    def get_value(self):
        value = self.get()
        if value == self.placeholder:
            return ""
        return value
