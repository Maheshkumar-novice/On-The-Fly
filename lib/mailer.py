from flask import session

from application import mail_client
from config import Config


# https://www.twilio.com/blog/verify-email-address-python-flask-twilio-verify
# https://www.twilio.com/docs/verify/email
def send_verification(to, type='email'):
    verification = mail_client.verify \
        .services(Config.TWILIO_VERIFY_SERVICE) \
        .verifications \
        .create(to=to, channel=type)
    return verification.sid


def check_verification_token(to, token):
    check = mail_client.verify \
        .services(Config.TWILIO_VERIFY_SERVICE) \
        .verification_checks \
        .create(to=to, code=token)
    return check.status == 'approved'
