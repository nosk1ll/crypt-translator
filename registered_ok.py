import tkinter as tk
import customtkinter as ctk
from ui_theme import (
    AUTH_BG,
    AUTH_BUTTON,
    AUTH_BUTTON_HOVER,
    AUTH_BUTTON_TEXT,
    AUTH_TEXT,
    MAIN_BG,
    MAIN_BUTTON,
)

FORM_W = 280
FIELD_H = 38
BTN_H = 40


class registered_ok(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=AUTH_BG, width=900, height=560)
        self.app = app

        self._left = tk.Canvas(self, highlightthickness=0, bd=0)
        self._left.place(relx=0, rely=0, relwidth=0.58, relheight=1)
        self._left.bind("<Configure>", self._paint_left)

        right = ctk.CTkFrame(self, fg_color=AUTH_BG, corner_radius=0)
        right.place(relx=0.58, rely=0, relwidth=0.42, relheight=1)

        form = ctk.CTkFrame(right, fg_color="transparent")
        form.place(relx=0.5, rely=0.48, anchor="center")

        self._build_logo(form)

        ctk.CTkLabel(
            form,
            text="Account created",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=AUTH_TEXT,
            fg_color="transparent",
        ).pack(pady=(18, 4))
        self.label_info = ctk.CTkLabel(
            form,
            text="Your account has been created with username:",
            font=ctk.CTkFont(size=13),
            text_color="#7A7A7A",
            fg_color="transparent",
            wraplength=FORM_W,
            justify="center",
        )
        self.label_info.pack(pady=(0, 22))

        controls = ctk.CTkFrame(form, fg_color="transparent", width=FORM_W)
        controls.pack()

        self.textbox_username = ctk.CTkEntry(
            controls,
            width=FORM_W,
            height=FIELD_H,
            fg_color="#FFFFFF",
            text_color=AUTH_TEXT,
            border_color="#D0D0D0",
        )
        self.textbox_username.pack(pady=(4, 14))

        self.button_copy = ctk.CTkButton(
            controls,
            text="Copy",
            width=FORM_W,
            height=BTN_H,
            fg_color=AUTH_BUTTON,
            hover_color=AUTH_BUTTON_HOVER,
            text_color=AUTH_BUTTON_TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: (
                self.winfo_toplevel().clipboard_clear(),
                self.winfo_toplevel().clipboard_append(self.textbox_username.get()),
            ),
        )
        self.button_copy.pack(pady=(14, 8))
        self.button_ok = ctk.CTkButton(
            controls,
            text="Ok",
            width=FORM_W,
            height=BTN_H,
            fg_color="#FFFFFF",
            hover_color="#F2F2F2",
            text_color="#000000",
            border_width=2,
            border_color="#9A9A9A",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.button_ok_click,
        )
        self.button_ok.pack()

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self._same_window_as_register()
        self.after_idle(self._same_window_as_register)

    def _same_window_as_register(self):
        top = self.winfo_toplevel()
        top.geometry("900x560")
        top.update_idletasks()
        self.configure(width=900, height=560)

    def _build_logo(self, parent):
        logo = tk.Canvas(parent, width=52, height=52, bg=AUTH_BG, highlightthickness=0)
        logo.pack()
        color = AUTH_BUTTON
        r = 10
        centers = ((18, 16), (34, 16), (18, 32), (34, 32))
        for x, y in centers:
            logo.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)

    def _paint_left(self, event):
        canvas = event.widget
        canvas.delete("grad")
        width = max(event.width, 1)
        height = max(event.height, 1)
        bright = self._hex_rgb(MAIN_BUTTON)
        dark = self._hex_rgb(MAIN_BG)
        for x in range(width):
            t = x / max(width - 1, 1)
            bright_amt = (1 - t) ** 2.2
            color = "#%02x%02x%02x" % tuple(int(d + (b - d) * bright_amt) for d, b in zip(dark, bright))
            canvas.create_line(x, 0, x, height, fill=color, tags="grad")

    def _hex_rgb(self, value):
        value = value.lstrip("#")
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))

    def set_username(self, username):
        self.textbox_username.delete(0, "end")
        self.textbox_username.insert(0, username)

    def button_ok_click(self):
        self.app.show_login()
