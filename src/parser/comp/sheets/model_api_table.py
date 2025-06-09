# src/parser/comp/sheets/model_api_table.py

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QMimeData,
    QSignalBlocker,
)
from .model import SheetsModel
from .helper_tri_state import TRI_FLAG

__all__ = ["CardTableQtModel"]

class CardTableQtModel(QAbstractTableModel):
    def __init__(self, sheets_model: SheetsModel):
        super().__init__()
        self.sheets_model = sheets_model
        self.cardtable = sheets_model.cardtable
        self._show_all = False
        self._drag_ids = []

        self.cardtable.orderChanged.connect(self._reset_model)
        self.cardtable.visibilityChanged.connect(self._reset_model)

    # ─── Public properties ───────────────────────────────
    @property
    def show_all(self) -> bool:
        return self._show_all

    @show_all.setter
    def show_all(self, val: bool):
        if val != self._show_all:
            self._show_all = val
            self._reset_model()

    # ─── Qt API: Structure ───────────────────────────────
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._visible_cards())

    def columnCount(self, parent=QModelIndex()) -> int:
        return 3

    # ─── Qt API: Data ─────────────────────────────────────
    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        card = self._card_by_row(index.row())
        if index.column() == 0 and role == Qt.CheckStateRole:
            return Qt.PartiallyChecked if card.disabled else Qt.Checked if card.show else Qt.Unchecked
        if index.column() == 1 and role == Qt.DisplayRole:
            return card.title
        if index.column() == 2 and role == Qt.DisplayRole:
            return str(self.sheets_model.current_items[card.id][1])
        return None

    def setData(self, index: QModelIndex, value, role=Qt.EditRole) -> bool:
        if (
            index.isValid()
            and index.column() == 0
            and role == Qt.CheckStateRole
            and value is not None
        ):
            try:
                state = Qt.CheckState(value)
            except ValueError:
                return False
            card = self._card_by_row(index.row())
            self.cardtable.update_visibility(card.id, state)
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return False

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        base = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self._show_all:
            if index.column() == 0:
                base |= Qt.ItemIsUserCheckable | TRI_FLAG
            base |= Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
        return base

    def headerData(self, section: int, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return {0: "✓", 1: "Field", 2: "Value"}.get(section, "")
        return super().headerData(section, orientation, role)

    # ─── Qt API: Drag & Drop ──────────────────────────────
    def supportedDropActions(self):
        return Qt.MoveAction

    def mimeTypes(self):
        return ["application/x-qabstractitemmodeldatalist"]

    def mimeData(self, indexes):
        md = super().mimeData(indexes)
        self._drag_ids = {
            self._card_by_row(ix.row()).id
            for ix in indexes
            if ix.isValid() and ix.column() == 0
        }
        return md

    def dropMimeData(self, mime: QMimeData, action, row, column, parent) -> bool:
        if action != Qt.MoveAction or not self._show_all or not self._drag_ids:
            return super().dropMimeData(mime, action, row, column, parent)

        dest_row = self._resolve_drop_row(row, parent)
        full_ids = [c.id for c in sorted(self.cardtable.cards, key=lambda c: c.order)]
        vis_ids = [cid for cid in full_ids if self.cardtable.by_id(cid).show or self._show_all]

        try:
            old_indexes = [vis_ids.index(cid) for cid in self._drag_ids]
        except ValueError:
            return False

        first, last = min(old_indexes), max(old_indexes)
        if dest_row > last:
            dest_row -= (last - first + 1)
        if first <= dest_row <= last:
            return False

        moving = vis_ids[first: last + 1]
        new_vis = vis_ids[:first] + vis_ids[last + 1:]
        new_vis = new_vis[:dest_row] + moving + new_vis[dest_row:]
        new_full = self._rebuild_full_ids(full_ids, vis_ids, new_vis)

        self.beginMoveRows(QModelIndex(), first, last, QModelIndex(), dest_row)
        with QSignalBlocker(self.cardtable):
            self.cardtable.reorder_by_list(new_full)
        self.endMoveRows()
        return True

    # ─── Internal Sync ────────────────────────────────────
    def _reset_model(self):
        self.beginResetModel()
        self.endResetModel()

    # ─── Private Helpers ──────────────────────────────────
    def _visible_cards(self) -> list:
        return sorted(self.cardtable.visible_cards(self._show_all), key=lambda c: c.order)

    def _card_by_row(self, row: int):
        cards = self._visible_cards()
        return cards[row] if 0 <= row < len(cards) else None

    def _resolve_drop_row(self, row, parent):
        if row >= 0:
            return row
        elif parent.isValid():
            return parent.row()
        return self.rowCount()

    def _rebuild_full_ids(self, full_ids, vis_ids, new_vis):
        vis_set = set(vis_ids)
        vis_map = dict(zip(vis_ids, new_vis))
        return [vis_map[cid] if cid in vis_set else cid for cid in full_ids]
