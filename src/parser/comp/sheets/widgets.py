     # src/parser/comp/sheets/widgets.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy, QHeaderView
)
from PySide6.QtGui import QFont


class SheetWidget(QWidget):
    """
    ✓-show | ✓-disable | Field | Value
    Value-column width is injected (default 200) so the controller
    can later pass a dynamic value.
    """

    def __init__(self) -> None:
        super().__init__()

        # ---- table --------------------------------------------------
        self.table = QTableWidget(0, 3, self)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setHorizontalHeaderLabels(["Select", "Field", "Value"])
        header_font = QFont(); header_font.setBold(True)
        self.table.horizontalHeader().setFont(header_font)  # makes all header cells bold

        # ---- navigation buttons -------------------------------------
        self.toggle_show_btn = QPushButton("Show/Hide", self)
        self.prev_btn        = QPushButton("← Previous", self)
        self.next_btn        = QPushButton("Next →", self)

        # ---- layout -------------------------------------------------
        buttons = QHBoxLayout()
        buttons.addWidget(self.toggle_show_btn)
        buttons.addStretch()
        buttons.addWidget(self.prev_btn)
        buttons.addWidget(self.next_btn)
        buttons.addStretch()

        root = QVBoxLayout(self)
        root.addWidget(self.table)
        root.addItem(QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        root.setStretch(1, 1)  # spacer stretches
        root.addLayout(buttons)