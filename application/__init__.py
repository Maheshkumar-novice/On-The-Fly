from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

from config import APP_SETTINGS

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'home'


def create_app():
    app = Flask(__name__)
    app.config.from_object(APP_SETTINGS)

    db.init_app(app)
    login_manager.init_app(app)

    @app.route('/')
    def home():
        if not current_user.is_anonymous:
            return redirect(url_for('auth.user_home'))

        return render_template('home.html', navbar_type='home')

    from application.auth.routes import auth_blueprint
    from application.business.routes import business_buleprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(business_buleprint, url_prefix='/business')

    from application.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    return app
