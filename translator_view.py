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
        self._syncing=False

        self.private_key = private_key
        self.public_key = public_key
        self._master = master
        self.cipher = getattr(master, "cipher", None) if master is not None else None
        run_loop = master is None
        if master is None:
            self.root = ctk.CTk()
        else:
            self.root = master
            for child in master.winfo_children():
                if child is getattr(master, "_mode_nav", None):
                    continue
                child.place_forget()
            self.root.deiconify()
            self.root.protocol("WM_DELETE_WINDOW", self._on_close)
            master._translator = self
        self.root.geometry("900x560")
        self.root.title("translator")
        self.root.configure(fg_color=MAIN_BG)
        self.root.after(50, self.root.lift)

        box_r = 12
        box_h = 140
        side = 14
        gap = 8

        self.shell = ctk.CTkFrame(self.root, fg_color=MAIN_BG, width=900, height=560, corner_radius=0, border_width=0)
        self.shell.place(x=0, y=0, relwidth=1, relheight=1)

        self._nav = ctk.CTkFrame(self.shell, fg_color=MAIN_BG, width=900, height=65, corner_radius=0, border_width=0)
        self._nav.pack(side="top", fill="x")
        self._nav.pack_propagate(False)

        body = ctk.CTkFrame(self.shell, fg_color="transparent")
        body.pack(fill="both", expand=True)
        work = ctk.CTkFrame(body, fg_color="transparent")
        work.pack(fill="both", expand=True, padx=20, pady=(10, 30))

        row4 = ctk.CTkFrame(work, fg_color="transparent")
        row4.pack(anchor="w", fill="both", expand=True, padx=side, pady=(10, 6))
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
        )
        self.textbox_decrypted.pack(side="left", fill="both", expand=True)
        self._bind_text_events(self.textbox_decrypted, self.textbox_decrypted_change)
        btns4 = ctk.CTkFrame(body4, fg_color="transparent")
        btns4.pack(side="left", padx=(gap, 0), anchor="n")
        self.button_dec_cut = self._clip_button(btns4, "cut", lambda: self._text_cut(self.textbox_decrypted))
        self.button_dec_paste = self._clip_button(btns4, "paste", lambda: self._text_paste(self.textbox_decrypted), pady=3)
        self.button_dec_delete = self._clip_button(btns4, "delete", lambda: self._text_delete(self.textbox_decrypted))

        row5 = ctk.CTkFrame(work, fg_color="transparent")
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
        )
        self.textbox_encrypted.pack(side="left", fill="both", expand=True)
        self._bind_text_events(self.textbox_encrypted, self.textbox_encrypted_change)
        btns5 = ctk.CTkFrame(body5, fg_color="transparent")
        btns5.pack(side="left", padx=(gap, 0), anchor="n")
        self.button_enc_cut = self._clip_button(btns5, "cut", lambda: self._text_cut(self.textbox_encrypted))
        self.button_enc_paste = self._clip_button(btns5, "paste", lambda: self._text_paste(self.textbox_encrypted), pady=3)
        self.button_enc_delete = self._clip_button(btns5, "delete", lambda: self._text_delete(self.textbox_encrypted))

        if run_loop:
            self.root.mainloop()

    def _on_close(self):
        if self._master is not None:
            self._master.destroy()
        else:
            self.root.destroy()

    def _inner(self, widget):
        return widget._textbox

    def _session_cipher(self):
        if self._master is not None:
            shared = getattr(self._master, "cipher", None)
            if shared is not None:
                self.cipher = shared
                return shared
        return self.cipher

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
        )
        btn.pack(pady=pady)
        return btn

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

    def _text_cut(self, widget):
        inner=self._inner(widget)
        text=inner.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        inner.delete("1.0", "end")
        self._sync_after_edit(widget)

    def _text_paste(self, widget):
        inner=self._inner(widget)
        try:
            clip=self.root.clipboard_get()
        except tk.TclError:
            return
        inner.insert("end", clip)
        self._sync_after_edit(widget)

    def _text_delete(self, widget):
        inner=self._inner(widget)
        inner.delete("1.0", "end")
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
        cipher=self._session_cipher()
        if cipher is None or self._syncing:
            return
        self._syncing=True
        try:
            encrypted=cipher.encrypt(decrypted.get("1.0", "end-1c"))
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
        cipher=self._session_cipher()
        if cipher is None or self._syncing:
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
            decrypted.insert("1.0", cipher.decrypt(encrypted))
            decrypted.edit_modified(False)
        finally:
            self.root.after_idle(self._end_sync)
