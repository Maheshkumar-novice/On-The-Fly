from flask import Blueprint

from application.auth.controller import *

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/')


auth_blueprint.add_url_rule(rule='/signup',
                            view_func=signup,
                            endpoint='signup',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/login',
                            view_func=login,
                            endpoint='login',
                            methods=['GET', 'POST'])


auth_blueprint.add_url_rule(rule='/security_measures',
                            view_func=security_measures,
                            endpoint='security_measures',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/email_verification',
                            view_func=email_verification,
                            endpoint='email_verification',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/mobile_verification',
                            view_func=mobile_verification,
                            endpoint='mobile_verification',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/totp_setup',
                            view_func=totp_setup,
                            endpoint='totp_setup',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/totp_qrcode',
                            view_func=totp_qrcode,
                            endpoint='totp_qrcode',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/totp_verification',
                            view_func=totp_verification,
                            endpoint='totp_verification',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/forgot_password',
                            view_func=forgot_password,
                            endpoint='forgot_password',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/password_reset/<token>',
                            view_func=password_reset,
                            endpoint='password_reset',
                            methods=['GET', 'POST'])

auth_blueprint.add_url_rule(rule='/logout',
                            view_func=logout,
                            endpoint='logout',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/user_home',
                            view_func=user_home,
                            endpoint='user_home',
                            methods=['GET'])