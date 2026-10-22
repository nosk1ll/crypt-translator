import os
from importlib.machinery import SourceFileLoader

login_view = SourceFileLoader(
    "login_view",
    os.path.join(os.path.dirname(__file__), "login_view.view"),
).load_module().login_view

if __name__ == "__main__":
    login_view()
