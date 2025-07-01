import sqlite3

conn = sqlite3.connect("assignments.db")
cursor = conn.cursor()

cursor.execute("SELECT id, username, email FROM users")
users = cursor.fetchall()

print("\n📋 Registered Users:")
for u in users:
    print(f"ID: {u[0]}, Username: {u[1]}, Email: {u[2]}")

conn.close()
