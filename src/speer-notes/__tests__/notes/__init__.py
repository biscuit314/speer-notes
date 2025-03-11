from urllib.parse import urlencode
from pytest_bdd import when, then
from __tests__ import *

FEATURE_PATH = 'notes.feature'

@given(parsers.parse('{username} adds notes'))
@when(parsers.parse('{username} adds notes'))
def step_impl(api, datatable, username, context):
    context[username] = {
        'notes_to_add': [],
        'status_codes': [],
        'notes_added': []
    }

    context[username]['notes_to_add'] = []
    context[username]['status_codes'] = []
    context[username]['notes_added'] = []
    for row in datatable[1:]:  # peel off header row
        title, body = row
        note = {
            'title': title,
            'body': body
        }
        context[username]['notes_to_add'].append(note)
        response = api.post(
            '/api/notes',
            data=json.dumps(note),
            headers=headers_with_authorization(username, 'password')
        )
        context[username]['status_codes'].append(response.status_code)
        context[username]['notes_added'].append(response.json)


@when(parsers.parse('{username} requests all notes'))
def step_impl(api, context, username):
    if username not in context:
        context[username] = {}
    response = api.get('/api/notes', headers=headers_with_authorization(username, 'password'))
    context[username]['notes_fetched'] = response.json.get('_items')
    context[username]['status_code'] = response.status_code



@when(parsers.parse('{requesting_username} requests a single note that {posting_username} added'))
def step_impl(api, context, requesting_username, posting_username):
    if requesting_username not in context:
        context[requesting_username] = {}
    single_note_id = context[posting_username]['notes_added'][0]['_id']
    response = api.get(
        f'/api/notes/{single_note_id}',
        headers=headers_with_authorization(requesting_username, 'password')
    )
    context[requesting_username]['request_results'] = {
        'status_code': response.status_code,
        'response_body': response.json
    }


@when(parsers.parse('{requesting_username} updates a single note that {posting_username} added'))
def step_impl(api, context, requesting_username, posting_username):
    if requesting_username not in context:
        context[requesting_username] = {}
    single_note = context[posting_username]['notes_added'][0]

    response = api.get(f'/api/notes/{single_note["_id"]}', headers=headers_with_authorization(posting_username, 'password'))
    replacement_note = response.json
    replacement_note['title'] = 'new title'

    headers = headers_with_authorization(requesting_username, 'password')
    headers['If-Match'] = replacement_note['_etag']

    response = api.put(
        f'/api/notes/{single_note["_id"]}',
        data=json.dumps(replacement_note),
        headers=headers
    )
    context[requesting_username]['request_results'] = {
        'status_code': response.status_code,
        'response_body': response.json
    }


@when(parsers.parse('{requesting_username} deletes a single note that {posting_username} added'))
def step_impl(api, context, requesting_username, posting_username):
    if requesting_username not in context:
        context[requesting_username] = {}
    single_note = context[posting_username]['notes_added'][0]

    headers = headers_with_authorization(requesting_username, 'password')
    headers['If-Match'] = single_note['_etag']

    response = api.delete(
        f'/api/notes/{single_note["_id"]}',
        headers=headers
    )

    if response.status_code != 401:
        headers = headers_with_authorization(posting_username, 'password')
        response = api.get(
            f'/api/notes/{single_note["_id"]}',
            headers=headers
        )

    context[requesting_username]['request_results'] = {
        'status_code': response.status_code,
        'response_body': {}
    }

@when(parsers.parse('{requesting_username} shares a single note with {share_with} that {posting_username} added'))
def step_impl(api, context, requesting_username, share_with, posting_username):
    if requesting_username not in context:
        context[requesting_username] = {}
    single_note = context[posting_username]['notes_added'][0]

    share = {
        'username': share_with
    }

    response = api.post(
        f'/api/notes/{single_note["_id"]}/share',
        data=json.dumps(share),
        headers=headers_with_authorization(requesting_username, 'password')
    )

    context[requesting_username]['request_results'] = {
        'status_code': response.status_code,
        'response_body': response.json,
    }
    context[requesting_username]['shared_note_id'] = single_note['_id']




@then(parsers.parse('the request {username} made results in a {status_code:d}'))
def step_impl(context, username, status_code):
    assert_that(context[username]['request_results']['status_code']).is_equal_to(status_code)



@when(parsers.parse('{username} searches all notes for {keyword}'))
def step_impl(api, context, username, keyword):
    response = api.get(
        f'/api/search?{urlencode({'q': keyword})}',
        headers=headers_with_authorization(username, 'password')
    )
    context['search_results'] = {
        'status_code': response.status_code,
        'results': response.json
    }


@then(parsers.parse('the result is {expected_hits:d} notes are found'))
def step_impl(context, expected_hits):
    hits = 0
    if context['search_results']['status_code'] == 200:
        hits = len(context['search_results']['results'])

    assert_that(hits).is_equal_to(expected_hits)
