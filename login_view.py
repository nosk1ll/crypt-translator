import tkinter as tk
from AccountManager import AccountManager
from PrivateKeyPublicKeyCipher import PrivateKeyPublicKeyCipher
from register_view import register_view
from translator_view import translator_view

class login_view:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("370x200")
        indent = 10

        self.label_username = tk.Label(self.root, text="username:", width=10, anchor="w")
        self.label_password = tk.Label(self.root, text="password:", width=10, anchor="w")
        self.textbox_username = tk.Entry(self.root, width=30)
        self.textbox_password = tk.Entry(self.root, width=30, show="*")

        self.label_username.place(x=indent, y=30)
        self.label_password.place(x=indent, y=70)
        self.root.update_idletasks()
        self.textbox_username.place(
            x=indent + self.label_username.winfo_x() + self.label_username.winfo_width(),
            y=self.label_username.winfo_y(),
        )
        self.textbox_password.place(
            x=indent + self.label_password.winfo_x() + self.label_password.winfo_width(),
            y=self.label_password.winfo_y(),
        )

        self.button_login = tk.Button(self.root, text="login", width=17, command=self.button_login_click)
        self.button_login.place(x=indent, y=110)
        self.button_register = tk.Button(self.root, text="register", width=17, command=self.button_register_click)
        self.button_register.place(x=150, y=110)
        self.button_username_paste = tk.Button(
            self.root,
            text="paste",
            width=5,
            pady=0,
            command=lambda: (
                self.textbox_username.delete(0, tk.END),
                self.textbox_username.insert(0, self.root.clipboard_get()),
            ),
        )
        self.root.update_idletasks()
        self.button_username_paste.place(
            x=300,
            y=self.textbox_username.winfo_y(),
            height=self.textbox_username.winfo_height()+2,
        )

        self.label_wrong = tk.Label(self.root, text="", fg="red")
        self.label_wrong.place(x=indent, y=155)

        self.root.mainloop()

    def button_login_click(self):
        am = AccountManager()
        password=self.textbox_password.get()
        username=self.textbox_username.get()
        if am.get_public_key(password)==username:
            private_key=am.get_private_key(password)
            public_key=username
            self.root.destroy()
            translator_view(private_key, public_key)
        else:
            self.label_wrong.config(text="Incorrect username and password.")

    def button_register_click(self):
        self.root.destroy()
        register_view()
