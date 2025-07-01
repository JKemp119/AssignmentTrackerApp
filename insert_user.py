import sqlite3

conn = sqlite3.connect("assignments.db")
cursor = conn.cursor()

username = input("Enter username: ")
email = input("Enter email: ")
password = input("Enter password: ")  # (not hashed here)

try:
    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    """, (username, email, password))
    conn.commit()
    print("✅ User added!")
except sqlite3.IntegrityError as e:
    print("❌ Error:", e)

conn.close()
