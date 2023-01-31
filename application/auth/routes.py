from flask import Blueprint

from application.auth.controller import *

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/')


auth_blueprint.add_url_rule(rule='/businesses/signup',
                            view_func=get_business_signup_page,
                            endpoint='get_business_signup_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/businesses/signup',
                            view_func=create_business_user,
                            endpoint='create_business_user',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/customers/signup',
                            view_func=get_customer_signup_page,
                            endpoint='get_customer_signup_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/customers/signup',
                            view_func=create_customer_user,
                            endpoint='create_customer_user',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/businesses/login',
                            view_func=get_business_login_page,
                            endpoint='get_business_login_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/businesses/login',
                            view_func=login_business_user,
                            endpoint='login_business_user',
                            methods=['POST'])


auth_blueprint.add_url_rule(rule='/customers/login',
                            view_func=get_customer_login_page,
                            endpoint='get_customer_login_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/customers/login',
                            view_func=login_customer_user,
                            endpoint='login_customer_user',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/logout',
                            view_func=logout,
                            endpoint='logout',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/security_measures',
                            view_func=get_security_measures_page,
                            endpoint='get_security_measures_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/email_verification',
                            view_func=get_email_verification_page,
                            endpoint='get_email_verification_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/generate_email_verification_code',
                            view_func=generate_email_verification_code,
                            endpoint='generate_email_verification_code',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/get_verification_code_page',
                            view_func=get_verification_code_page,
                            endpoint='get_verification_code_page',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/verify_email',
                            view_func=verify_email_verification_code,
                            endpoint='verify_email_verification_code',
                            methods=['POST'])
