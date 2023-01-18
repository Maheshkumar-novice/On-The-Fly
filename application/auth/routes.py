from flask import Blueprint

from application.auth.controller import *

auth_blueprint = Blueprint('auth', __name__, template_folder='templates/')


auth_blueprint.add_url_rule(rule='/businesses/signup',
                            view_func=get_business_signup_page,
                            endpoint='get_business_signup_page',
                            methods=['GET'])
