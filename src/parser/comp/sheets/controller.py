# src/parser/comp/sheets/controller.py

from __future__ import annotations
from PySide6.QtCore    import Qt, QModelIndex
from PySide6.QtWidgets import QAbstractItemView
from .helper_table_sizer import set_initial_sizing
from .model_api_table    import CardTableQtModel
from .controller_nav     import NavigationController
from .helper_tri_state  import TriStateDelegate, TRI_FLAG


class SheetsController:
    COL_SELECT, COL_FIELD, COL_VALUE = range(3)

    def __init__(self, model, widget):
        self.model  = model
        self.widget = widget
        self.view   = widget.table  # QTableView

        # 1) install our QAbstractTableModel
        self.qt_model = CardTableQtModel(self.model)
        self.view.setModel(self.qt_model)

        # 2) Configure drag & drop *in the controller*
        self._setup_drag_drop()

        self.view.setEditTriggers(
            #QAbstractItemView.NoEditTriggers
            QAbstractItemView.EditKeyPressed
            | QAbstractItemView.AnyKeyPressed
            | QAbstractItemView.DoubleClicked
        )

        #   tri-state checkbox support
        delegate = TriStateDelegate(self.view)
        self.view.setItemDelegateForColumn(self.COL_SELECT, delegate)

        # 2) initial sizing
        set_initial_sizing(self.widget, self.model)

        # 3) navigation
        self.nav = NavigationController(
            self.model.rows,
            self.widget.prev_btn,
            self.widget.next_btn
        )
        self.nav.rowChanged.connect(self._on_row_changed)
        self._on_row_changed(self.model.rows.index)

        # 4) show/hide toggle
        self.widget.toggle_show_btn.clicked.connect(self._toggle_show_mode)
        # start in “view mode” (no edit): hide checkbox column
        self.qt_model.show_all = False
        self.view.setColumnHidden(self.COL_SELECT, True)
        self.widget.toggle_show_btn.setText("Show")

    def _setup_drag_drop(self) -> None:
        """
        Turn on internal‐move drag & drop for the table view.
        """
        self.view.setDragEnabled(True)
        self.view.setAcceptDrops(True)
        self.view.setDropIndicatorShown(True)
        self.view.setDragDropMode(QAbstractItemView.InternalMove)   #   DragDrop
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)

    def _toggle_show_mode(self):
        """Flip between edit (show_all) and view modes."""
        new_mode = not self.qt_model.show_all
        # 1) update model
        self.qt_model.show_all = new_mode
        # 2) show/hide the checkbox column
        self.view.setColumnHidden(self.COL_SELECT, not new_mode)
        # 3) update button label
        self.widget.toggle_show_btn.setText("Hide" if new_mode else "Show")
        # 4) force a full layout pass so the checkboxes appear/disappear
        self.qt_model.layoutChanged.emit()

    def _on_row_changed(self, idx: int) -> None:
        """Refresh the 'Value' column and row heights when the current row changes."""
        top    = self.qt_model.index(0, self.COL_VALUE)
        bottom = self.qt_model.index(self.qt_model.rowCount() - 1, self.COL_VALUE)
        self.qt_model.dataChanged.emit(top, bottom, [Qt.DisplayRole])
        self.view.resizeRowsToContents()
