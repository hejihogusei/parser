# src/parser/main.py
from PySide6.QtWidgets import QApplication
import sys
from pathlib import Path

from comp.main import MainApp

def main():
    # Resolve path to project root
    root_path = Path(__file__).resolve().parents[2]
    excel_path = root_path / "temp" / "sheets_old.xlsx"
    print(excel_path)

    app = QApplication(sys.argv)
    main_app = MainApp(excel_path=excel_path)
    main_app.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()