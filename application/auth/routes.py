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
