from flask import Blueprint

from application.business.controller import *

business_buleprint = Blueprint(
    'business', __name__, template_folder='templates/')


business_buleprint.add_url_rule(rule='/home',
                                view_func=home,
                                endpoint='home',
                                methods=['GET'])

business_buleprint.add_url_rule(rule='/edit',
                                view_func=edit,
                                endpoint='edit',
                                methods=['GET'])
