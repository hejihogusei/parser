from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

from .helper_tri_state import TRI_FLAG

class CardViewController:
    COL_SELECT = 0
    COL_FIELD  = 1
    COL_VALUE  = 2

    def __init__(self, table, model):
        self.tbl = table
        self.model = model
        self.tri_flag = TRI_FLAG
        self._show_all = False

    def show_all(self):
        self._show_all = True
        self.tbl.setColumnHidden(self.COL_SELECT, False)
        self._refresh()

    def show_selected(self):
        """
        print(f"show_selected: _show_all: {self._show_all}")
        for row in range(self.tbl.rowCount()):
            item = self.tbl.item(row, self.COL_SELECT)
            if item is None:
                continue
            state = item.checkState()
            print(f"show_selected: row: {row}, state: {state}")
            #self.model.cards[row].show = (state == Qt.Checked)
        """
        self._show_all = False
        self.tbl.setColumnHidden(self.COL_SELECT, True)
        self._refresh()

    def _refresh(self):
        items = self.model.current_items    #   get values from current row
        cards = list(self.model.cards)  #   get column cards
        tbl = self.tbl
        tbl.setRowCount(0)  #   clear all rows in cardview
        tbl.setWordWrap(False)

        for i, card in enumerate(cards):  #  for i, (card, (field, value)) in enumerate(zip(cards, items)):
            field, value = items[card.id]
            if not self._show_all and not card.show:
                #   do not show 'invisible' cards
                continue
            #   add new empty row with index: row, starting at 0
            tbl.insertRow(tbl.rowCount())
            row = tbl.rowCount() - 1

            if self._show_all:
                #   inserting checkboxes column
                chk = QTableWidgetItem()
                chk.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | self.tri_flag)
                if card.disabled:   chk.setCheckState(Qt.PartiallyChecked)
                elif card.show:     chk.setCheckState(Qt.Checked)
                else:               chk.setCheckState(Qt.Unchecked)
                tbl.setItem(row, self.COL_SELECT, chk)

            #   inserting Field and Value columns
            tbl.setItem(row, self.COL_FIELD, QTableWidgetItem(str(field)))
            tbl.setItem(row, self.COL_VALUE, QTableWidgetItem(str(value)))

        tbl.resizeRowsToContents()