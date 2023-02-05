import pyotp
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

from config import Config


def send_verification_mail(email, verification_code):
    message = _get_sendgrid_message(email)
    message.dynamic_template_data = {
        'twilio_message': f'On The Fly verification code is {verification_code}'
    }
    message.template_id = Config.SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID

    _send_sendgrid_mail(message)


def send_password_reset_mail(email, url):
    message = _get_sendgrid_message(email)
    message.dynamic_template_data = {
        'password_reset_link': url
    }
    message.template_id = Config.SENDGRID_PASSWORD_RESET_TEMPLATE_ID
    _send_sendgrid_mail(message)


def send_mobile_no_verification(mobile_no):
    _get_twilio_client_verify_service().verifications.create(to=mobile_no, channel='sms')


def check_mobile_no_verification_code(mobilie_no, code):
    return _get_twilio_client_verify_service().verification_checks.create(to=mobilie_no, code=code).status == 'approved'


def get_totp_uri(email, totp_secret):
    return pyotp.totp.TOTP(totp_secret).provisioning_uri(
        issuer_name='On The Fly', name=email)


def check_totp(totp_secret, totp):
    return pyotp.TOTP(totp_secret).now() == totp


def _get_sendgrid_message(email):
    return Mail(
        from_email=Config.SENDGRID_SENDER_EMAIL,
        to_emails=email
    )


def _send_sendgrid_mail(message):
    SendGridAPIClient(Config.SENDGRID_API_KEY).send(message)


def _get_twilio_client_verify_service():
    return Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN).verify.services(Config.TWILIO_VERIFY_SERVICE)
