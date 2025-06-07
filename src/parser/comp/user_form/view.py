# src/parser/comp/user_form/view.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFormLayout, QLineEdit, QSpinBox, QComboBox
)

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("User Form")

        self.form = widget
        self.save_btn = QPushButton("Save")
        self.restore_btn = QPushButton("Restore")

        layout = QVBoxLayout()
        layout.addWidget(self.form)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.restore_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
