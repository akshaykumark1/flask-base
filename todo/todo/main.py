import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the database (create a tasks table)
def init_db():
    with sqlite3.connect('todo.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task TEXT NOT NULL
                        )''')

# Route to display the To-Do list
@app.route('/')
def index():
    # Fetch tasks from the database
    with sqlite3.connect('todo.db') as conn:
        conn.row_factory = sqlite3.Row
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        # Insert the new task into the database
        with sqlite3.connect('todo.db') as conn:
            conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        return redirect(url_for('index'))

# Route to remove a task
@app.route('/remove/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Initialize the database when starting the app
    init_db()
    app.run(debug=True)
