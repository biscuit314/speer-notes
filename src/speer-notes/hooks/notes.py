"""
hooks.notes
This module defines functions to add link relations to notes.
"""
import logging
import json
from flask import request as current_request
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.notes')


@trace
def add_hooks(app):
    """Wire up the hooks for notes."""
    if not SETTINGS.has_enabled('HY_DISABLE_HYPERMEDIA'):
        app.on_fetched_item_notes += _add_links_to_note
        app.on_fetched_resource_notes += _add_links_to_notes_collection
        app.on_post_POST_notes += _post_notes

    app.on_pre_PUT_notes += _strip_meta_fields
    app.on_insert_notes += _add_owner_to_note
    app.on_replace_notes += _add_owner_to_replaced_note


@trace
def _strip_meta_fields(request, payload):
    note = request.json

    for key in list(note.keys()):
        if key.startswith('_') and key not in ['_owner', '_shared_with']:
            del note[key]

    request.data = json.dumps(note)


@trace
def _add_owner_to_note(notes):
    username = current_request.authorization.username
    for note in notes:
        note['_owner'] = username


def _add_owner_to_replaced_note(note, xx):
    username = current_request.authorization.username
    note['_owner'] = username


@trace
def _post_notes(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_notes_collection(j, request.url)
        else:
            _add_links_to_note(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_notes_collection(notes_collection, self_href=None):
    for note in notes_collection['_items']:
        _add_links_to_note(note)

    if '_links' not in notes_collection:
        notes_collection['_links'] = {
            'self': {
                'href': self_href
            }
        }

    base_url = get_my_base_url()

    id_field = get_id_field('notes')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    notes_collection['_links']['item'] = {
        'href': f'{base_url}/notes/{{{id_field}}}',
        'title': 'note',
        'templated': True
    }

    self_href = notes_collection['_links']['self']['href']

    if not SETTINGS.has_enabled('HY_DISABLE_RFC6861'):
        affordances.rfc6861.create_form.add_link(notes_collection, 'notes', self_href)


@trace
def _add_links_to_note(note):
    # if '_links' not in note:
    #     return

    base_url = get_my_base_url()
    note_id = get_resource_id(note, 'notes')

    _add_remote_children_links(note)
    _add_remote_parent_links(note)

    note['_links']['self'] = {
        'href': f"{base_url}/notes/{note_id}",
        'title': 'note'
    }
    if not SETTINGS.has_enabled('HY_DISABLE_RFC6861'):
        affordances.rfc6861.edit_form.add_link(note, 'notes')
    affordances.share.add_link(note, 'notes')


@trace
def _add_remote_children_links(note):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    note_id = get_resource_id(note, 'notes')

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links(note):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    note_id = get_resource_id(note, 'notes')

    # == do not edit this method above this line ==
