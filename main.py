from flask import Flask, render_template, request, redirect, session
import sqlite3, os, smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "apex_global_secure"

UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DATABASE
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        image TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ROUTES
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return render_template('index.html', projects=projects)

@app.route('/projects')
def projects():
    conn = sqlite3.connect('database.db')
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/careers')
def careers():
    return render_template('careers.html')
    
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        msg['Subject'] = "ApexBuild Contact"
        msg['From'] = "your_email@gmail.com"
        msg['To'] = "your_email@gmail.com"

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)
        server.quit()

    return render_template('contact.html')

# LOGIN SYSTEM
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username']=="admin" and request.form['password']=="1234":
            session['user']="admin"
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()

    return render_template('dashboard.html', projects=projects)

@app.route('/add-project', methods=['GET','POST'])
def add_project():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        img = request.files['image']

        filename = img.filename
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO projects(title,description,image) VALUES(?,?,?)",
                     (title, desc, filename))
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_project.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    
    from flask import Flask, render_template, request, redirect, session
import sqlite3, os, smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "apex_global_secure"

UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DATABASE
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        image TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ROUTES
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return render_template('index.html', projects=projects)
    
@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/projects')
def projects():
    conn = sqlite3.connect('database.db')
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        msg['Subject'] = "ApexBuild Contact"
        msg['From'] = "your_email@gmail.com"
        msg['To'] = "your_email@gmail.com"

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)
        server.quit()

    return render_template('contact.html')

# LOGIN SYSTEM
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username']=="admin" and request.form['password']=="1234":
            session['user']="admin"
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()

    return render_template('dashboard.html', projects=projects)

@app.route('/add-project', methods=['GET','POST'])
def add_project():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        img = request.files['image']

        filename = img.filename
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO projects(title,description,image) VALUES(?,?,?)",
                     (title, desc, filename))
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_project.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    
    from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {"admin": {"password":"Password123"}}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"]==password:
            user = User(username)
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
    
@app.route('/services')
def services():
    jobs = [
        "Project Manager",
        "Civil Engineer",
        "Construction Supervisor",
        "Site Engineer",
        "Quantity Surveyor"
    ]
    return render_template('services.html', jobs=jobs)
    
if __name__ == "__main__":
    app.run()
    
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        msg = Message(
            subject=f"New Message from {name}",
            sender=email,
            recipients=["your@email.com"]
        )
        msg.body = message
        mail.send(msg)

    return render_template("contact.html")
    
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your@email.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image = db.Column(db.String(200))
    description = db.Column(db.Text)
    
import os
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from werkzeug.utils import secure_filename

@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        file = request.files["image"]

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_project = Project(
            title=title,
            image=filename,
            description=description
        )

        db.session.add(new_project)
        db.session.commit()

    projects = Project.query.all()
    return render_template("dashboard.html", projects=projects)
    
@app.route("/projects")
def projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)
    
@app.route("/admin/analytics")
@login_required
def analytics():
    return render_template("analytics.html")
    
from flask_babel import Babel

babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'