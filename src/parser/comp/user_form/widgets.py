# src/parser/comp/user_form/widgets.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QSpinBox, QComboBox

class UserForm(QWidget):
    def __init__(self):
        super().__init__()
        self.name = QLineEdit()
        self.age = QSpinBox()
        self.age.setRange(0, 200)
        self.icecream = QComboBox()
        self.icecream.addItems(["Vanilla", "Strawberry", "Chocolate"])

        layout = QFormLayout()
        layout.addRow("Name", self.name)
        layout.addRow("Age", self.age)
        layout.addRow("Favorite Ice cream", self.icecream)

        self.setLayout(layout)