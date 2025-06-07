# src/parser/comp/sheets/controller.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtGui import QFontMetrics


class ExcelViewerController:
    def __init__(self, model, widget):
        self.model = model
        self.widget = widget
        self.table = widget.table
        self.hdr_height = 0
        self.hdr = self.table.horizontalHeader()

        # set sizing
        self.default_sizing()

        # Connect navigation buttons
        self.widget.prev_btn.clicked.connect(self.on_prev)
        self.widget.next_btn.clicked.connect(self.on_next)

        # Load the first row
        self.load_row()

    def default_sizing(self):
        # set default sizing
        def c2px(n: int, pad: int = 8) -> int:
            fm: QFontMetrics = self.widget.fontMetrics()
            return fm.horizontalAdvance('M' * n) + pad  # 'M' ≈ widest latin
        self.hdr_height = self.hdr.height()
        self.table.verticalHeader().setDefaultSectionSize(self.hdr_height)
        min_width = c2px(self.model.title_width) + c2px(self.model.col_width)   # + self.table.columnWidth(0)
        self.table.setMinimumWidth(min_width)
        self.hdr.setStretchLastSection(True)

    def on_prev(self):
        self.model.prev()
        self.load_row()

    def on_next(self):
        self.model.next()
        self.load_row()

    def load_row(self):
        row, items  = self.model.current_row
        if row is not None:
            self.set_row(row, items)

    def set_row(self, row_series, items):
        self.widget.table.setRowCount(len(items))
        for i, (col, val) in enumerate(items):
            self.widget.table.setItem(i, 1, QTableWidgetItem(str(col)))
            self.widget.table.setItem(i, 2, QTableWidgetItem(str(val)))
        self.resize_table_to_fit_rows()

    def resize_table_to_fit_rows(self):
        def calc_height(table):
            total_height = sum(table.rowHeight(row) for row in range(table.rowCount()))
            return total_height + self.hdr_height + 20

        self.widget.table.resizeColumnsToContents()
        self.widget.table.resizeRowsToContents()

        height = calc_height(self.widget.table)
        self.widget.table.setMinimumHeight(height)
        self.widget.table.setMaximumHeight(height)

        #if not self._table_width:
        #    self._table_width = self.widget.table.size().width() * 1.5
        #self.widget.table.setMinimumWidth(self._table_width)
        #self.widget.table.setMaximumWidth(self._table_width)

        # Optionally: Ask parent to update layout
        self.widget.table.updateGeometry()
        self.widget.updateGeometry()

