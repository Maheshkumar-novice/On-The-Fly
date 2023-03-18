from flask import Blueprint

from application.customer.controller import *

customer_blueprint = Blueprint(
    'customer', __name__, template_folder='templates/')


customer_blueprint.add_url_rule(rule='/home',
                                view_func=home,
                                endpoint='home',
                                methods=['GET'])

customer_blueprint.add_url_rule(rule='/feed',
                                view_func=feed,
                                endpoint='feed',
                                methods=['GET', 'POST'])
