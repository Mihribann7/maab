from models.base import AbstractRole
from abc import ABC
from enum import Enum
from models.notification import Notification


class Role(Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"


class User(AbstractRole, ABC):
    def __init__(self, _id, full_name, email, password, role):
        super().__init__(_id, full_name, email, password)
        self.role = role
        self._notifications = []

    def add_notification(self, message):
        new_id = len(self._notifications) + 1
        notification = Notification(new_id, message, self._id)
        self._notifications.append(notification)

    def view_notifications(self):
        for n in self._notifications:
            print(f"[{n.priority.upper()}] {n.message}")

    def delete_notification(self, notification_id):
        self._notifications = [
            n for n in self._notifications if n.id != notification_id
        ]

    def get_profile(self):
        return {
            "id": self._id,
            "name": self._full_name,
            "email": self._email,
            "role": self.role.value,
            "created_at": self._created_at
        }

    def update_profile(self, full_name=None, email=None, password=None):
        if full_name:
            self._full_name = full_name
        if email:
            self._email = email
        if password:
            self._password_hash = self._hash_password(password)
