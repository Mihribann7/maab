import csv
import datetime
from abc import ABC, abstractmethod


class AbstractRole(ABC):
    def __init__(self, id, full_name, email, password):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now().isoformat()

    @abstractmethod
    def get_profile(self):
        pass

    @abstractmethod
    def get_menu_options(self):
        pass


class User(AbstractRole):
    def __init__(self, id, full_name, email, password, role):
        super().__init__(id, full_name, email, password)
        self.role = role
        self.notifications = []

    def get_profile(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

    def add_notification(self, message):
        notification = Notification(
            id=len(self.notifications) + 1,
            message=message,
            recipient_id=self.id
        )
        self.notifications.append(notification)
        return notification

    def get_menu_options(self):
        base_options = {
            "1": "View Profile",
            "0": "Logout"
        }
        return base_options


class Student(User):
    def __init__(self, id, full_name, email, password, grade):
        super().__init__(id, full_name, email, password, "Student")
        self.grade = grade
        self.assignments = {}
        self.grades = []

    def submit_assignment(self, assignment_id, content):
        if assignment_id in self.assignments:
            return False
        self.assignments[assignment_id] = {
            "content": content,
            "submitted_at": datetime.datetime.now().isoformat()
        }
        return True

    def view_grades(self):
        return self.grades

    def get_menu_options(self):
        options = super().get_menu_options()
        options.update({
            "2": "Submit Assignment",
            "3": "View Grades"
        })
        return options


class Teacher(User):
    def __init__(self, id, full_name, email, password):
        super().__init__(id, full_name, email, password, "Teacher")
        self.assignments = []

    def create_assignment(self, title, description, deadline, subject, class_id):
        assignment = Assignment(
            title=title,
            description=description,
            deadline=deadline,
            subject=subject,
            teacher_id=self.id,
            class_id=class_id
        )
        self.assignments.append(assignment)
        return assignment

    def grade_assignment(self, student, assignment_id, grade_value):
        grade = Grade(
            student_id=student.id,
            subject="Math",
            value=grade_value,
            teacher_id=self.id
        )
        student.grades.append(grade)
        return grade

    def get_menu_options(self):
        options = super().get_menu_options()
        options.update({
            "2": "Create Assignment",
            "3": "Grade Assignment"
        })
        return options


class Parent(User):
    def __init__(self, id, full_name, email, password):
        super().__init__(id, full_name, email, password, "Parent")
        self.children = []

    def add_child(self, student):
        if student not in self.children:
            self.children.append(student)
            return True
        return False

    def view_child_grades(self, child):
        if child in self.children:
            return child.view_grades()
        return None

    def get_menu_options(self):
        options = super().get_menu_options()
        options.update({
            "2": "View Child Grades"
        })
        return options


class Admin(User):
    def __init__(self, id, full_name, email, password):
        super().__init__(id, full_name, email, password, "Admin")

    def add_user(self, platform, user_type, user_data):
        if user_type == "Student":
            user = Student(None, user_data['name'], user_data['email'], user_data['password'], user_data['grade'])
        elif user_type == "Teacher":
            user = Teacher(None, user_data['name'], user_data['email'], user_data['password'])
        elif user_type == "Parent":
            user = Parent(None, user_data['name'], user_data['email'], user_data['password'])
        elif user_type == "Admin":
            user = Admin(None, user_data['name'], user_data['email'], user_data['password'])
        else:
            return None

        platform.add_user(user)
        return user

    def remove_user(self, platform, user_id):
        user = platform.find_user(user_id)
        if user:
            platform.users.remove(user)
            return True
        return False

    def get_menu_options(self):
        options = super().get_menu_options()
        options.update({
            "2": "Add User",
            "3": "Remove User",
            "4": "View All Users",
            "5": "System Report",
            "6": "Export Data (CSV)"
        })
        return options


class Assignment:
    def __init__(self, title, description, deadline, subject, teacher_id, class_id):
        self.id = None
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.submissions = []


class Grade:
    def __init__(self, student_id, subject, value, teacher_id):
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.teacher_id = teacher_id
        self.date = datetime.datetime.now().isoformat()

    def __str__(self):
        return f"{self.subject}: {self.value} (by Teacher {self.teacher_id})"


class Notification:
    def __init__(self, id, message, recipient_id):
        self.id = id
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = datetime.datetime.now().isoformat()
        self.is_read = False

    def __str__(self):
        return f"[{'READ' if self.is_read else 'UNREAD'}] {self.message}"


class EduPlatform:
    def __init__(self):
        self.users = []
        self.assignments = []
        self.next_user_id = 1
        self.next_assignment_id = 1

    def add_user(self, user):
        user.id = self.next_user_id
        self.next_user_id += 1
        self.users.append(user)
        return user

    def add_assignment(self, assignment):
        assignment.id = self.next_assignment_id
        self.next_assignment_id += 1
        self.assignments.append(assignment)
        return assignment

    def find_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def find_assignment(self, assignment_id):
        for assignment in self.assignments:
            if assignment.id == assignment_id:
                return assignment
        return None

    def export_to_csv(self):
        with open(".venv/users.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Email", "Role", "Grade (if student)"])
            for user in self.users:
                grade = user.grade if isinstance(user, Student) else ""
                writer.writerow([user.id, user.full_name, user.email, user.role, grade])

        with open(".venv/assignments.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Subject", "Teacher ID", "Deadline"])
            for assignment in self.assignments:
                writer.writerow([
                    assignment.id,
                    assignment.title,
                    assignment.subject,
                    assignment.teacher_id,
                    assignment.deadline
                ])

        with open(".venv/grades.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Student ID", "Student Name", "Subject", "Grade", "Teacher ID"])
            for user in self.users:
                if isinstance(user, Student):
                    for grade in user.grades:
                        writer.writerow([
                            user.id,
                            user.full_name,
                            grade.subject,
                            grade.value,
                            grade.teacher_id
                        ])

        print("Exported successfully!")

