import colorsys
import tkinter as tk
import customtkinter as ctk
from PrivateKeyPublicKeyCipher import PrivateKeyPublicKeyCipher
from ui_theme import (
    MAIN_BG,
    MAIN_BUTTON,
    MAIN_BUTTON_HOVER,
    MAIN_BUTTON_TEXT,
    MAIN_ENTRY_BG,
    MAIN_ENTRY_TEXT,
    MAIN_TEXT,
)

TAB_MODES = (
    ("Main Menu", "main"),
    ("Translator Mode", "translator"),
    ("Instant Mode", "instant"),
    ("Destruct Mode", "destruct"),
    ("Confusion Mode", "confusion"),
)
TAB_COLORS = {
    "main": "#9D52BF",
    "translator": "#2E86AB",
    "instant": "#E9C46A",
    "destruct": "#E76F51",
    "confusion": "#2A9D8F",
}


def _darken_tab_color(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    t = 0.38
    dr, dg, db = 0x43, 0x23, 0x52
    return "#%02x%02x%02x" % (
        int(r * t + dr * (1 - t)),
        int(g * t + dg * (1 - t)),
        int(b * t + db * (1 - t)),
    )


def _layout_shared_tabs(app, event=None):
    nav = getattr(app, "_mode_nav", None)
    tabs = getattr(app, "_mode_tabs", None)
    if nav is None or not tabs:
        return
    if event is None or event.widget is app or event.widget is nav:
        nav.place(x=0, y=0, relwidth=1, height=65)
    width = event.width if event is not None and event.widget is nav else nav.winfo_width()
    if width < 10:
        app.update_idletasks()
        width = nav.winfo_width()
    if width < 10:
        width = 900
    n = len(tabs)
    base = width // n
    extra = width - base * n
    x = 0
    for i, tab in enumerate(tabs):
        w = base + (1 if i < extra else 0)
        tab.place(x=x, y=0, width=w, height=65)
        x += w


def _set_active_mode_tab(app, mode):
    for tab in getattr(app, "_mode_tabs", []):
        color = TAB_COLORS[tab._mode]
        fill = color if tab._mode == mode else _darken_tab_color(color)
        tab.configure(bg=fill)
        for child in tab.winfo_children():
            child.configure(bg=fill)


def ensure_mode_nav(app, mode):
    if getattr(app, "_mode_nav", None) is None:
        nav = tk.Frame(app, bg=MAIN_BG, height=65, highlightthickness=0, bd=0)
        nav.pack_propagate(False)
        tabs = []
        for title, key in TAB_MODES:
            color = TAB_COLORS[key]
            tab = tk.Frame(nav, bg=color, height=65, highlightthickness=0, bd=0)
            tab._mode = key
            tab.pack_propagate(False)
            label = tk.Label(
                tab,
                text=title,
                bg=color,
                fg="#FFFFFF",
                font=("Segoe UI", 16, "bold"),
                justify="center",
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
            tab.configure(cursor="hand2")
            label.configure(cursor="hand2")
            tab.bind("<Button-1>", lambda event, m=key: switch_app_mode(app, m))
            label.bind("<Button-1>", lambda event, m=key: switch_app_mode(app, m))
            tabs.append(tab)
        app._mode_nav = nav
        app._mode_tabs = tabs
        nav.bind("<Configure>", lambda event: _layout_shared_tabs(app, event))
        app.bind("<Configure>", lambda event: _layout_shared_tabs(app, event), add="+")
    _layout_shared_tabs(app)
    app._mode_nav.lift()
    _set_active_mode_tab(app, mode)
    app.after_idle(lambda: _layout_shared_tabs(app))


def switch_app_mode(app, mode):
    from instant_mode_view import instant_mode_view
    from destruct_mode_view import destruct_mode_view
    from confusion_mode_view import confusion_mode_view
    from translator_view import translator_view

    if getattr(app, "instant", None) is None:
        app.instant = instant_mode_view(app, app)
    if getattr(app, "destruct", None) is None:
        app.destruct = destruct_mode_view(app, app)
    if getattr(app, "confusion", None) is None:
        app.confusion = confusion_mode_view(app, app)

    for name in ("login", "register", "registered", "main_menu", "instant", "destruct", "confusion"):
        frame = getattr(app, name, None)
        if frame is not None:
            frame.place_forget()

    translator = getattr(app, "_translator", None)
    if translator is not None:
        translator.shell.place_forget()

    app.geometry("900x560")
    app.configure(fg_color=MAIN_BG)

    if mode == "translator":
        if translator is None:
            translator_view(app.private_key, app.public_key, master=app)
        else:
            translator.shell.place(x=0, y=0, relwidth=1, relheight=1)
        ensure_mode_nav(app, mode)
        return

    target = {
        "main": app.main_menu,
        "instant": app.instant,
        "destruct": app.destruct,
        "confusion": app.confusion,
    }[mode]
    target.place(x=0, y=0, relwidth=1, relheight=1)
    ensure_mode_nav(app, mode)


class main_menu_view(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=MAIN_BG, width=900, height=560)
        self.app = app
        self.cipher = None
        self.private_key = None
        self.public_key = None

        btn_w = 81
        btn_h = 36
        btn_r = 8
        box_r = 12
        side = 28

        self._nav = ctk.CTkFrame(self, fg_color=MAIN_BG, width=900, height=65, corner_radius=0, border_width=0)
        self._nav.pack(side="top", fill="x")
        self._nav.pack_propagate(False)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True)
        content = ctk.CTkFrame(body, fg_color="transparent", width=744, height=250)
        content.pack_propagate(False)
        content.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            content,
            text="your username:",
            text_color=MAIN_TEXT,
            fg_color="transparent",
            font=ctk.CTkFont(size=14),
            anchor="w",
        ).pack(fill="x")
        user_row = ctk.CTkFrame(content, fg_color="transparent", height=btn_h)
        user_row.pack(fill="x", pady=(6, 22))
        user_row.pack_propagate(False)
        self.label_username = ctk.CTkEntry(
            user_row,
            height=btn_h,
            fg_color=MAIN_ENTRY_BG,
            text_color=MAIN_ENTRY_TEXT,
            border_width=0,
            corner_radius=box_r,
        )
        self.label_username.pack(side="left", fill="x", expand=True)
        self.button_copy = ctk.CTkButton(
            user_row,
            text="copy",
            width=btn_w,
            height=btn_h,
            corner_radius=btn_r,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            command=self.button_copy_click,
        )
        self.button_copy.pack(side="left", padx=(10, 0))

        ctk.CTkLabel(
            content,
            text="recepient's username:",
            text_color=MAIN_TEXT,
            fg_color="transparent",
            font=ctk.CTkFont(size=14),
            anchor="w",
        ).pack(fill="x")
        recip_row = ctk.CTkFrame(content, fg_color="transparent", height=btn_h)
        recip_row.pack(fill="x", pady=(6, 22))
        recip_row.pack_propagate(False)
        self.textbox_recepient = ctk.CTkEntry(
            recip_row,
            height=btn_h,
            fg_color=MAIN_ENTRY_BG,
            text_color=MAIN_ENTRY_TEXT,
            border_width=0,
            corner_radius=box_r,
        )
        self.textbox_recepient.pack(side="left", fill="x", expand=True)
        self.button_paste = ctk.CTkButton(
            recip_row,
            text="paste",
            width=btn_w,
            height=btn_h,
            corner_radius=btn_r,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            command=self.button_paste_click,
        )
        self.button_paste.pack(side="left", padx=(10, 0))

        self.button_confirm = ctk.CTkButton(
            content,
            text="confirm recepient",
            height=42,
            corner_radius=btn_r,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.button_confirm_click,
        )
        self.button_confirm.pack(fill="x", pady=(10, 0))

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        ensure_mode_nav(self.app, "main")
        self.after_idle(lambda: ensure_mode_nav(self.app, "main"))

    def set_keys(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key
        self.cipher = None
        self.app.private_key = private_key
        self.app.public_key = public_key
        self.app.recipient_public_key = None
        self.app.cipher = None
        self.label_username.delete(0, "end")
        self.label_username.insert(0, public_key)
        self.textbox_recepient.delete(0, "end")
        self.button_confirm.configure(fg_color=MAIN_BUTTON, hover_color=MAIN_BUTTON_HOVER)

    def button_copy_click(self):
        top = self.winfo_toplevel()
        top.clipboard_clear()
        top.clipboard_append(self.public_key)

    def button_paste_click(self):
        self.textbox_recepient.delete(0, "end")
        self.textbox_recepient.insert(0, self.winfo_toplevel().clipboard_get())

    def button_confirm_click(self):
        recepient_public_key = self.textbox_recepient.get()
        self.cipher = PrivateKeyPublicKeyCipher(self.private_key, recepient_public_key)
        self.app.recipient_public_key = recepient_public_key
        self.app.cipher = self.cipher
        self._rainbow_confirm()

    def _rainbow_confirm(self):
        after_id = getattr(self, "_rainbow_after", None)
        if after_id is not None:
            self.after_cancel(after_id)
            self._rainbow_after = None
        self._rainbow_gen = getattr(self, "_rainbow_gen", 0) + 1
        gen = self._rainbow_gen
        steps = 20
        delay_ms = 50

        def frame(i):
            if gen != self._rainbow_gen:
                return
            if i >= steps:
                self.button_confirm.configure(fg_color=MAIN_BUTTON, hover_color=MAIN_BUTTON_HOVER)
                self._rainbow_after = None
                return
            r, g, b = colorsys.hsv_to_rgb(i / steps, 0.55, 1.0)
            color = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
            self.button_confirm.configure(fg_color=color, hover_color=color)
            self._rainbow_after = self.after(delay_ms, lambda: frame(i + 1))

        frame(0)
