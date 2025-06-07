# src/parser/comp/sheets/view.py
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self, form_widget):
        super().__init__()
        self.setWindowTitle("Excel Viewer")
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setCentralWidget(form_widget)
        self._centered = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self._centered:
            QTimer.singleShot(0, self._center_on_screen)
            self._centered = True

    def _center_on_screen(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())






