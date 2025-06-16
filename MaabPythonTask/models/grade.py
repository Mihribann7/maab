from datetime import datetime


class Grade:
    def __init__(self, _id, student_id, subject, value, teacher_id, comment=""):
        self.id = _id
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = datetime.now().isoformat()
        self.teacher_id = teacher_id
        self.comment = comment

    def update_grade(self, value, comment=None):
        self.value = value
        if comment is not None:
            self.comment = comment
        self.date = datetime.now().isoformat()

    def get_grade_info(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "comment": self.comment
        }
