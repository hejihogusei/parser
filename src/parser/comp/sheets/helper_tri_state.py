# src/parser/comp/sheets/helper_tri_state.py
from __future__ import annotations
from PySide6.QtCore    import Qt, QEvent
from PySide6.QtWidgets import QStyledItemDelegate


# ─────────────────────────  helpers  ──────────────────────────
def tri_flag() -> int:
    """
    Return `Qt.ItemIsTristate` that works on the current PySide build.
    Raises if the build has no user-clickable tri-state support.
    """
    # Qt 6 namespaced enum
    if hasattr(Qt.ItemFlag, "ItemIsTristate"):
        return Qt.ItemFlag.ItemIsTristate

    if hasattr(Qt.ItemFlag, "ItemIsAutoTristate"):
        return Qt.ItemFlag.ItemIsAutoTristate

    # Fallback: some builds expose only 'ItemIsAutoTristate'
    if hasattr(Qt, "ItemIsAutoTristate"):
        return Qt.ItemIsAutoTristate

    # Last resort: no tri-state available
    return 0


TRI_FLAG = tri_flag()        # exported constant


# ──────────────────────  delegate class  ─────────────────────
class TriStateDelegate(QStyledItemDelegate):
    """
    Delegate that cycles ☐  ▣  ☑  states on every user activation.
    Install per column:

        from .tri_state_delegate import TriStateDelegate, TRI_FLAG
        self.table.setItemDelegateForColumn(select_col, TriStateDelegate(self.table, self.model))
    """
    def __init__(self, table, model):
        super().__init__(table)
        self.model = model

    CYCLE = {
        Qt.Checked:             Qt.Unchecked,  # ✔ → □
        Qt.Unchecked:           Qt.PartiallyChecked,  # □ → ▣
        Qt.PartiallyChecked:    Qt.Checked,  # ▣ → ✔
        None:                   Qt.Checked,  # safety fallback
    }
    # ----------------------------------------------------------
    def editorEvent(self, event, model, option, index):
        # Handle mouse-release, key-press etc.
        if (event.type() == QEvent.MouseButtonRelease ):
            state = index.data(Qt.CheckStateRole)
            # Normalize to Qt.CheckState
            try:
                state = Qt.CheckState(state)
            except ValueError:
                state = None
            next_state = self.CYCLE.get(state, Qt.Checked)
            model.setData(index, next_state, Qt.CheckStateRole)

            # Update underlying card model directly
            self.model.cardtable.update_visibility(index.row(), next_state)

            return True                                   # event handled
        return super().editorEvent(event, model, option, index)



