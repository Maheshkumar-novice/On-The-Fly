from datetime import datetime

from flask import current_app


def is_eligible_for_retry(stored_time):
    time_limit = current_app.config['TIME_LIMIT_NEEDED_FOR_RESEND']
    if (not stored_time) or (_get_time_passed_since(stored_time) > time_limit):
        return True
    return False


def get_remaining_time_to_reach_eligibility(stored_time):
    time_limit = current_app.config['TIME_LIMIT_NEEDED_FOR_RESEND']
    if not stored_time:
        return 0

    time_passed = _get_time_passed_since(stored_time)
    remaining_time = time_limit - time_passed

    if remaining_time < 0:
        return 0

    return remaining_time


def _get_time_passed_since(timestamp):
    return (datetime.now() - timestamp).total_seconds()
