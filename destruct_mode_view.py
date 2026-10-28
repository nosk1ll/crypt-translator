import math
import time
import tkinter as tk
import customtkinter as ctk
from ui_theme import MAIN_BG, MAIN_TEXT


class destruct_mode_view(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=MAIN_BG, width=900, height=560)
        self.app = app
        spacer = ctk.CTkFrame(self, fg_color=MAIN_BG, width=900, height=65, corner_radius=0, border_width=0)
        spacer.pack(side="top", fill="x")
        spacer.pack_propagate(False)

        self._coming = tk.Label(
            self,
            text="Coming Soon",
            font=("Segoe UI", 100),
            fg=MAIN_TEXT,
            bg=MAIN_BG,
            bd=0,
            highlightthickness=0,
        )
        self._x = 40.0
        self._y = 200.0
        self._vx = 48.0
        self._g = 70.0
        self._vy = 0.0
        self._last = None
        self._bounce_after = None
        self._coming.place(x=self._x, y=self._y)

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self._start_coming_soon()

    def place_forget(self):
        self._stop_coming_soon()
        super().place_forget()

    def _start_coming_soon(self):
        if self._bounce_after is None:
            self._last = None
            self._bounce_after = self.after(16, self._bounce_coming_soon)

    def _stop_coming_soon(self):
        if self._bounce_after is not None:
            self.after_cancel(self._bounce_after)
            self._bounce_after = None
        self._last = None

    def _bounce_coming_soon(self):
        if not self.winfo_ismapped():
            self._bounce_after = None
            return
        now = time.perf_counter()
        if self._last is None:
            self._last = now
            self._bounce_after = self.after(16, self._bounce_coming_soon)
            return
        dt = now - self._last
        self._last = now
        if dt <= 0:
            self._bounce_after = self.after(16, self._bounce_coming_soon)
            return
        if dt > 0.05:
            dt = 0.05

        width = self.winfo_width()
        height = self.winfo_height()
        if width < 2 or height < 2:
            self._bounce_after = self.after(16, self._bounce_coming_soon)
            return

        tw = self._coming.winfo_reqwidth()
        th = self._coming.winfo_reqheight()
        if tw < 1:
            tw = 1
        if th < 1:
            th = 1

        max_x = width - tw
        max_y = height - th
        if max_x < 0:
            max_x = 0
        if max_y < 0:
            max_y = 0

        rise = 0.60 * height
        if rise > max_y:
            rise = max_y
        if rise < 1:
            rise = 1
        launch = math.sqrt(2.0 * self._g * rise)

        self._x += self._vx * dt
        self._vy += self._g * dt
        self._y += self._vy * dt

        if self._x <= 0:
            self._x = 0
            self._vx = abs(self._vx)
        if self._x + tw >= width:
            self._x = max_x
            self._vx = -abs(self._vx)

        if self._y + th >= height:
            self._y = max_y
            self._vy = -launch

        self._coming.place(x=self._x, y=self._y)
        self._bounce_after = self.after(16, self._bounce_coming_soon)
