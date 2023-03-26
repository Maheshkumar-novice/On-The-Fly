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
                                methods=['GET', 'POST'])

business_buleprint.add_url_rule(rule='/create_item',
                                view_func=create_business_item,
                                endpoint='create_business_item',
                                methods=['GET', 'POST'])

business_buleprint.add_url_rule(rule='/edit_item',
                                view_func=edit_business_item,
                                endpoint='edit_business_item',
                                methods=['GET', 'POST'])

business_buleprint.add_url_rule(rule='/delete_item',
                                view_func=delete_business_item,
                                endpoint='delete_business_item',
                                methods=['DELETE'])

business_buleprint.add_url_rule(rule='/view/<int:id>',  # business id
                                view_func=view,
                                endpoint='view',
                                methods=['GET'])

business_buleprint.add_url_rule(rule='/items_view/<int:id>',  # business id
                                view_func=business_items_view,
                                endpoint='business_items_view',
                                methods=['GET', 'POST'])

business_buleprint.add_url_rule(rule='/ticket/<int:business_id>',
                                view_func=ticket,
                                endpoint='ticket',
                                methods=['GET', 'POST'])


business_buleprint.add_url_rule(rule='/items/<int:business_id>',
                                view_func=items_by_business_id,
                                endpoint='items_by_business_id',
                                methods=['GET'])


business_buleprint.add_url_rule(rule='/ticket',
                                view_func=create_ticket,
                                endpoint='create_ticket',
                                methods=['POST'])

# https://stackoverflow.com/questions/30967822/when-do-i-use-path-params-vs-query-params-in-a-restful-api


business_buleprint.add_url_rule(rule='/tickets',
                                view_func=tickets,
                                endpoint='tickets',
                                methods=['GET'])

business_buleprint.add_url_rule(rule='/tickets/<int:id>',
                                view_func=ticket_by_id,
                                endpoint='ticket_by_id',
                                methods=['GET'])

business_buleprint.add_url_rule(rule='/tickets/<int:id>/comment',
                                view_func=add_ticket_comment,
                                endpoint='add_ticket_comment',
                                methods=['POST'])

business_buleprint.add_url_rule(rule='/tickets/<int:id>/status',
                                view_func=update_ticket_status,
                                endpoint='update_ticket_status',
                                methods=['PUT'])