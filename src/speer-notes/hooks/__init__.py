import logging
from hypermea.core.hooks import fix_links, tidy_post_links
from hypermea.core.utils import echo_message, is_mongo_running, make_error_response
from hypermea.core.logging import trace
from flask import g
import hooks._gateway
import hooks._error_handlers
import hooks._settings
import hooks._logs
import affordances
from configuration import SETTINGS
import hooks.notes
import hooks.users

LOG = logging.getLogger('hooks')


@trace
def add_hooks(app):
    if not SETTINGS.has_enabled('HY_DISABLE_HYPERMEDIA'):
        app.on_post_GET += fix_links
        app.on_post_PATCH += fix_links
        app.on_post_POST += tidy_post_links
    
    @app.before_request
    def before_request():
        if not is_mongo_running():
            LOG.error('MongoDB is not accessible with current settings.')
            return make_error_response('MongoDB is not running or is not properly configured', 503)

    if not SETTINGS.has_enabled('HY_DISABLE_RFC6861'):
        affordances.rfc6861.create_form.add_affordance(app)
        affordances.rfc6861.edit_form.add_affordance(app)

    if SETTINGS.has_enabled('HY_ADD_ECHO'):
        @app.route('/_echo', methods=['PUT'])
        def _echo_message():
            return echo_message()

    hooks._gateway.add_hooks(app)
    hooks._error_handlers.add_hooks(app)
    hooks._settings.add_hooks(app)
    hooks._logs.add_hooks(app)
    hooks.notes.add_hooks(app)
    hooks.users.add_hooks(app)
    affordances.share.add_affordance(app)

    for method in ['GET', 'PATCH', 'PUT', 'DELETE', 'HEAD']:
        collection_handler = getattr(app, f'on_pre_{method}')
        collection_handler += _restrict_to_owner_or_shared_with
        item_handler = getattr(app, f'on_pre_{method}_item')
        item_handler += _restrict_to_owner_or_shared_with
    affordances.search.add_affordance(app)
    affordances.auth.signup.add_affordance(app)
    affordances.auth.login.add_affordance(app)


@trace
def _restrict_to_owner_or_shared_with(_, request, lookup):
    username = request.authorization.username
    if not g.is_admin:
        lookup['$or'] = [{'_shared_with': {'$in': [username.lower()]}}, {'_owner': username.lower()}]


