# src/parser/comp/sheets/controller.py
from __future__ import annotations
from PySide6.QtCore    import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from .helper_table_sizer        import set_initial_sizing
from .helper_tri_state          import TriStateDelegate, TRI_FLAG
from .controller_nav            import NavigationController
from .controller_visibility     import VisibilityController
from .controller_cardview       import CardViewController


class SheetsController:
    COL_SELECT, COL_FIELD, COL_VALUE = range(3)

    def __init__(self, model, widget):
        self.model  = model
        self.widget = widget
        self.tbl    = widget.table
        self.tri_flag = TRI_FLAG

        self._setup_tri_state_delegate()
        self._setup_initial_sizing()
        self._setup_cardview()
        self._setup_visibility_controller()
        self._setup_navigation()

        self._refresh(model.rows.index)

    # ─────────────────────────────────────────────────────────────
    def _setup_tri_state_delegate(self):
        delegate = TriStateDelegate(self.tbl, self.model)
        self.tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbl.setItemDelegateForColumn(self.COL_SELECT, delegate)

    def _setup_initial_sizing(self):
        set_initial_sizing(self.widget, self.model)

    def _setup_cardview(self):
        self.cardview_controller = CardViewController(self.tbl, self.model)
        #self.cardview_controller.show_selected()

    def _setup_visibility_controller(self):
        self.toggle_ctrl = VisibilityController(
            button=self.widget.toggle_show_btn,
            table=self.tbl,
            cardview_controller=self.cardview_controller
        )
        self.toggle_ctrl.install()

    def _setup_navigation(self):
        self.nav = NavigationController(
            self.model.rows,
            self.widget.prev_btn,
            self.widget.next_btn
        )
        self.nav.rowChanged.connect(self._refresh)

    # ─────────────────────────────────────────────────────────────
    def _refresh(self, _idx: int) -> None:
        if self.toggle_ctrl.show_mode:
            self.cardview_controller.show_all()
        else:
            self.cardview_controller.show_selected()