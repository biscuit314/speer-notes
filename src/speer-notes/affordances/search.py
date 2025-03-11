"""
This module defines functions to add affordances.search.
"""
import logging
import json
from datetime import datetime
from eve.io.mongo import MongoJSONEncoder
from bson import json_util, ObjectId
from flask import make_response, request, jsonify
from hypermea.core.utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url, get_db

LOG = logging.getLogger("affordances.search")


def add_affordance(app):
    @app.route("/api/search", methods=["GET"])
    def do_search_note():
        if app.auth and (not app.auth.authorized(None, "search", "GET")):
            return make_error_response(unauthorized_message, 401)

        username = request.authorization.username
        return _do_search_notes(username, request.args.get('q', ''))

# def add_link(resource, collection_name):
#     base_url = get_my_base_url()
#     resource_id = get_resource_id(resource, collection_name)
#
#     resource['_links']['search'] = {
#         'href': f'{base_url}/{collection_name}/{resource_id}/search',
#         'title': 'PUT to do search'
#     }

def note_encoder(field):
    if type(field) == ObjectId:
        return str(field)
    if type(field) == datetime:
        return field.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    return field.__str__


def _do_search_notes(username, keywords):
    LOG.debug(f'Searching for "{keywords}"')

    notes_collection = get_db()['notes']

    notes = notes_collection.find(
#        {"$text": {"$search": keywords}},
        {
            "$and": [
                {"$text": {"$search": keywords}},
                {
                    "$or": [
                        {"_owner": username.lower()},
                        {"_shared_with": {"$in": [username.lower()]}}
                    ]
                }
            ]
        },
        {
            "title": 1,
            "body": 1,
            "_id": 1,
            "_created": 1,
            "_updated": 1,
            "_etags": 1,
            "_score": {"$meta": "textScore"},
        }
    ).sort([("score", {"$meta": "textScore"})])

    results = []
    for note in notes:
        results.append(note)

    return make_response(json.loads(json.dumps(results, default=note_encoder)), 200)
