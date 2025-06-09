# src/parser/comp/sheets/widgets.py

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy, QHeaderView, QAbstractItemView
)
from PySide6.QtGui import QFont


class SheetsWidget(QWidget):
    """
    ✓‐tri‐state | Field | Value
    UI‐only container; all data logic lives in controllers/models.
    Uses QTableView + QAbstractTableModel (CardTableQtModel).
    """

    # ── column indexes ─────────────────────────────────────────────
    COL_SELECT, COL_FIELD, COL_VALUE = range(3)

    def __init__(self) -> None:
        super().__init__()

        # ---- table view ------------------------------------------------
        self.table = QTableView(self)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setWordWrap(False)

        # enable internal drag & drop; model.moveRows handles reordering
        #self.table.setDragEnabled(True)
        #self.table.setAcceptDrops(True)
        #self.table.setDropIndicatorShown(True)
        #self.table.setDragDropMode(QAbstractItemView.InternalMove)
        #self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # header styling
        hdr = self.table.horizontalHeader()
        header_font = hdr.font()
        header_font.setBold(True)
        header_font.setPointSize(header_font.pointSize() + 2)
        hdr.setFont(header_font)
        hdr.setSectionResizeMode(QHeaderView.Fixed)

        # ---- navigation buttons ---------------------------------------
        self.toggle_show_btn = QPushButton("Show/Hide", self)
        self.prev_btn        = QPushButton("← Previous", self)
        self.next_btn        = QPushButton("Next →", self)

        # ---- layout: buttons ------------------------------------------
        buttons = QHBoxLayout()
        buttons.addWidget(self.toggle_show_btn)
        buttons.addStretch()
        buttons.addWidget(self.prev_btn)
        buttons.addWidget(self.next_btn)
        buttons.addStretch()

        # ---- main layout ----------------------------------------------
        root = QVBoxLayout(self)
        root.addWidget(self.table, stretch=1)
        root.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        #root.addStretch()
        root.addLayout(buttons)
        self.setLayout(root)