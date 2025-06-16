from datetime import datetime


class Assignment:
    def __init__(self, _id, title, description, deadline, subject, teacher_id, class_id, difficulty="o‘rta"):
        self.id = _id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.difficulty = difficulty
        self.submissions = {}
        self.grades = {}

    def add_submission(self, student_id, content):
        if datetime.fromisoformat(self.deadline) < datetime.now():
            return "Late submission."
        self.submissions[student_id] = content
        return "Submission received."

    def set_grade(self, student_id, grade):
        if student_id not in self.submissions:
            return "Student has not submitted this assignment."
        self.grades[student_id] = grade
        return f"Grade {grade} is for student {student_id}."

    def get_status(self):
        return {
            "assignment_id": self.id,
            "title": self.title,
            "submitted": list(self.submissions.keys()),
            "graded": list(self.grades.keys()),
            "pending": list(set(self.submissions.keys()) - set(self.grades.keys()))
        }
