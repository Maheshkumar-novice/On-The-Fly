import os

from dotenv import load_dotenv

load_dotenv()


APP_SETTINGS = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')


class Config():
    EMAIL_CONFIRMATION_SENDER_EMAIL = os.getenv(
        'EMAIL_CONFIRMATION_SENDER_EMAIL')
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_VERIFY_SERVICE = os.getenv('TWILIO_VERIFY_SERVICE', '')
    JWT_VALIDITY_FOR_PASSWORD_RESET_IN_SECONDS = int(os.getenv(
        'JWT_VALIDITY_FOR_PASSWORD_RESET_IN_SECONDS', 300))
    SENDGRID_SENDER_EMAIL = os.getenv('SENDGRID_SENDER_EMAIL', '')
    SENDGRID_PASSWORD_RESET_TEMPLATE_ID = os.getenv(
        'SENDGRID_PASSWORD_RESET_TEMPLATE_ID', '')
    SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID = os.getenv(
        'SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID', '')
    TIME_LIMIT_NEEDED_FOR_RESEND = int(
        os.getenv('TIME_LIMIT_NEEDED_FOR_RESEND', 60))


class DevelopmentConfig(Config):
    JSON_SORT_KEYS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DB_URL')
