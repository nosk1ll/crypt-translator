import customtkinter as ctk
from login_view import login_view
from register_view import register_view
from registered_ok import registered_ok
from main_menu_view import main_menu_view
from ui_theme import AUTH_BG, MAIN_BG

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("crypt-translator")
        self.configure(fg_color=AUTH_BG)
        self.resizable(False, False)

        self.private_key = None
        self.public_key = None
        self.recipient_public_key = None
        self.cipher = None

        self.login = login_view(self, self)
        self.register = register_view(self, self)
        self.registered = registered_ok(self, self)
        self.main_menu = main_menu_view(self, self)

        self.show_login()

    def _show(self, view, geometry):
        self.geometry(geometry)
        self.configure(fg_color=MAIN_BG if view is self.main_menu else AUTH_BG)
        for other in (self.login, self.register, self.registered, self.main_menu):
            if other is view:
                other.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                other.place_forget()

    def show_login(self):
        self.login.reset()
        self._show(self.login, "900x560")

    def show_register(self):
        self.register.reset()
        self._show(self.register, "900x560")

    def show_registered_ok(self, username):
        self.registered.set_username(username)
        self._show(self.registered, "500x150")

    def open_translator(self, private_key, public_key):
        self.main_menu.set_keys(private_key, public_key)
        self._show(self.main_menu, "900x560")


if __name__ == "__main__":
    AuthApp().mainloop()
