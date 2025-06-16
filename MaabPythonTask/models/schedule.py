class Schedule:
    def __init__(self, _id, class_id, day):
        self.id = _id
        self.class_id = class_id
        self.day = day
        self.lessons = {}

    def add_lesson(self, time, subject, teacher_id):
        if time in self.lessons:
            return f"Conflict: There is already a lesson at {time}."
        self.lessons[time] = {
            "subject": subject,
            "teacher_id": teacher_id
        }
        return f"Lesson added at {time}."

    def view_schedule(self):
        return {
            "class_id": self.class_id,
            "day": self.day,
            "lessons": self.lessons
        }

    def remove_lesson(self, time):
        if time in self.lessons:
            del self.lessons[time]
            return f"Lesson at {time} removed."
        return f"No lesson scheduled at {time}."
