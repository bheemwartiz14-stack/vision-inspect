import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from components.camera_view import CameraView
from components.placeholder_entry import PlaceholderEntry
from components.sidebar import Sidebar
from services.job_service import JobService


class _BasePage(ttk.Frame):
    title = "Page"

    def on_show(self, **kwargs):
        pass

    def on_hide(self):
        pass


class _CameraPage(_BasePage):
    title = "Camera"

    def __init__(self, parent):
        super().__init__(parent)
        card = ttk.Frame(self, padding=14)
        card.pack(fill="both", expand=True)

        header = ttk.Frame(card)
        header.pack(fill="x")
        ttk.Label(header, text="Live Camera", font=("Segoe UI", 14, "bold")).pack(side="left")

        btns = ttk.Frame(header)
        btns.pack(side="right")
        ttk.Button(btns, text="Start", command=self.start).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="Stop", command=self.stop).pack(side="left")

        self.camera = CameraView(card, source=0)
        self.camera.pack(fill="both", expand=True, pady=(12, 0))

    def start(self):
        self.camera.start()

    def stop(self):
        self.camera.stop()

    def on_show(self, **kwargs):
        self.camera.start()

    def on_hide(self):
        self.camera.stop()


class _ManageJobsPage(_BasePage):
    title = "Manage Jobs"

    def __init__(self, parent, dashboard):
        super().__init__(parent)
        self.dashboard = dashboard
        self.job_service = JobService()
        self._image_paths = []

        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)
        root.grid_columnconfigure(0, weight=1, uniform="cols")
        root.grid_columnconfigure(1, weight=2, uniform="cols")
        root.grid_rowconfigure(0, weight=1)

        form = ttk.Frame(root, padding=14)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(form, text="Create job", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(form, text="Add a new inspection job with reference images.", foreground="#6b7280").pack(anchor="w", pady=(2, 12))

        self.title_entry = PlaceholderEntry(form, placeholder="Job title", width=30)
        self.title_entry.pack(fill="x", pady=6)

        ttk.Label(form, text="Job description").pack(anchor="w", pady=(10, 4))
        self.desc_text = tk.Text(form, height=6, wrap="word", bd=1, relief="solid")
        self.desc_text.pack(fill="x")

        ttk.Label(form, text="Job reference images").pack(anchor="w", pady=(10, 4))
        img_row = ttk.Frame(form)
        img_row.pack(fill="x")
        ttk.Button(img_row, text="Choose images", command=self._pick_images).pack(side="left")
        ttk.Button(img_row, text="Clear", command=self._clear_images).pack(side="left", padx=(8, 0))
        self.images_hint = ttk.Label(form, text="No images selected", foreground="#6b7280")
        self.images_hint.pack(anchor="w", pady=(6, 0))

        ttk.Label(form, text="Job status").pack(anchor="w", pady=(10, 4))
        self.status_combo = ttk.Combobox(form, values=["Active", "Paused", "Draft"], state="readonly")
        self.status_combo.set("Active")
        self.status_combo.pack(fill="x")

        ttk.Button(form, text="Create job", command=self._create_job).pack(fill="x", pady=(14, 0))

        list_card = ttk.Frame(root, padding=14)
        list_card.grid(row=0, column=1, sticky="nsew")
        list_card.grid_rowconfigure(2, weight=1)
        list_card.grid_columnconfigure(0, weight=1)

        ttk.Label(list_card, text="All jobs", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")

        quick = ttk.Frame(list_card)
        quick.grid(row=1, column=0, sticky="ew", pady=(10, 10))
        quick.grid_columnconfigure(0, weight=1)
        self.job_id_entry = PlaceholderEntry(quick, placeholder="View job by ID (e.g. 12)")
        self.job_id_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(quick, text="View", command=self._view_by_id).grid(row=0, column=1, padx=(8, 0))
        ttk.Button(quick, text="Refresh", command=self.refresh).grid(row=0, column=2, padx=(8, 0))

        self.tree = ttk.Treeview(list_card, columns=("id", "title", "status"), show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Job title")
        self.tree.heading("status", text="Status")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("title", width=320, anchor="w")
        self.tree.column("status", width=110, anchor="center")
        self.tree.grid(row=2, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", lambda _e: self._view_selected())

        actions = ttk.Frame(list_card)
        actions.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(actions, text="View selected", command=self._view_selected).pack(side="left")

    def _company_id(self):
        session = getattr(self.dashboard.controller, "session", {}) or {}
        return session.get("company_id")

    def _pick_images(self):
        paths = filedialog.askopenfilenames(
            title="Select reference images",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")],
        )
        if not paths:
            return
        self._image_paths = list(paths)
        self._render_images_hint()

    def _clear_images(self):
        self._image_paths = []
        self._render_images_hint()

    def _render_images_hint(self):
        if not self._image_paths:
            self.images_hint.configure(text="No images selected")
            return
        names = [os.path.basename(p) for p in self._image_paths[:3]]
        extra = "" if len(self._image_paths) <= 3 else f" (+{len(self._image_paths) - 3} more)"
        self.images_hint.configure(text=", ".join(names) + extra)

    def _create_job(self):
        company_id = self._company_id()
        if not company_id:
            messagebox.showerror("Error", "Missing company session. Please login again.")
            return

        title = self.title_entry.get_value()
        description = (self.desc_text.get("1.0", "end") or "").strip()
        status = self.status_combo.get().strip()

        if not title:
            messagebox.showerror("Validation", "Job title is required.")
            return

        images_json = json.dumps(self._image_paths)
        self.job_service.create_job(title, description, images_json, status, company_id)
        messagebox.showinfo("Success", "Job created.")

        self.title_entry.delete(0, "end")
        self.desc_text.delete("1.0", "end")
        self._clear_images()
        self.status_combo.set("Active")
        self.refresh()

    def _view_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a job first.")
            return
        job_id = self.tree.item(sel[0], "values")[0]
        self.dashboard.open_job_detail(int(job_id))

    def _view_by_id(self):
        raw = self.job_id_entry.get_value().strip()
        if not raw:
            messagebox.showerror("Error", "Enter a job ID.")
            return
        try:
            job_id = int(raw)
        except ValueError:
            messagebox.showerror("Error", "Job ID must be a number.")
            return
        self.dashboard.open_job_detail(job_id)

    def refresh(self):
        company_id = self._company_id()
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not company_id:
            return

        for job in self.job_service.get_jobs(company_id):
            job_id, title, _desc, _img, status, _company_id = job
            self.tree.insert("", "end", values=(job_id, title, status))

    def on_show(self, **kwargs):
        self.refresh()


class _JobDetailPage(_BasePage):
    title = "Job"

    def __init__(self, parent, dashboard):
        super().__init__(parent)
        self.dashboard = dashboard
        self.job_service = JobService()
        self._job_id = None

        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)
        root.grid_columnconfigure(0, weight=1, uniform="cols")
        root.grid_columnconfigure(1, weight=2, uniform="cols")
        root.grid_rowconfigure(0, weight=1)

        info = ttk.Frame(root, padding=14)
        info.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        top = ttk.Frame(info)
        top.pack(fill="x")
        ttk.Button(top, text="← Back", command=self.dashboard.open_jobs).pack(side="left")
        self.title_lbl = ttk.Label(info, text="Job", font=("Segoe UI", 16, "bold"))
        self.title_lbl.pack(anchor="w", pady=(10, 6))

        self.meta_lbl = ttk.Label(info, text="", foreground="#6b7280")
        self.meta_lbl.pack(anchor="w")

        ttk.Label(info, text="Description", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 4))
        self.desc = tk.Text(info, height=7, wrap="word", bd=1, relief="solid")
        self.desc.configure(state="disabled")
        self.desc.pack(fill="x")

        ttk.Label(info, text="Reference images", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(14, 4))
        self.images = tk.Listbox(info, height=7)
        self.images.pack(fill="both", expand=True)

        cam_card = ttk.Frame(root, padding=14)
        cam_card.grid(row=0, column=1, sticky="nsew")
        cam_card.grid_rowconfigure(1, weight=1)
        cam_card.grid_columnconfigure(0, weight=1)

        cam_header = ttk.Frame(cam_card)
        cam_header.grid(row=0, column=0, sticky="ew")
        ttk.Label(cam_header, text="Camera", font=("Segoe UI", 14, "bold")).pack(side="left")

        cam_btns = ttk.Frame(cam_header)
        cam_btns.pack(side="right")
        ttk.Button(cam_btns, text="Start", command=lambda: self.camera.start()).pack(side="left", padx=(0, 8))
        ttk.Button(cam_btns, text="Stop", command=lambda: self.camera.stop()).pack(side="left")

        self.camera = CameraView(cam_card, source=0)
        self.camera.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

    def on_show(self, job_id=None, **kwargs):
        if job_id is None:
            return
        self._job_id = job_id

        job = self.job_service.get_job_by_id(job_id)
        if not job:
            messagebox.showerror("Not found", f"Job #{job_id} not found.")
            self.dashboard.open_jobs()
            return

        job_id, title, description, image_path, status, company_id = job
        self.dashboard.page_title.configure(text=f"Job #{job_id}")
        self.title_lbl.configure(text=title)
        self.meta_lbl.configure(text=f"ID: {job_id}   Status: {status}   Company: {company_id}")

        self.desc.configure(state="normal")
        self.desc.delete("1.0", "end")
        self.desc.insert("1.0", (description or "").strip())
        self.desc.configure(state="disabled")

        self.images.delete(0, "end")
        for p in self._parse_images(image_path):
            self.images.insert("end", p)

        self.camera.start()

    def on_hide(self):
        self.camera.stop()

    def _parse_images(self, image_path):
        if not image_path:
            return []
        try:
            data = json.loads(image_path)
            if isinstance(data, list):
                return [str(x) for x in data]
        except Exception:
            pass
        return [str(image_path)]


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f7fa")
        self.controller = controller

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#f5f7fa")
        style.configure("TLabel", background="#f5f7fa", foreground="#111827")

        self.sidebar = Sidebar(self, self._on_nav)

        self.main = ttk.Frame(self, padding=0)
        self.main.pack(side="left", fill="both", expand=True)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=0)
        self.main.grid_columnconfigure(2, weight=1)

        self.center = ttk.Frame(self.main, padding=0)
        self.center.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        self.center.grid_rowconfigure(1, weight=1)
        self.center.grid_columnconfigure(0, weight=1)
        self.center.grid_propagate(False)

        self._resize_after_id = None
        self._last_main_size = (0, 0)
        self._last_center_size = None
        self.main.bind("<Configure>", self._on_main_configure)

        header = ttk.Frame(self.center, padding=(16, 14))
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        self.page_title = ttk.Label(header, text="Dashboard", font=("Segoe UI", 18, "bold"))
        self.page_title.grid(row=0, column=0, sticky="w")

        self.content = ttk.Frame(self.center)
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {
            "jobs": _ManageJobsPage(self.content, self),
            "job_detail": _JobDetailPage(self.content, self),
            "camera": _CameraPage(self.content),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        self._active = None
        self.open_jobs()

    def _on_main_configure(self, event):
        # Debounce resize to avoid rapid <Configure> loops (and avoid winfo_* calls).
        self._last_main_size = (event.width, event.height)
        if self._resize_after_id is not None:
            try:
                self.after_cancel(self._resize_after_id)
            except Exception:
                pass
        self._resize_after_id = self.after(60, self._apply_center_size)

    def _apply_center_size(self):
        self._resize_after_id = None
        w, h = self._last_main_size
        if w <= 1 or h <= 1:
            return
        # Keep the main content centered with a max width for a more "modern" layout.
        available_w = max(600, w - 32)
        available_h = max(500, h - 32)
        target_w = min(1040, available_w)
        size = (target_w, available_h)
        if self._last_center_size == size:
            return
        self._last_center_size = size
        self.center.configure(width=target_w, height=available_h)

    def _on_nav(self, key):
        self.sidebar.set_active(key)
        if key == "logout":
            self._logout()
            return
        if key == "camera":
            self.show_page("camera")
            return
        if key == "jobs":
            self.open_jobs()
            return

    def _logout(self):
        self.show_page("jobs")  # ensures camera pages stop cleanly
        self.controller.session = {}
        self.controller.show_frame("AuthScreen")

    def show_page(self, key, **kwargs):
        next_page = self.pages.get(key)
        if not next_page:
            return

        if self._active is not None:
            try:
                self._active.on_hide()
            except Exception:
                pass

        self._active = next_page
        self.page_title.configure(text=getattr(next_page, "title", "Dashboard"))
        next_page.tkraise()
        try:
            next_page.on_show(**kwargs)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_jobs(self):
        self.sidebar.set_active("jobs")
        self.show_page("jobs")

    def open_job_detail(self, job_id):
        self.sidebar.set_active("jobs")
        self.show_page("job_detail", job_id=job_id)
