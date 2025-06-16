from models.user_base import User, Role


class Admin(User):
    def __init__(self, _id, full_name, email, password, permissions=None):
        super().__init__(_id, full_name, email, password, Role.ADMIN)
        self.permissions = permissions if permissions else []

    def add_user(self, user_list, user_object):
        user_list.append(user_object)
        return f"User {user_object._full_name} added."

    def remove_user(self, user_list, user_id):
        for user in user_list:
            if user._id == user_id:
                user_list.remove(user)
                return f"User with ID {user_id} removed."
        return "User not found."

    def generate_report(self, user_list):
        report = []
        for user in user_list:
            profile = user.get_profile()
            report.append({
                "id": profile["id"],
                "name": profile["name"],
                "email": profile["email"],
                "role": profile["role"],
                "created_at": profile["created_at"]
            })
        return report
