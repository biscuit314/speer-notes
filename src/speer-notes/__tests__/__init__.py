import json
import base64
from assertpy import assert_that
from pytest_bdd import parsers, given


ADMIN_CREDENTIALS = ('sysop', 'swordfish')


############################################
#    DELETE ME
def print_json(printable):
    print('\n-----')
    print(json.dumps(printable, indent=2))
    print('-----\n')
############################################



def headers_with_authorization(username, password):
    creds = f'{username}:{password}'
    token = base64.b64encode(creds.encode()).decode()
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {token}'
    }


@given(parsers.parse('a user named {username} is signed up'))
def step_impl(api, username):
    new_user = {
        'username': username,
        'name': username,
        'password': 'password'
    }
    response = api.post(
        '/api/auth/signup',
        data=json.dumps(new_user),
        headers=headers_with_authorization(*ADMIN_CREDENTIALS)
    )
    assert_that(response.status_code).is_equal_to(201)


@given(parsers.parse('someone named {username} who is not signed up'))
def step_impl(username):
    pass
