from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from forms import AdminForm
from models import db, User, Article
import os
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import dotenv

dotenv.load_dotenv()

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db.init_app(app)
Bootstrap5(app)
limiter = Limiter(
    get_remote_address,
    app=app,
)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.isAdmin:
            return f(*args, **kwargs) 
        else:
            return abort(403)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)

@app.route('/course')
def course():
    return render_template('course.html', current_user=current_user)

@app.route('/register', methods=["GET", "POST"])
@limiter.limit("2 per second") 
def register():
    if request.method == "POST":
        if request.form.get('password') != request.form.get('second-password'):
            flash("Your passwords doesn't match")

            return redirect(url_for('register'))
        
        user = db.session.execute(db.select(User).where(User.login == request.form.get('login'))).scalar()
        if user:
            flash("This email already exist, please try another.")

            return redirect(url_for('register'))
        
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
            )
        
        new_user = User(  
            name=request.form.get('name'),
            surname=request.form.get('surname'),
            login=request.form.get('login'),
            password=hash_and_salted_password,
            email=request.form.get('email'),
            telegramId=-1,
            registeredAt=datetime.utcnow().timestamp()
        )
        if request.form.get('password') == ADMIN_PASSWORD:
            new_user.isAdmin = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        
        return redirect(url_for("home"))

    return render_template("register.html", current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
@limiter.limit("2 per second") 
def login():
    if request.method == "POST":
        password = request.form.get('password')
        user = db.session.execute(db.select(User).where(User.login == request.form.get('login'))).scalar()
        if not user:
            flash("That login doesn't exist, please try again.")

            return redirect(url_for("login"))

        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")

            return redirect(url_for("login"))
        else:
            login_user(user)

            return redirect(url_for('home'))
    
    return render_template("login.html", current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('home'))


@app.route('/admin', methods=["GET", "POST"])
@limiter.limit("2 per second") 
@admin_only
def admin():
    if request.method == "POST":

        new_article = Article(
            article=request.form.get('message_text'),
            publishAt=request.form.get('timezone'),
        )
        db.session.add(new_article)
        db.session.commit()

        return redirect(url_for("admin"))
    
    now = datetime.now().date()
    publish_history = db.session.execute(db.select(Article).where(Article.publishAt >= now)).scalars().all()
    users = db.session.execute(db.select(User)).scalars().all()

    return render_template("admin.html", publish_history=publish_history, users=users ,current_user=current_user)

@app.route("/delete/<int:article_id>")
@limiter.limit("2 per second") 
@admin_only
def delete_article(article_id):
    article_to_delete = db.session.execute(db.select(Article).where(Article.id == article_id)).scalar()
    db.session.delete(article_to_delete)
    db.session.commit()

    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(port=5000)
