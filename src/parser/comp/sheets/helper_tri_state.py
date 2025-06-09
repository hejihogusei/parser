# src/parser/comp/sheets/helper_tri_state.py

from __future__ import annotations
from PySide6.QtCore    import Qt, QEvent
from PySide6.QtWidgets import QStyledItemDelegate


def tri_flag() -> Qt.ItemFlag:
    """
    Return the correct tristate‐checkbox flag on this Qt build.
    """
    # top‐level
    if hasattr(Qt, "ItemIsTristate"):
        return Qt.ItemIsTristate
    if hasattr(Qt, "ItemIsAutoTristate"):
        return Qt.ItemIsAutoTristate
    # namespaced under ItemFlag
    if hasattr(Qt.ItemFlag, "ItemIsTristate"):
        return Qt.ItemFlag.ItemIsTristate
    if hasattr(Qt.ItemFlag, "ItemIsAutoTristate"):
        return Qt.ItemFlag.ItemIsAutoTristate
    return Qt.NoItemFlags


TRI_FLAG = tri_flag()


class TriStateDelegate(QStyledItemDelegate):
    """
    Delegate to cycle ☑ → ☐ → ▣ → ☑ in column 0 of CardTableQtModel.
    After each click it calls model.setData(..., CheckStateRole),
    letting your Qt‐model (CardTableQtModel) update the CardTableModel
    and emit the right signals.
    """

    CYCLE = {
        Qt.Checked:           Qt.Unchecked,
        Qt.Unchecked:         Qt.PartiallyChecked,
        Qt.PartiallyChecked:  Qt.Checked,
        None:                 Qt.Checked,
    }

    def __init__(self, parent=None):
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        # only intercept mouse‐release in the checkbox column
        if index.column() == 0 and event.type() == QEvent.MouseButtonRelease:
            current = model.data(index, Qt.CheckStateRole)
            try:
                current = Qt.CheckState(current)
            except (ValueError, TypeError):
                current = None
            nxt = self.CYCLE.get(current, Qt.Checked)
            model.setData(index, nxt, Qt.CheckStateRole)
            return True
        return super().editorEvent(event, model, option, index)
