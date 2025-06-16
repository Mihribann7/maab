from models.user_base import User, Role


class Parent(User):
    def __init__(self, _id, full_name, email, password, children=None):
        super().__init__(_id, full_name, email, password, Role.PARENT)
        self.children = children if children else []

    def view_child_grades(self, child):
        if child._id in self.children:
            return child.view_grades()
        return "Invalid child id"

    def view_child_assignments(self, child):
        if child._id in self.children:
            return child.assignments
        return "Invalid child id"

    def receive_child_notification(self, child):
        if child._id in self.children:
            return child.view_notifications()
        return "Invalid child id"
