from datetime import date
class User:
    def __init__(self, id, login, password, role):
        self.id = id
        self.login = login
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "password": self.password,
            "role": self.role,
        }

class Student(User):
    def __init__(self, id, login, password, full_name, group, contact, direction, participation_form, created_at=None):
        super().__init__(id, login, password, "Студент")
        self.full_name = full_name
        self.group = group
        self.contact = contact
        self.direction = direction
        self.participation_form = participation_form
        self.created_at = created_at if created_at else str(date.today())

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "full_name": self.full_name,
            "group": self.group,
            "contact": self.contact,
            "direction": self.direction,
            "participation_form": self.participation_form,
            "created_at": self.created_at,
        })
        return data

class Organizer(User):
    def __init__(self, id, login, password, full_name, contact, position="", created_at=None):
        super().__init__(id, login, password, "Организатор")
        self.full_name = full_name
        self.contact = contact
        self.position = position
        self.created_at = created_at if created_at else str(date.today())

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "full_name": self.full_name,
            "contact": self.contact,
            "position": self.position,
            "created_at": self.created_at,
        })
        return data