print("Welcome to the Assignment Tracker!")
print("Run the individual scripts to insert users, add assignments, or view data.")
print("Example:\n  python insert_user.py\n  python view_assignments.py")

import sqlite3

def connect_db():
    return sqlite3.connect("assignments.db")

def insert_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """, (username, email, password))
        conn.commit()
        print("✅ User added!\n")
    except sqlite3.IntegrityError as e:
        print("❌ Error:", e)
    conn.close()

def view_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    print("\n📋 Registered Users:")
    for u in users:
        print(f"ID: {u[0]} | Username: {u[1]} | Email: {u[2]}")
    conn.close()
    print("")

def add_assignment():
    user_id = input("Enter user ID to assign to: ")
    title = input("Assignment Title: ")
    description = input("Description: ")
    due_date = input("Due Date (YYYY-MM-DD): ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO assignments (user_id, title, description, due_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, title, description, due_date))
    conn.commit()
    print("✅ Assignment added!\n")
    conn.close()

def view_assignments():
    conn = connect_db()
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
    print("")

def main_menu():
    while True:
        print("📌 Assignment Tracker Menu")
        print("1. Add User")
        print("2. View Users")
        print("3. Add Assignment")
        print("4. View Assignments")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            insert_user()
        elif choice == "2":
            view_users()
        elif choice == "3":
            add_assignment()
        elif choice == "4":
            view_assignments()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.\n")

if __name__ == "__main__":
    main_menu()


