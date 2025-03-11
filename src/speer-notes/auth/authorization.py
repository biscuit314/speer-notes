"""
The auth module used for HY.
"""
from eve_negotiable_auth import NegotiableAuth, AUTH_PARSER
from flask import g
from . import SETTINGS
from .auth_handlers import basic #, bearer, bearer_challenge

AUTH_PARSER.add_handler('Basic', basic, realm=f'{SETTINGS["AUTH_REALM"]}')
# AUTH_PARSER.add_handler('Bearer', bearer, bearer_challenge, realm=f'{SETTINGS["AUTH_REALM"]}')


class HypermeaAuthorization(NegotiableAuth):
    def __init__(self):
        super(HypermeaAuthorization, self).__init__()

    def authorized(self, allowed_roles, resource, method):
        get_home_allowed = SETTINGS.has_enabled('AUTH_ALLOW_GET_HOME') or SETTINGS.get('HY_GATEWAY_URL', False)
        if get_home_allowed and method == 'GET' and resource is None:
            return True

        return super().authorized(allowed_roles, resource, method)

    def process_claims(self, claims, allowed_roles, resource, method):
        if "username" not in claims:
            return False

        roles = claims.get('roles', [])
        if allowed_roles and not any(role in allowed_roles for role in roles):
            return False

        g.is_admin = False
        if 'admin' not in roles:
            self.set_request_auth_value(claims['username'])
        else:
            g.is_admin = True

        return True
