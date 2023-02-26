from flask_login import login_required, current_user
from flask import render_template
from application.business.models import BusinessInformation


@login_required
def home():
    business_information = BusinessInformation.query.filter_by(user_id=current_user.id).scalar()
    data = {**current_user.to_dict(), **business_information.to_dict()}
    return render_template('business_home.html', navbar_type='user', user_type='business', business_data=data), {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@login_required
def edit():
    return 'profile'
