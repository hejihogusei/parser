# src/parser/comp/sheets/__init__.py
from PySide6.QtWidgets import QApplication, QMainWindow

from .model                 import SheetsModel     #  main Sheets Model
from .widgets               import SheetsWidget
from .view                  import SheetsView
from .controller            import SheetsController   # main Sheets Controller


__all__ = ["SheetsWindow"]


class SheetsWindow:
    """Top-level façade used by the application."""

    def __init__(self, path_or_df):
        # 1. model layer
        self.model  = SheetsModel(path_or_df)

        # 2. view layer
        self.widget = SheetsWidget()
        self.view   = SheetsView(self.widget)

        # 3. controller layer (CardViewController internally
        #    creates NavigationController & TableSizer)
        self.controller = SheetsController(self.model, self.widget)

    # delegate show ----------------------------------------------------
    def show(self):
        self.view.show()