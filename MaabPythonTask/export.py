import csv
import sqlite3
from openpyxl import Workbook
from datetime import datetime


def export_to_csv(users, filename="users_export.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Full Name", "Email", "Role", "Created At"])
        for user in users:
            profile = user.get_profile()
            writer.writerow([
                profile["id"],
                profile["name"],
                profile["email"],
                profile["role"],
                profile["created_at"]
            ])
    print(f"[CSV] Exported {len(users)} users to {filename}")


def export_to_excel(users, filename="users_export.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    ws.append(["ID", "Full Name", "Email", "Role", "Created At"])
    for user in users:
        profile = user.get_profile()
        ws.append([
            profile["id"],
            profile["name"],
            profile["email"],
            profile["role"],
            profile["created_at"]
        ])
    wb.save(filename)
    print(f"[Excel] Exported {len(users)} users to {filename}")


def export_to_sql(users, filename="users_export.sql"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, email TEXT, role TEXT, created_at TEXT);\n")
        for user in users:
            profile = user.get_profile()
            file.write(
                f"INSERT INTO users (id, name, email, role, created_at) VALUES "
                f"({profile['id']}, '{profile['name']}', '{profile['email']}', '{profile['role']}', '{profile['created_at']}');\n"
            )
    print(f"[SQL] Exported {len(users)} users to {filename}")
