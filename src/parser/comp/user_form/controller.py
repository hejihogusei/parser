# src/parser/comp/user_form/controller.py
from comp.user_form.ctl.name_ctl import NameController
from comp.user_form.ctl.age_ctl import AgeController
from comp.user_form.ctl.flavor_ctl import FlavorController

class UserController:
    def __init__(self, model, view, backup_service):
        self.model = model
        self.view = view
        self.backup_service = backup_service

        self.name_ctl = NameController(view.form.name, model)
        self.age_ctl = AgeController(view.form.age, model)
        self.flavor_ctl = FlavorController(view.form.icecream, model)

        view.save_btn.clicked.connect(self.handle_save)
        view.restore_btn.clicked.connect(self.handle_restore)

    def handle_save(self):
        self.backup_service.save(self.model.to_dict())

    def handle_restore(self):
        data = self.backup_service.restore()
        if data:
            self.model.update_from_dict(data)
            self.view.form.name.setText(self.model.name)
            self.view.form.age.setValue(self.model.age)
            self.view.form.icecream.setCurrentText(self.model.flavor)
