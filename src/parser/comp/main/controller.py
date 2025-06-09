# src/parser/comp/main/controller.py
from comp.user_form import UserFormWindow
from comp.sheets import SheetsWindow    #   entry point into Sheets

class MainAppController:
    def __init__(self, view, excel_path):
        self.view = view
        self._connect_signals()
        self.excel_path = excel_path

    def _connect_signals(self):
        self.view.launch_user_form_btn.clicked.connect(self._show_user_form)
        self.view.launch_sheets_btn.clicked.connect(self._show_sheets_viewer)

    def _show_user_form(self):
        self.user_form = UserFormWindow()
        self.user_form.show()

    def _show_sheets_viewer(self):
        #   calls up Sheets MVC
        self.sheets_window = SheetsWindow(self.excel_path)
        self.sheets_window.show()