from abc import ABC, abstractmethod
from datetime import datetime
import hashlib


class AbstractRole(ABC):
    def __init__(self, _id, full_name, email, password):
        self._id = _id
        self._full_name = full_name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._created_at = datetime.now().isoformat()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    @abstractmethod
    def get_profile(self):
        pass

    @abstractmethod
    def update_profile(self, full_name=None, email=None, password=None):
        pass
