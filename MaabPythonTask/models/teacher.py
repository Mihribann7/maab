from models.user_base import User, Role


class Teacher(User):
    def __init__(self, _id, full_name, email, password, subjects=None, classes=None):
        super().__init__(_id, full_name, email, password, Role.TEACHER)
        self.subjects = subjects if subjects else []
        self.classes = classes if classes else []
        self.assignments = {}

    def create_assignment(self, assignment_id, title, description, deadline, subject, class_id):
        assignment = {
            "id": assignment_id,
            "title": title,
            "description": description,
            "deadline": deadline,
            "subject": subject,
            "teacher_id": self._id,
            "class_id": class_id,
            "submissions": {},
            "grades": {}
        }
        self.assignments[assignment_id] = assignment
        return assignment

    def grade_assignment(self, assignment_id, student_id, grade):
        if assignment_id in self.assignments:
            assignment = self.assignments[assignment_id]
            assignment["grades"][student_id] = grade
            return f"Graded student {student_id} with {grade}"
        return "Assignment not found"

    def view_student_progress(self, student):
        return {
            "student_id": student._id,
            "grades": student.grades,
            "average": student.calculate_average_grade()
        }
