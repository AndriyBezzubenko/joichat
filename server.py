from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os, sqlite3, uuid

app = Flask(__name__)
app.secret_key = 'super-secret-key'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 🛠️ Создание таблиц
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT, email TEXT UNIQUE,
                    password TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    image TEXT, text TEXT)''')
    db.commit()

@app.route('/')
def index():
    db = get_db()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['POST'])
def register():
    db = get_db()
    data = request.form
    hashed = generate_password_hash(data['password'])
    try:
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (data['name'], data['email'], hashed))
        db.commit()
        return redirect('/')
    except:
        return "Email уже зарегистрирован", 400

@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    data = request.form
    user = db.execute("SELECT * FROM users WHERE email=?", (data['email'],)).fetchone()
    if user and check_password_hash(user['password'], data['password']):
        session['user_id'] = user['id']
        return redirect('/')
    return "Неверный логин/пароль", 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return "Вы не авторизованы", 403
    file = request.files['photo']
    text = request.form.get('text', '')
    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db = get_db()
        db.execute("INSERT INTO posts (user_id, image, text) VALUES (?, ?, ?)",
                   (session['user_id'], filename, text))
        db.commit()
        return redirect('/')
    return "Неправильный формат файла", 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT, email TEXT UNIQUE,
                    password TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    image TEXT, text TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    user_id INTEGER,
                    text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')  # Add timestamp
    db.commit()

    from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# ... (Your existing code)

@app.route('/register', methods=['POST'])
def register():
    db = get_db()
    data = request.form
    if data['password'] != data['confirm_password']:
        flash('Пароли не совпадают', 'danger')
        return redirect('/')  # Redirect back to index or registration page
    hashed = generate_password_hash(data['password'])
    try:
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (data['username'], data['email'], hashed))
        db.commit()
        flash('Регистрация успешна! Войдите.', 'success')
        return redirect('/')
    except sqlite3.IntegrityError:
        flash('Email уже зарегистрирован', 'danger')
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    data = request.form
    user = db.execute("SELECT * FROM users WHERE email=?", (data['email'],)).fetchone()
    if user and check_password_hash(user['password'], data['password']):
        session['user_id'] = user['id']
        session['username'] = user['username']  # Store username in session
        flash('Вы успешно вошли!', 'success')
        return redirect('/')
    else:
        flash('Неверный логин/пароль', 'danger')
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('Вы вышли из системы.', 'info')
    return redirect('/')

# ... (Adjust your index route to pass username)
@app.route('/')
def index():
    db = get_db()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    comments = db.execute("SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id").fetchall()
    return render_template('index.html', posts=posts, comments=comments, username=session.get('username'))

def is_inappropriate(text):
    #  Replace with a more robust filtering mechanism (e.g., a profanity filter library)
    inappropriate_words = ['badword1', 'badword2']
    for word in inappropriate_words:
        if word in text.lower():
            return True
    return False

@app.route('/upload', methods=['POST'])
def upload():
    # ... (Your upload code)
    if is_inappropriate(text):
        flash('Ваш текст содержит неприемлемые выражения.', 'warning')
        return redirect('/')
    # ... (Save the post)

    POSTS_PER_PAGE = 10

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    db = get_db()
    offset = (page - 1) * POSTS_PER_PAGE
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?",
                       (POSTS_PER_PAGE, offset)).fetchall()
    total_posts = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    last_page = (total_posts + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    comments = db.execute("SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id").fetchall()
    return render_template('index.html', posts=posts, comments=comments, username=session.get('username'), page=page, last_page=last_page)