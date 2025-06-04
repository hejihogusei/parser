from PySide6.QtWidgets import QApplication
import sys

from comp.user_form import UserFormWindow

def main():
    app = QApplication(sys.argv)

    user_form = UserFormWindow()
    user_form.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()