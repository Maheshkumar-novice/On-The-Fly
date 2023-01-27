from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import APP_SETTINGS

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(APP_SETTINGS)

    db.init_app(app)
    login_manager.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html', navbar_type='home')

    from application.auth.routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from application.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    return app
