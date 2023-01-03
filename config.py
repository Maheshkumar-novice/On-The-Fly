import os

from dotenv import load_dotenv

load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))

APP_SETTINGS = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')


class Config():
    EMAIL_CONFIRMATION_SENDER_EMAIL = os.getenv(
        'EMAIL_CONFIRMATION_SENDER_EMAIL')
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    JSON_SORT_KEYS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DB_URL')
