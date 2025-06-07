# src/parser/comp/sheets/__init__.py
from PySide6.QtWidgets import QMainWindow, QApplication

from .model import SheetModel
from .widgets import SheetWidget
from .view import MainWindow
from .controller import ExcelViewerController

class ExcelViewerWindow:
    def __init__(self, path):
        self.model = SheetModel(path)
        self.widget = SheetWidget()
        self.view = MainWindow(self.widget)
        self.controller = ExcelViewerController(self.model, self.widget)


    def show(self):
        self.view.show()

