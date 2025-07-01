import sqlite3

conn = sqlite3.connect("assignments.db")
cursor = conn.cursor()

cursor.execute("""
SELECT a.id, u.username, a.title, a.due_date, a.status
FROM assignments a
JOIN users u ON a.user_id = u.id
""")

assignments = cursor.fetchall()

print("\n📚 Assignments:")
for a in assignments:
    print(f"ID: {a[0]} | User: {a[1]} | Title: {a[2]} | Due: {a[3]} | Status: {a[4]}")

conn.close()
