import sqlite3

conn = sqlite3.connect("assignments.db")
cursor = conn.cursor()

user_id = input("Enter user ID: ")
title = input("Assignment Title: ")
description = input("Description: ")
due_date = input("Due Date (YYYY-MM-DD): ")

cursor.execute("""
    INSERT INTO assignments (user_id, title, description, due_date)
    VALUES (?, ?, ?, ?)
""", (user_id, title, description, due_date))

conn.commit()
print("✅ Assignment added!")
conn.close()
