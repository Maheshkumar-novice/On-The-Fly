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

auth_blueprint.add_url_rule(rule='/logout',
                            view_func=logout,
                            endpoint='logout',
                            methods=['GET'])
# auth_blueprint.add_url_rule(rule='/email_verification',
#                             view_func=generate_email_verification_code,
#                             endpoint='generate_email_verification_code',
#                             methods=['POST'])

# auth_blueprint.add_url_rule(rule='/email_verification_code',
#                             view_func=get_verification_code_page,
#                             endpoint='get_verification_code_page',
#                             methods=['GET'])

# auth_blueprint.add_url_rule(rule='/email_verification_code',
#                             view_func=verify_email_verification_code,
#                             endpoint='verify_email_verification_code',
#                             methods=['POST'])
