# src/parser/comp/sheets/controller_visibility.py

from PySide6.QtCore import Qt

class VisibilityController:
    """
    Manages toggling between edit mode (with checkboxes) and view mode (filtered).
    Usage:
        self.toggle_ctrl = ToggleVisibilityController(widget.toggle_show_btn, card_table, self.card_view)
        self.toggle_ctrl.install()
    """

    def __init__(self, button, table, cardview_controller):
        self.button = button
        self.table = table
        self.cardview_controller = cardview_controller
        self._active = False  # False = view mode (filtered)

    @property
    def show_mode(self) -> bool:
        return self._active

    def install(self):
        self.button.clicked.connect(self._toggle)

    def _toggle(self):
        self._active = not self._active
        self.button.setText("Hide" if self._active else "Show")

        if self._active:
            # In edit mode, show all rows with checkboxes
            self.cardview_controller.show_all()
        else:
            # In view mode, show only visible rows (as selected)
            self.cardview_controller.show_selected()