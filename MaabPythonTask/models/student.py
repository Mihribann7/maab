from models.user_base import User
from models.user_base import Role


class Student(User):
    def __init__(self, _id, full_name, email, password, grade, subjects=None):
        super().__init__(_id, full_name, email, password, Role.STUDENT)
        self.grade = grade
        self.subjects = subjects if subjects else {}
        self.assignments = {}
        self.grades = {}

    def submit_assignment(self, assignment_id, content):
        self.assignments[assignment_id] = {
            "status": "submitted",
            "content": content
        }

    def view_grades(self, subject=None):
        if subject:
            return self.grades.get(subject, [])
        return self.grades

    def calculate_average_grade(self):
        all_grades = []
        for grade_list in self.grades.values():
            all_grades.extend(grade_list)
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)
