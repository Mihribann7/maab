from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.parent import Parent
from models.assignment import Assignment
from models.grade import Grade
from models.schedule import Schedule
from models.notification import Notification
from export import *

from datetime import datetime

users = []
assignments = []
grades = []
schedules = []
notifications = []

student = Student(1, "Sara Karimova", "sara@example.com", "stud123", "9-A", {"Math": 2})
teacher = Teacher(2, "Mr. Ali", "ali@example.com", "teach123", ["Math"], ["9-A"])
parent = Parent(3, "Saras Mom", "mom@example.com", "mom123", [1])
admin = Admin(4, "Admin", "admin@example.com", "admin123", ["add_user", "remove_user"])

users.extend([student, teacher, parent, admin])


def print_main_menu():
    print("\n---MAIN MENU---\n")
    print("1. Student")
    print("2. Teacher")
    print("3. Parent")
    print("4. Admin")
    print("5. Assignment")
    print("6. Grade")
    print("7. Schedule")
    print("8. Notification")
    print("9. Export")
    print("10. Exit")

def student_menu():
    while True:
        print("\n--- Student Menu ---")
        print("1. Submit Assignment")
        print("2. View Grades")
        print("3. Calculate Average")
        print("4. View Notifications")
        print("5. Back")
        choice = input("Select: ")

        if choice == "1":
            aid = int(input("Assignment ID: "))
            content = input("Your content: ")
            for a in assignments:
                if a.id == aid:
                    print("Assignment submitted successfully!")
                    print(a.add_submission(student._id, content))
        elif choice == "2":
            print("Grades:", student.view_grades())
        elif choice == "3":
            print("Average Grade:", student.calculate_average_grade())
        elif choice == "4":
            print("Notifications:", student.view_notifications())
        elif choice == "5":
            break
        else:
            print("Invalid.")

def teacher_menu():
    while True:
        print("\n--- Teacher Menu ---")
        print("1. Create Assignment")
        print("2. Grade Assignment")
        print("3. View Student Progress")
        print("4. Back")
        choice = input("Select: ")

        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            subject = input("Subject: ")
            class_id = input("Class ID: ")
            aid = len(assignments) + 1
            a = Assignment(aid, title, desc, f"{deadline}T23:59:59", subject, teacher._id, class_id)
            assignments.append(a)
            teacher.assignments[aid] = a
            print("Assignment created!")
        elif choice == "2":
            aid = int(input("Assignment ID: "))
            sid = int(input("Student ID: "))
            g = int(input("Grade (1-5): "))
            for a in assignments:
                if a.id == aid:
                    print(a.set_grade(sid, g))
                    student.grades.setdefault(a.subject, []).append(g)
        elif choice == "3":
            print(teacher.view_student_progress(student))
        elif choice == "4":
            break
        else:
            print("Invalid.")

def parent_menu():
    while True:
        print("\n--- Parent Menu ---")
        print("1. View Child Grades")
        print("2. View Child Assignments")
        print("3. View Notifications")
        print("4. Back")
        choice = input("Select: ")

        if choice == "1":
            print(parent.view_child_grades(student))
        elif choice == "2":
            print(parent.view_child_assignments(student))
        elif choice == "3":
            print(parent.receive_child_notification(student))
        elif choice == "4":
            break
        else:
            print("Invalid.")

def admin_menu():
    global users

    while True:
        print("\n--- Admin Menu ---")
        print("1. Add User")
        print("2. Remove User")
        print("3. Generate Report")
        print("4. Back")
        choice = input("Select: ")

        if choice == "1":
            print("\nWho do you want to add?")
            print("1. Student")
            print("2. Teacher")
            print("3. Parent")
            print("4. Admin")
            role_choice = input("Enter option: ")

            _id = max([u._id for u in users], default=0) + 1
            name = input("Full Name: ")
            email = input("Email: ")
            password = input("Password: ")

            if role_choice == "1":
                grade = input("Grade (e.g. 9-A): ")
                new_user = Student(_id, name, email, password, grade)
            elif role_choice == "2":
                new_user = Teacher(_id, name, email, password)
            elif role_choice == "3":
                new_user = Parent(_id, name, email, password)
            elif role_choice == "4":
                new_user = Admin(_id, name, email, password)
            else:
                print("Invalid role choice.")
                continue

            users.append(new_user)
            print(f"{new_user.role.value} '{name}' added successfully with ID {_id}.")

        elif choice == "2":
            uid = int(input("User ID to remove: "))
            print(admin.remove_user(users, uid))

        elif choice == "3":
            report = admin.generate_report(users)
            for entry in report:
                print(entry)

        elif choice == "4":
            break
        else:
            print("Invalid.")



def assignment_menu():
    while True:
        print("\n--- Assignment Menu ---")
        print("1. View All Assignments")
        print("2. View Assignment Status")
        print("3. Back")
        choice = input("Select: ")

        if choice == "1":
            for a in assignments:
                print(vars(a))
        elif choice == "2":
            aid = int(input("Assignment ID: "))
            for a in assignments:
                if a.id == aid:
                    print(a.get_status())
        elif choice == "3":
            break
        else:
            print("Invalid.")

def grade_menu():
    while True:
        print("\n--- Grade Menu ---")
        print("1. View Student Grades")
        print("2. Back")
        choice = input("Select: ")

        if choice == "1":
            print("Student Grades:", student.view_grades())
        elif choice == "2":
            break
        else:
            print("Invalid.")

def schedule_menu():
    while True:
        print("\n--- Schedule Menu ---")
        print("1. Create/View Schedule")
        print("2. Back")
        choice = input("Select: ")

        if choice == "1":
            sched = Schedule(1, "9-A", "Monday")
            sched.add_lesson("08:00", "Math", teacher._id)
            schedules.append(sched)
            print(sched.view_schedule())
        elif choice == "2":
            break
        else:
            print("Invalid.")

def notification_menu():
    while True:
        print("\n--- Notification Menu ---")
        print("1. Send to Student")
        print("2. View Student Notifications")
        print("3. Back")
        choice = input("Select: ")

        if choice == "1":
            msg = input("Message: ")
            notif_id = len(notifications) + 1
            notif = Notification(notif_id, msg, student._id)
            student.add_notification(notif.send()["message"])
            notifications.append(notif)
            print("Notification sent.")
        elif choice == "2":
            print(student.view_notifications())
        elif choice == "3":
            break
        else:
            print("Invalid.")


def export_menu():
    while True:
        print("\n--- Export Menu ---")
        print("1. Export Users to CSV")
        print("2. Export Users to Excel")
        print("3. Export Users to SQL")
        print("4. Back")
        choice = input("Select: ")

        if choice == "1":
            export_to_csv(users)
        elif choice == "2":
            export_to_excel(users)
        elif choice == "3":
            export_to_sql(users)
        elif choice == "4":
            break
        else:
            print("Invalid.")

while True:
    print("\nPlease, select one of the followings:")
    print_main_menu()
    main_choice = input()

    if main_choice == "1":
        student_menu()
    elif main_choice == "2":
        teacher_menu()
    elif main_choice == "3":
        parent_menu()
    elif main_choice == "4":
        admin_menu()
    elif main_choice == "5":
        assignment_menu()
    elif main_choice == "6":
        grade_menu()
    elif main_choice == "7":
        schedule_menu()
    elif main_choice == "8":
        notification_menu()
    elif main_choice == "9":
        export_menu()
    elif main_choice == "10":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
