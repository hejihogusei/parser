class FlavorController:
    def __init__(self, combo, model):
        self.combo = combo
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        self.combo.setCurrentText(self.model.flavor)
        self.combo.currentTextChanged.connect(self.on_flavor_changed)

    def on_flavor_changed(self, text):
        self.model.flavor = text
