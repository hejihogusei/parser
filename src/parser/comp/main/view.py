# src/parser/comp/main/view.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")

        self.launch_user_form_btn = QPushButton("Open User Form")
        self.launch_sheets_btn = QPushButton("View Excel File")

        layout = QVBoxLayout()
        layout.addWidget(self.launch_user_form_btn)
        layout.addWidget(self.launch_sheets_btn)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
