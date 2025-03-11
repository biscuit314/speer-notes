"""
hooks.users
This module defines functions to add link relations to users.
"""
import logging
import json
import hashlib
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
import affordances

LOG = logging.getLogger('hooks.users')


@trace
def add_hooks(app):
    """Wire up the hooks for users."""
    if not SETTINGS.has_enabled('HY_DISABLE_HYPERMEDIA'):
        app.on_fetched_item_users += _add_links_to_user
        app.on_fetched_resource_users += _add_links_to_users_collection
        app.on_post_POST_users += _post_users

    app.on_insert_users += _encrypt_password


@trace
def _encrypt_password(users):
    for user in users:
        to_encrypt = f"{user['username']}:{user['password']}"
        user['password'] = hashlib.sha256(to_encrypt.encode('utf-8')).hexdigest()


@trace
def _post_users(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_users_collection(j, request.url)
        else:
            _add_links_to_user(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_users_collection(users_collection, self_href=None):
    for user in users_collection['_items']:
        _add_links_to_user(user)

    if '_links' not in users_collection:
        users_collection['_links'] = {
            'self': {
                'href': self_href
            }
        }

    base_url = get_my_base_url()

    id_field = get_id_field('users')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    users_collection['_links']['item'] = {
        'href': f'{base_url}/users/{{{id_field}}}',
        'title': 'user',
        'templated': True
    }
    
    self_href = users_collection['_links']['self']['href']
    if not SETTINGS.has_enabled('HY_DISABLE_RFC6861'):
        affordances.rfc6861.create_form.add_link(users_collection, 'users', self_href)


@trace
def _add_links_to_user(user):
    # if '_links' not in user:
    #     return

    base_url = get_my_base_url()
    user_id = get_resource_id(user, 'users')

    _add_remote_children_links(user)
    _add_remote_parent_links(user)

    user['_links']['self'] = {
        'href': f"{base_url}/users/{user_id}",
        'title': 'user'
    }
    if not SETTINGS.has_enabled('HY_DISABLE_RFC6861'):
        affordances.rfc6861.edit_form.add_link(user, 'users')



@trace
def _add_remote_children_links(user):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    user_id = get_resource_id(user, 'users')

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links(user):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    user_id = get_resource_id(user, 'users')

    # == do not edit this method above this line ==
