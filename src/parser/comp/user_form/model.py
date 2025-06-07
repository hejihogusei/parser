# src/parser/comp/user_form/model.py
class UserModel:
    def __init__(self, name="Joanna Doe", age=25, flavor="Vanilla"):
        self.name = name
        self.age = age
        self.flavor = flavor

    def to_dict(self):
        return {"name": self.name, "age": self.age, "flavor": self.flavor}

    def update_from_dict(self, data):
        self.name = data.get("name", self.name)
        self.age = data.get("age", self.age)
        self.flavor = data.get("flavor", self.flavor)
