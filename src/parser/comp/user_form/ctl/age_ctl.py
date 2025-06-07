# src/parser/comp/user_form/ctl/age_ctl.py
class AgeController:
    def __init__(self, spinbox, model):
        self.spinbox = spinbox
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        self.spinbox.setValue(self.model.age)
        self.spinbox.valueChanged.connect(self.on_age_changed)

    def on_age_changed(self, value):
        self.model.age = value
