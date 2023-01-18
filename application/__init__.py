from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import APP_SETTINGS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(APP_SETTINGS)

    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html', title='On The Fly')

    from application.auth.routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
