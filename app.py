from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key

DATABASE = 'teachers.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT NOT NULL,
        subject TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM teachers")
    teachers = c.fetchall()
    conn.close()
    return render_template('index.html', teachers=teachers)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        session['logged_in'] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    if 'logged_in' in session:
        name = request.form['name']
        designation = request.form['designation']
        subject = request.form['subject']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO teachers (name, designation, subject) VALUES (?, ?, ?)",
                  (name, designation, subject))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
