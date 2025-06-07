# src/parser/comp/user_form/ctl/name_ctl.py
class NameController:
    def __init__(self, line_edit, model):
        self.line_edit = line_edit
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        self.line_edit.setText(self.model.name)
        self.line_edit.textChanged.connect(self.on_name_changed)

    def on_name_changed(self, text):
        self.model.name = text
