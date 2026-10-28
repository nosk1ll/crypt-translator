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


class translator_view:
    def __init__(self, private_key, public_key, master=None):
        self.cipher=None
        self._syncing=False

        self.private_key = private_key
        self.public_key = public_key
        self._master = master
        run_loop = master is None
        if master is None:
            self.root = ctk.CTk()
        else:
            self.root = master
            for child in master.winfo_children():
                child.place_forget()
            self.root.deiconify()
            self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.geometry("900x560")
        self.root.title("translator")
        self.root.configure(fg_color=MAIN_BG)
        self.root.after(50, self.root.lift)

        btn_w = 81
        btn_h = 28
        btn_r = 8
        box_r = 12
        box_h = 140
        side = 14
        gap = 8

        row1 = ctk.CTkFrame(self.root, fg_color="transparent")
        row1.pack(anchor="w", fill="x", padx=side, pady=(10, 6))
        ctk.CTkLabel(row1, text="your username: ", text_color=MAIN_TEXT, fg_color="transparent").pack(side="left")
        self.label_username = ctk.CTkLabel(row1, text=public_key, text_color=MAIN_TEXT, fg_color="transparent")
        self.label_username.pack(side="left")
        self.button_copy = ctk.CTkButton(
            row1,
            text="copy",
            width=btn_w,
            height=btn_h,
            corner_radius=btn_r,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            command=self.button_copy_click,
        )
        self.button_copy.pack(side="left", padx=6)

        row2 = ctk.CTkFrame(self.root, fg_color="transparent")
        row2.pack(anchor="w", fill="x", padx=side, pady=6)
        ctk.CTkLabel(row2, text="recepient's username:", text_color=MAIN_TEXT, fg_color="transparent").pack(side="left")
        self.textbox_recepient = ctk.CTkEntry(
            row2,
            height=btn_h,
            fg_color=MAIN_ENTRY_BG,
            text_color=MAIN_ENTRY_TEXT,
            border_width=0,
            corner_radius=box_r,
        )
        self.textbox_recepient.pack(side="left", fill="x", expand=True, padx=6)
        self.button_paste = ctk.CTkButton(
            row2,
            text="paste",
            width=btn_w,
            height=btn_h,
            corner_radius=btn_r,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            command=self.button_paste_click,
        )
        self.button_paste.pack(side="left")

        self.button_confirm = ctk.CTkButton(
            self.root,
            text="confirm recepient",
            width=176,
            height=btn_h,
            corner_radius=btn_r,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            command=self.button_confirm_click,
        )
        self.button_confirm.pack(anchor="w", padx=side, pady=6)

        row4 = ctk.CTkFrame(self.root, fg_color="transparent")
        row4.pack(anchor="w", fill="both", expand=True, padx=side, pady=(8, 6))
        ctk.CTkLabel(row4, text="decrypted text:", text_color=MAIN_TEXT, fg_color="transparent").pack(anchor="w")
        body4 = ctk.CTkFrame(row4, fg_color="transparent")
        body4.pack(anchor="w", fill="both", expand=True)
        self.textbox_decrypted = ctk.CTkTextbox(
            body4,
            height=box_h,
            fg_color=MAIN_ENTRY_BG,
            text_color=MAIN_ENTRY_TEXT,
            border_width=0,
            corner_radius=box_r,
            state="disabled",
        )
        self.textbox_decrypted.pack(side="left", fill="both", expand=True)
        self._bind_text_events(self.textbox_decrypted, self.textbox_decrypted_change)
        btns4 = ctk.CTkFrame(body4, fg_color="transparent")
        btns4.pack(side="left", padx=(gap, 0), anchor="n")
        self.button_dec_cut = self._clip_button(btns4, "Cut", lambda: self._text_cut(self.textbox_decrypted))
        self.button_dec_copy = self._clip_button(btns4, "Copy", lambda: self._text_copy(self.textbox_decrypted), pady=3)
        self.button_dec_paste = self._clip_button(btns4, "Paste", lambda: self._text_paste(self.textbox_decrypted))

        row5 = ctk.CTkFrame(self.root, fg_color="transparent")
        row5.pack(anchor="w", fill="both", expand=True, padx=side, pady=(6, 12))
        ctk.CTkLabel(row5, text="encrypted text:", text_color=MAIN_TEXT, fg_color="transparent").pack(anchor="w")
        body5 = ctk.CTkFrame(row5, fg_color="transparent")
        body5.pack(anchor="w", fill="both", expand=True)
        self.textbox_encrypted = ctk.CTkTextbox(
            body5,
            height=box_h,
            fg_color=MAIN_ENTRY_BG,
            text_color=MAIN_ENTRY_TEXT,
            border_width=0,
            corner_radius=box_r,
            state="disabled",
        )
        self.textbox_encrypted.pack(side="left", fill="both", expand=True)
        self._bind_text_events(self.textbox_encrypted, self.textbox_encrypted_change)
        btns5 = ctk.CTkFrame(body5, fg_color="transparent")
        btns5.pack(side="left", padx=(gap, 0), anchor="n")
        self.button_enc_cut = self._clip_button(btns5, "Cut", lambda: self._text_cut(self.textbox_encrypted))
        self.button_enc_copy = self._clip_button(btns5, "Copy", lambda: self._text_copy(self.textbox_encrypted), pady=3)
        self.button_enc_paste = self._clip_button(btns5, "Paste", lambda: self._text_paste(self.textbox_encrypted))

        if run_loop:
            self.root.mainloop()

    def _on_close(self):
        if self._master is not None:
            self._master.destroy()
        else:
            self.root.destroy()

    def _inner(self, widget):
        return widget._textbox

    def button_copy_click(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.public_key)

    def button_paste_click(self):
        self.textbox_recepient.delete(0, "end")
        self.textbox_recepient.insert(0, self.root.clipboard_get())

    def _clip_button(self, parent, text, command, pady=0):
        btn = ctk.CTkButton(
            parent,
            text=text,
            width=81,
            height=28,
            corner_radius=8,
            fg_color=MAIN_BUTTON,
            hover_color=MAIN_BUTTON_HOVER,
            text_color=MAIN_BUTTON_TEXT,
            command=command,
            state="disabled",
        )
        btn.pack(pady=pady)
        return btn

    def _set_message_controls_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.textbox_decrypted.configure(state=state)
        self.textbox_encrypted.configure(state=state)
        for btn in (
            self.button_dec_cut,
            self.button_dec_copy,
            self.button_dec_paste,
            self.button_enc_cut,
            self.button_enc_copy,
            self.button_enc_paste,
        ):
            btn.configure(state=state)

    def button_confirm_click(self):
        recepient_public_key=self.textbox_recepient.get()
        self.cipher = PrivateKeyPublicKeyCipher(self.private_key,recepient_public_key)
        self._set_message_controls_enabled(True)
        self._rainbow_confirm()

    def _rainbow_confirm(self):
        after_id = getattr(self, "_rainbow_after", None)
        if after_id is not None:
            self.root.after_cancel(after_id)
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
            self._rainbow_after = self.root.after(delay_ms, lambda: frame(i + 1))

        frame(0)

    def _bind_text_events(self, widget, handler):
        inner=self._inner(widget)
        inner.bind("<<Modified>>", handler)
        inner.bind("<KeyRelease>", handler)
        inner.bind("<<Paste>>", handler)

    def _end_sync(self):
        self._syncing=False

    def _is_non_edit_event(self, event):
        if event is None:
            return False
        keysym=getattr(event, "keysym", "")
        state=getattr(event, "state", 0)
        if keysym in (
            "Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R",
            "Left", "Right", "Up", "Down", "Home", "End", "Next", "Prior",
            "Caps_Lock", "Num_Lock",
        ):
            return True
        if (state & 0x4) and keysym.lower() in ("a", "c"):
            return True
        return False

    def _text_copy(self, widget):
        inner=self._inner(widget)
        try:
            text=inner.get("sel.first", "sel.last")
        except tk.TclError:
            text=inner.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def _text_cut(self, widget):
        inner=self._inner(widget)
        try:
            text=inner.get("sel.first", "sel.last")
            inner.delete("sel.first", "sel.last")
        except tk.TclError:
            text=inner.get("1.0", "end-1c")
            inner.delete("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._sync_after_edit(widget)

    def _text_paste(self, widget):
        inner=self._inner(widget)
        try:
            clip=self.root.clipboard_get()
        except tk.TclError:
            return
        try:
            inner.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        inner.insert("insert", clip)
        self._sync_after_edit(widget)

    def _sync_after_edit(self, widget):
        self._inner(widget).edit_modified(True)
        if widget is self.textbox_decrypted:
            self.textbox_decrypted_change()
        else:
            self.textbox_encrypted_change()

    def textbox_decrypted_change(self, event=None):
        decrypted=self._inner(self.textbox_decrypted)
        encrypted_box=self._inner(self.textbox_encrypted)
        if decrypted.edit_modified():
            decrypted.edit_modified(False)
        if self.cipher is None or self._syncing:
            return
        self._syncing=True
        try:
            encrypted=self.cipher.encrypt(decrypted.get("1.0", "end-1c"))
            encrypted_box.delete("1.0", "end")
            encrypted_box.insert("1.0", encrypted)
            encrypted_box.edit_modified(False)
        finally:
            self.root.after_idle(self._end_sync)

    def textbox_encrypted_change(self, event=None):
        if self._is_non_edit_event(event):
            return
        decrypted=self._inner(self.textbox_decrypted)
        encrypted_box=self._inner(self.textbox_encrypted)
        if encrypted_box.edit_modified():
            encrypted_box.edit_modified(False)
        if self.cipher is None or self._syncing:
            return
        self._syncing=True
        try:
            raw=encrypted_box.get("1.0", "end-1c")
            encrypted=raw.strip()
            if encrypted!=raw:
                encrypted_box.delete("1.0", "end")
                encrypted_box.insert("1.0", encrypted)
                encrypted_box.edit_modified(False)
            decrypted.delete("1.0", "end")
            decrypted.insert("1.0", self.cipher.decrypt(encrypted))
            decrypted.edit_modified(False)
        finally:
            self.root.after_idle(self._end_sync)
