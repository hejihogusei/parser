# src/parser/comp/sheets/controller_nav.py
from PySide6.QtCore import QObject, Signal


class NavigationController(QObject):
    """
    Handles prev/next buttons with wrap-around,
    emits rowChanged(idx).
    """

    rowChanged: Signal = Signal(int)

    def __init__(self, row_model, prev_btn, next_btn):
        super().__init__()
        self._rows = row_model
        prev_btn.clicked.connect(self._prev)
        next_btn.clicked.connect(self._next)

    # -------------------------------------------------------------------
    def _prev(self):
        self._rows.index = (self._rows.index - 1) % self._rows.row_count
        self.rowChanged.emit(self._rows.index)

    def _next(self):
        self._rows.index = (self._rows.index + 1) % self._rows.row_count
        self.rowChanged.emit(self._rows.index)