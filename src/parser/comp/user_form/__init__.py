from . import model, services, view, controller

class UserFormWindow:
    def __init__(self):
        self.model = model.UserModel()
        self.backup = services.BackupService()
        self.view = view.MainWindow()
        self.controller = controller.UserController(self.model, self.view, self.backup)

    def show(self):
        self.view.show()