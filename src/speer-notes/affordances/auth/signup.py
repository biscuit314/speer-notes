"""
This module defines functions to add affordances.auth.signup.
"""
import logging
import json
from flask import make_response, request
from hypermea.core.utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url, get_api

LOG = logging.getLogger("affordances.auth.signup")


def add_affordance(app):
    @app.route("/api/auth/signup", methods=["POST"])
    def do_add_user():
        if app.auth and (not app.auth.authorized(None, "signup", "POST")):
            return make_error_response(unauthorized_message, 401)

        return _do_add_user(request.json)

def _do_add_user(user_data):
    result = get_api().post('/api/users', data=json.dumps(user_data), headers=dict(request.headers))
    if result.status_code >= 400:
        return make_error_response(result.json, result.status_code)
    else:
        return make_response(result.json, result.status_code)
