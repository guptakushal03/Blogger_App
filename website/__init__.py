from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "GuniBloggingApp"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Python311/Projects/Flask Blogger App/website/database.db'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db_path = f'sqlite:///C:/Python311/Projects/Flask Blogger App/website/database.db'
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print(f"Database created at: {db_path}")
    else:
        print(f"Database already exists at: {db_path}")
