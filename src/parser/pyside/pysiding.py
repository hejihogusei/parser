import sys
from PySide6.QtCore import QSize, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QMainWindow, QVBoxLayout, QTextEdit, QLabel, QLineEdit, QHBoxLayout
)


class StreamToTextEdit:
    def __init__(self, widget):
        self.widget = widget
    def write(self, msg):
        if msg.strip():
            QTimer.singleShot(0, lambda: self.widget.append(msg.strip()))
    def flush(self): pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 App")
        self.setMinimumSize(QSize(1280, 720))
        #self.setMaximumSize(QSize(1280, 720))

        # Redirect print() to console
        self.console = QTextEdit()
        self.console.setMaximumSize(QSize(1280, 200))
        self.console.setReadOnly(True)
        sys.stdout = StreamToTextEdit(self.console)
        #sys.stderr = StreamToTextEdit(self.console)
        ######


        ######
        self.layout()


        ######
    def layout(self):
        frame = QVBoxLayout()
        container = QWidget()
        container.setLayout(frame)
        layout = QHBoxLayout()
        frame.addLayout(layout)
        frame.addWidget(self.console)
        self.setCentralWidget(container)
        ######
        layout.addWidget(Color("red"))
        layout.addWidget(Color("blue"))
        layout.addWidget(Color("green"))



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
