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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Form")

        self.form = UserForm()
        self.save_btn = QPushButton("Save")
        self.restore_btn = QPushButton("Restore")

        layout = QVBoxLayout()
        layout.addWidget(self.form)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.restore_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
