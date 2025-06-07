# src/parser/comp/user_form/__init__.py
from . import model, services, view, controller, widgets

class UserFormWindow:
    def __init__(self):
        self.model = model.UserModel()
        self.backup = services.BackupService()
        self.form = widgets.UserForm()
        self.view = view.MainWindow(self.form)
        self.controller = controller.UserController(self.model, self.view, self.backup)

    def show(self):
        self.view.show()