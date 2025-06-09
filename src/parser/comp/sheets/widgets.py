# src/parser/comp/sheets/widgets.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy, QHeaderView
)
from PySide6.QtGui import QFont


class SheetsWidget(QWidget):
    """
    ✓‐tri-state | Field | Value
    UI-only container; all data logic lives in controllers/models.
    """

    # ── expose column indexes so controllers don't hard-code numbers
    COL_SELECT, COL_FIELD, COL_VALUE = range(3)

    def __init__(self) -> None:
        super().__init__()

        # ---- table --------------------------------------------------
        self.table = QTableWidget(0, 3, self)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setHorizontalHeaderLabels(["✓", "Field", "Value"])

        hdr = self.table.horizontalHeader()
        # start from the header’s current font so you inherit family/size
        header_font = hdr.font()
        header_font.setBold(True)
        header_font.setPointSize(header_font.pointSize() + 2)  # +2 pt
        hdr.setFont(header_font)

        # ---- navigation buttons -------------------------------------
        self.toggle_show_btn = QPushButton("Show/Hide", self)
        self.prev_btn = QPushButton("← Previous", self)
        self.next_btn = QPushButton("Next →", self)

        # ---- Navigation Buttons (sub-View) layout -------------------------------------------------
        buttons = QHBoxLayout()
        buttons.addWidget(self.toggle_show_btn)
        buttons.addStretch()
        buttons.addWidget(self.prev_btn)
        buttons.addWidget(self.next_btn)
        buttons.addStretch()

        # ---- Card View (Table & Buttons) layout -------------------------------------------------
        root = QVBoxLayout(self)
        root.addWidget(self.table, stretch= 1)  # index 0
        root.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding))  # index 1
        root.addStretch(1)
        root.addLayout(buttons)  # index 2