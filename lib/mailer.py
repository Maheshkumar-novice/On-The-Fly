from flask import session
from application import mail_client
from config import Config


# https://www.twilio.com/blog/verify-email-address-python-flask-twilio-verify
def send_verification(to_email):
    verification = mail_client.verify \
        .services(Config.TWILIO_VERIFY_SERVICE) \
        .verifications \
        .create(to=to_email, channel='email')
    return verification.sid


def check_verification_token(token):
    to_email = session['to_email']
    check = mail_client.verify \
        .services(Config.TWILIO_VERIFY_SERVICE) \
        .verification_checks \
        .create(to=to_email, code=token)
    return check.status == 'approved'
