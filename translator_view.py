import tkinter as tk
import os
from StringCipher import StringCipher
from DummyCipher import DummyCipher
from PowmodHash import PowmodHash
from PrivateKeyPublicKeyCipher import PrivateKeyPublicKeyCipher
from AccountManager import AccountManager


class translator_view:
    def __init__(self, private_key, public_key):
        self.cipher=None
        self._syncing=False

        self.private_key = private_key
        self.public_key = public_key
        self.root = tk.Tk()
        self.root.geometry("900x480")
        self.root.title("translator")

        row1 = tk.Frame(self.root)
        row1.pack(anchor="w", padx=10, pady=8)
        tk.Label(row1, text="your username: ").pack(side="left")
        self.label_username = tk.Label(row1, text=public_key)
        self.label_username.pack(side="left")
        self.button_copy = tk.Button(row1, text="copy", command=self.button_copy_click)
        self.button_copy.pack(side="left", padx=8)

        row2 = tk.Frame(self.root)
        row2.pack(anchor="w", fill="x", padx=10, pady=8)
        tk.Label(row2, text="recepient's username:").pack(side="left")
        self.textbox_recepient = tk.Entry(row2)
        self.textbox_recepient.pack(side="left", fill="x", expand=True, padx=8)
        self.button_paste = tk.Button(row2, text="paste", command=self.button_paste_click)
        self.button_paste.pack(side="left")

        self.button_confirm = tk.Button(self.root, text="confirm recepient", command=self.button_confirm_click)
        self.button_confirm.pack(anchor="w", padx=10, pady=8)

        row4 = tk.Frame(self.root)
        row4.pack(anchor="w", padx=10, pady=8)
        tk.Label(row4, text="decrypted text:").pack(anchor="w")
        body4 = tk.Frame(row4)
        body4.pack(anchor="w")
        self.textbox_decrypted = tk.Text(body4, height=8, width=70)
        self.textbox_decrypted.pack(side="left")
        self._bind_text_events(self.textbox_decrypted, self.textbox_decrypted_change)
        btns4 = tk.Frame(body4)
        btns4.pack(side="left", padx=8, anchor="n")
        tk.Button(btns4, text="Cut", width=8, command=lambda: self._text_cut(self.textbox_decrypted)).pack()
        tk.Button(btns4, text="Copy", width=8, command=lambda: self._text_copy(self.textbox_decrypted)).pack()
        tk.Button(btns4, text="Paste", width=8, command=lambda: self._text_paste(self.textbox_decrypted)).pack()

        row5 = tk.Frame(self.root)
        row5.pack(anchor="w", padx=10, pady=8)
        tk.Label(row5, text="encrypted text:").pack(anchor="w")
        body5 = tk.Frame(row5)
        body5.pack(anchor="w")
        self.textbox_encrypted = tk.Text(body5, height=8, width=70)
        self.textbox_encrypted.pack(side="left")
        self._bind_text_events(self.textbox_encrypted, self.textbox_encrypted_change)
        btns5 = tk.Frame(body5)
        btns5.pack(side="left", padx=8, anchor="n")
        tk.Button(btns5, text="Cut", width=8, command=lambda: self._text_cut(self.textbox_encrypted)).pack()
        tk.Button(btns5, text="Copy", width=8, command=lambda: self._text_copy(self.textbox_encrypted)).pack()
        tk.Button(btns5, text="Paste", width=8, command=lambda: self._text_paste(self.textbox_encrypted)).pack()

        self.root.mainloop()

    def button_copy_click(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.public_key)

    def button_paste_click(self):
        self.textbox_recepient.delete(0, tk.END)
        self.textbox_recepient.insert(0, self.root.clipboard_get())

    def button_confirm_click(self):
        recepient_public_key=self.textbox_recepient.get()
        self.cipher = PrivateKeyPublicKeyCipher(self.private_key,recepient_public_key)

    def _bind_text_events(self, widget, handler):
        widget.bind("<<Modified>>", handler)
        widget.bind("<KeyRelease>", handler)
        widget.bind("<<Paste>>", handler)

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
        try:
            text=widget.get("sel.first", "sel.last")
        except tk.TclError:
            text=widget.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def _text_cut(self, widget):
        try:
            text=widget.get("sel.first", "sel.last")
            widget.delete("sel.first", "sel.last")
        except tk.TclError:
            text=widget.get("1.0", "end-1c")
            widget.delete("1.0", "end")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._sync_after_edit(widget)

    def _text_paste(self, widget):
        try:
            clip=self.root.clipboard_get()
        except tk.TclError:
            return
        try:
            widget.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        widget.insert("insert", clip)
        self._sync_after_edit(widget)

    def _sync_after_edit(self, widget):
        widget.edit_modified(True)
        if widget is self.textbox_decrypted:
            self.textbox_decrypted_change()
        else:
            self.textbox_encrypted_change()

    def textbox_decrypted_change(self, event=None):
        if self.textbox_decrypted.edit_modified():
            self.textbox_decrypted.edit_modified(False)
        if self.cipher is None or self._syncing:
            return
        self._syncing=True
        try:
            encrypted=self.cipher.encrypt(self.textbox_decrypted.get("1.0", "end-1c"))
            self.textbox_encrypted.delete("1.0", "end")
            self.textbox_encrypted.insert("1.0", encrypted)
            self.textbox_encrypted.edit_modified(False)
        finally:
            self.root.after_idle(self._end_sync)

    def textbox_encrypted_change(self, event=None):
        if self._is_non_edit_event(event):
            return
        if self.textbox_encrypted.edit_modified():
            self.textbox_encrypted.edit_modified(False)
        if self.cipher is None or self._syncing:
            return
        self._syncing=True
        try:
            raw=self.textbox_encrypted.get("1.0", "end-1c")
            encrypted=raw.strip()
            if encrypted!=raw:
                self.textbox_encrypted.delete("1.0", "end")
                self.textbox_encrypted.insert("1.0", encrypted)
                self.textbox_encrypted.edit_modified(False)
            self.textbox_decrypted.delete("1.0", "end")
            self.textbox_decrypted.insert("1.0", self.cipher.decrypt(encrypted))
            self.textbox_decrypted.edit_modified(False)
        finally:
            self.root.after_idle(self._end_sync)
