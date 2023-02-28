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
                                methods=['GET', 'POST'])

business_buleprint.add_url_rule(rule='/subtypes',
                                view_func=business_subtypes,
                                endpoint='business_subtypes',
                                methods=['GET'])

business_buleprint.add_url_rule(rule='/items',
                                view_func=business_items,
                                endpoint='business_items',
                                methods=['GET'])

business_buleprint.add_url_rule(rule='/create_item',
                                view_func=create_business_item,
                                endpoint='create_business_item',
                                methods=['GET', 'POST'])
