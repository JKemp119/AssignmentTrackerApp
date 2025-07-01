from functools import wraps
from flask import Flask, render_template, request, redirect, session, url_for, flash, get_flashed_messages

# Add this decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # required for session login tracking


# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('assignments.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Route to add a user
@app.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    ...
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password)
            )
            conn.commit()
            conn.close()
            flash(f"✅ User '{username}' added successfully!", "success")
            return redirect('/')
        except Exception as e:
            return f"❌ Error adding user: {e}"

    return render_template('add_user.html')
# View all users
@app.route('/users')
@login_required
def view_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, email FROM users').fetchall()
    conn.close()
    return render_template('view_users.html', users=users)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/users')

# Add Assignment
@app.route('/assignments/add', methods=['GET', 'POST'])
@login_required
def add_assignment():
    ...
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()

    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        conn.execute(
            'INSERT INTO assignments (user_id, title, description, due_date) VALUES (?, ?, ?, ?)',
            (user_id, title, description, due_date)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    
    conn.close()
    return render_template('add_assignment.html', users=users)
# View all assignments
@app.route('/assignments')
@login_required
def view_assignments():
    ...
    conn = get_db_connection()
    assignments = conn.execute("""
        SELECT a.id, a.title, a.description, a.due_date, a.status, u.username
        FROM assignments a
        JOIN users u ON a.user_id = u.id
    """).fetchall()
    conn.close()
    return render_template('view_assignments.html', assignments=assignments)
#login and logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password_hash = ?', (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"✅ Welcome back, {user['username']}!", "success")
            return redirect('/')
        else:
            return "❌ Invalid email or password"

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/assignments/complete/<int:assignment_id>', methods=['POST'])
@login_required
def mark_assignment_complete(assignment_id):
    conn = get_db_connection()
    conn.execute('UPDATE assignments SET status = "completed" WHERE id = ?', (assignment_id,))
    conn.commit()
    conn.close()
    flash("✅ Assignment marked complete!", "success")
    return redirect('/assignments')
# Run the Flask app
if __name__ == '__main__':
    print("✅ Flask app is running at http://127.0.0.1:5000")
    app.run(debug=True)

