import tkinter as tk
import customtkinter as ctk
from AccountManager import AccountManager
from ui_theme import (
    AUTH_BG,
    AUTH_BUTTON,
    AUTH_BUTTON_HOVER,
    AUTH_BUTTON_TEXT,
    AUTH_TEXT,
    AUTH_WARN,
    MAIN_BG,
    MAIN_BUTTON,
)

FORM_W = 280
FIELD_H = 38
BTN_H = 40
PASTE_W = 58
PASTE_GAP = 8


class login_view(ctk.CTkFrame):
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
            text="Log In",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=AUTH_TEXT,
            fg_color="transparent",
        ).pack(pady=(18, 4))
        ctk.CTkLabel(
            form,
            text="Please enter your login details below",
            font=ctk.CTkFont(size=13),
            text_color="#7A7A7A",
            fg_color="transparent",
            wraplength=FORM_W,
            justify="center",
        ).pack(pady=(0, 22))

        controls = ctk.CTkFrame(form, fg_color="transparent", width=FORM_W)
        controls.pack()

        ctk.CTkLabel(
            controls,
            text="Username",
            font=ctk.CTkFont(size=13),
            text_color=AUTH_TEXT,
            fg_color="transparent",
            width=FORM_W,
            anchor="w",
        ).pack()

        user_row = ctk.CTkFrame(controls, fg_color="transparent", width=FORM_W, height=FIELD_H)
        user_row.pack(pady=(4, 14))
        user_row.pack_propagate(False)
        self.textbox_username = ctk.CTkEntry(
            user_row,
            width=FORM_W - PASTE_W - PASTE_GAP,
            height=FIELD_H,
            fg_color="#FFFFFF",
            text_color=AUTH_TEXT,
            border_color="#D0D0D0",
            placeholder_text="Username",
        )
        self.textbox_username.place(x=0, y=0)
        self.button_username_paste = ctk.CTkButton(
            user_row,
            text="paste",
            width=PASTE_W,
            height=FIELD_H,
            fg_color=AUTH_BUTTON,
            hover_color=AUTH_BUTTON_HOVER,
            text_color=AUTH_BUTTON_TEXT,
            command=self._paste_username,
        )
        self.button_username_paste.place(x=FORM_W - PASTE_W, y=0)

        ctk.CTkLabel(
            controls,
            text="Password",
            font=ctk.CTkFont(size=13),
            text_color=AUTH_TEXT,
            fg_color="transparent",
            width=FORM_W,
            anchor="w",
        ).pack()
        self.textbox_password = ctk.CTkEntry(
            controls,
            width=FORM_W,
            height=FIELD_H,
            show="*",
            fg_color="#FFFFFF",
            text_color=AUTH_TEXT,
            border_color="#D0D0D0",
            placeholder_text="Password",
        )
        self.textbox_password.pack(pady=(4, 8))
        self.textbox_password.bind("<Return>", lambda event: self.button_login_click())

        self.label_wrong = ctk.CTkLabel(
            controls,
            text="",
            text_color=AUTH_WARN,
            fg_color="transparent",
            font=ctk.CTkFont(size=12),
            width=FORM_W,
        )
        self.label_wrong.pack(pady=(0, 8))

        self.button_login = ctk.CTkButton(
            controls,
            text="Log in",
            width=FORM_W,
            height=BTN_H,
            fg_color=AUTH_BUTTON,
            hover_color=AUTH_BUTTON_HOVER,
            text_color=AUTH_BUTTON_TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.button_login_click,
        )
        self.button_login.pack(pady=(4, 8))
        self.button_register = ctk.CTkButton(
            controls,
            text="Register",
            width=FORM_W,
            height=BTN_H,
            fg_color="#FFFFFF",
            hover_color="#F2F2F2",
            text_color="#000000",
            border_width=2,
            border_color="#9A9A9A",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.button_register_click,
        )
        self.button_register.pack()

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

    def _paste_username(self):
        self.textbox_username.delete(0, "end")
        self.textbox_username.insert(0, self.winfo_toplevel().clipboard_get())

    def reset(self):
        self.label_wrong.configure(text="")

    def button_login_click(self):
        am = AccountManager()
        password=self.textbox_password.get()
        username=self.textbox_username.get()
        if am.get_public_key(password)==username:
            private_key=am.get_private_key(password)
            public_key=username
            self.app.open_translator(private_key, public_key)
        else:
            self.label_wrong.configure(text="Incorrect username and password.")

    def button_register_click(self):
        self.app.show_register()
