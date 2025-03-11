"""
This module defines functions to add affordances.auth.login.
"""
import hashlib
import base64
import logging
from flask import make_response, request, jsonify
from hypermea.core.utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url, get_db

LOG = logging.getLogger("affordances.auth.login")


def add_affordance(app):
    @app.route("/api/auth/login", methods=["POST"])
    def do_login():
        credentials = request.json
        if 'username' not in credentials or 'password' not in credentials:
            return make_error_response(unauthorized_message, 401)

        user_collection = get_db()['users']
        user = user_collection.find_one({'username': credentials['username']})
        if not user:
            return make_error_response(unauthorized_message, 401)

        to_encrypt = f'{credentials["username"]}:{credentials["password"]}'.encode('utf8')
        if not user['password'] == hashlib.sha256(to_encrypt).hexdigest():
            return make_error_response(unauthorized_message, 401)

        basic_token = base64.b64encode(to_encrypt).decode()
        response = {
            "Authorization": f"Basic {basic_token}"
        }

        return make_response(jsonify(response), 200)
