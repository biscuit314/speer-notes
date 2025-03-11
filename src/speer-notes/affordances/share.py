"""
This module defines functions to add affordances.share.
"""
import logging

from bson import ObjectId
from flask import make_response, request, g
from hypermea.core.utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url, get_db

LOG = logging.getLogger("affordances.share")


def add_affordance(app):
    @app.route("/api/notes/<note_id>/share", methods=["POST"])
    def do_share_note(note_id):
        if app.auth and (not app.auth.authorized(None, "share", "POST")):
            return make_error_response(unauthorized_message, 401)

        response = None
        username = request.authorization.username
        if not g.is_admin:
            notes_collection = get_db()['notes']
            note = notes_collection.find_one({'_id': ObjectId(note_id)})
            if note and (note['_owner'] == username or username in note.get('_shared_with', [])):
                response =_do_share_note(note_id)
            else:
                response = make_error_response('The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.', 404)

        return response


def add_link(resource, collection_name):
    base_url = get_my_base_url()
    resource_id = get_resource_id(resource, collection_name)

    resource['_links']['share'] = {
        'href': f'{base_url}/{collection_name}/{resource_id}/share',
        'title': 'POST {"username": _username_} to do share this note'
    }

def _do_share_note(note_id):
    username = request.json.get('username')
    if not username:
        return make_error_response('You must specifiy which username to share this note with in the POST body: {"username": _username_}', 400)

    valid_user = get_db()['users'].find_one({'username': username.lower()})
    if not valid_user:
        return make_error_response('Invalid username', 400)

    notes_collection = get_db()['notes']
    note = notes_collection.find_one({'_id': ObjectId(note_id)})
    if not note:
        return make_error_response('The note does not exist', 404)

    shared_with = set(note.get('_shared_with', []))
    shared_with.add(username)

    notes_collection.update_one({'_id': note['_id']}, {'$set': {'_shared_with': list(shared_with)}})

    return make_response('OK', 200)
