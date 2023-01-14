from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

from config import APP_SETTINGS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(APP_SETTINGS)

    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html', title='On The Fly')

    return app
