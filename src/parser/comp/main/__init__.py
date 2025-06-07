# src/parser/comp/main/__init__.py
from .view import MainAppWindow
from .controller import MainAppController

class MainApp:
    def __init__(self, excel_path):
        self.view = MainAppWindow()
        self.controller = MainAppController(self.view, excel_path)

    def show(self):
        self.view.show()