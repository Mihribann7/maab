from datetime import datetime


class Notification:
    def __init__(self, _id, message, recipient_id, priority="normal"):
        self.id = _id
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = datetime.now().isoformat()
        self.priority = priority

    def send(self):
        return {
            "id": self.id,
            "message": self.message,
            "recipient_id": self.recipient_id,
            "created_at": self.created_at,
            "priority": self.priority,
            "status": "sent"
        }

    def get_notification_info(self):
        return {
            "id": self.id,
            "message": self.message,
            "recipient_id": self.recipient_id,
            "created_at": self.created_at,
            "priority": self.priority
        }