def login(platform):
    print("\n=== LOGIN ===")
    email = input("Email: ")
    password = input("Password: ")

    for user in platform.users:
        if user.email == email and user.password == password:
            return user

    print("Invalid credentials!")
    return None


def display_menu(title, options):
    print(f"\n=== {title} ===")
    for key, value in options.items():
        print(f"{key}. {value}")
    return input("Select option: ")


def main():
    platform = EduPlatform()

    admin = Admin(None, "System Admin", "admin", "123")
    platform.add_user(admin)

    while True:
        print("\n=== EDU PLATFORM ===")
        print("1. Login")
        print("2. Exit")
        choice = input("Select option: ")

        if choice == "2":
            print("Goodbye!")
            break

        if choice == "1":
            user = login(platform)
            if not user:
                continue

            while True:
                options = user.get_menu_options()
                choice = display_menu(f"{user.role} MENU", options)

                if choice == "0":
                    break

                elif choice == "1":
                    print("\nYour Profile:")
                    for key, value in user.get_profile().items():
                        print(f"{key}: {value}")

                elif isinstance(user, Student) and choice == "2":
                    assignment_id = input("Assignment ID: ")
                    content = input("Content: ")
                    if user.submit_assignment(assignment_id, content):
                        print("Assignment submitted!")
                    else:
                        print("Failed to submit assignment!")

                elif isinstance(user, Student) and choice == "3":
                    print("\nYour Grades:")
                    for grade in user.grades:
                        print(f"- {grade}")

                elif isinstance(user, Teacher) and choice == "2":
                    print("\nCreate Assignment:")
                    title = input("Title: ")
                    description = input("Description: ")
                    deadline = input("Deadline (YYYY-MM-DD): ")
                    subject = input("Subject: ")
                    class_id = input("Class ID: ")
                    assignment = user.create_assignment(title, description, deadline, subject, class_id)
                    platform.add_assignment(assignment)
                    print(f"Assignment created with ID: {assignment.id}")

                elif isinstance(user, Teacher) and choice == "3":
                    student_id = input("Student ID: ")
                    student = platform.find_user(int(student_id))
                    if not student or not isinstance(student, Student):
                        print("Invalid student ID!")
                        continue

                    assignment_id = input("Assignment ID: ")
                    grade_value = input("Grade (1-5): ")
                    user.grade_assignment(student, assignment_id, int(grade_value))
                    print("Grade submitted!")


                elif isinstance(user, Parent) and choice == "2":
                    if not user.children:
                        print("No children linked to your account!")
                        continue

                    print("\nSelect Child:")
                    for i, child in enumerate(user.children, 1):
                        print(f"{i}. {child.full_name} (ID: {child.id})")

                    child_choice = input("Select child: ")
                    try:
                        child = user.children[int(child_choice) - 1]
                        print(f"\nGrades for {child.full_name}:")
                        for grade in child.grades:
                            print(f"- {grade}")
                    except:
                        print("Invalid selection!")

                elif isinstance(user, Admin) and choice == "2":
                    print("\nAdd New User:")
                    user_type = input("Type (Student/Teacher/Parent/Admin): ").capitalize()
                    name = input("Full name: ")
                    email = input("Email: ")
                    password = input("Password: ")

                    user_data = {
                        'name': name,
                        'email': email,
                        'password': password
                    }

                    if user_type == "Student":
                        grade = input("Grade: ")
                        user_data['grade'] = grade

                    new_user = user.add_user(platform, user_type, user_data)
                    if new_user:
                        print(f"{user_type} created with ID: {new_user.id}")
                    else:
                        print("Failed to create user!")

                elif isinstance(user, Admin) and choice == "3":
                    user_id = input("User ID to remove: ")
                    if user.remove_user(platform, int(user_id)):
                        print("User removed!")
                    else:
                        print("Failed to remove user!")

                elif isinstance(user, Admin) and choice == "4":
                    print("\nAll Users:")
                    for u in platform.users:
                        print(f"ID: {u.id}, Name: {u.full_name}, Role: {u.role}, Email: {u.email}")

                elif isinstance(user, Admin) and choice == "5":
                    print("\nSystem Report:")
                    print(f"Total Users: {len(platform.users)}")
                    print(f"Students: {len([u for u in platform.users if isinstance(u, Student)])}")
                    print(f"Teachers: {len([u for u in platform.users if isinstance(u, Teacher)])}")
                    print(f"Assignments: {len(platform.assignments)}")

                elif isinstance(user, Admin) and choice == "6":
                    platform.export_to_csv()
                    print("Exported to CSV!")
                else:
                    print("Invalid option!")


if __name__ == "__main__":
    main()