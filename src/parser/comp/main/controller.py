# src/parser/comp/main/controller.py
from comp.user_form import UserFormWindow
from comp.sheets import ExcelViewerWindow

class MainAppController:
    def __init__(self, view, excel_path):
        self.view = view
        self._connect_signals()
        self.excel_path = excel_path

    def _connect_signals(self):
        self.view.launch_user_form_btn.clicked.connect(self._show_user_form)
        self.view.launch_excel_btn.clicked.connect(self._show_excel_viewer)

    def _show_user_form(self):
        self.user_form = UserFormWindow()
        self.user_form.show()

    def _show_excel_viewer(self):
        self.excel_window = ExcelViewerWindow(self.excel_path)
        self.excel_window.show()