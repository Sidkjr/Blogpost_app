from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    blogapp = Flask(__name__)
    blogapp.config['SECRET_KEY'] = "saltkey"
    blogapp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(blogapp)

    from .views import views
    from .auth import auth

    blogapp.register_blueprint(views, url_prefix="/")
    blogapp.register_blueprint(auth, url_prefix="/")

    from .models import User, Post
    create_database(blogapp)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(blogapp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return blogapp

def create_database(blogapp):
    if not path.exists("website/" + DB_NAME):
        with blogapp.app_context():
            db.create_all()
        print("Created Database!")