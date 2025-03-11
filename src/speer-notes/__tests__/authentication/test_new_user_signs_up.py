import pytest
from pytest_bdd import scenario, when, then
from __tests__.authentication import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'New user signs up')
def test_new_user_signs_up():
    pass


@given(parsers.parse('that {username} wants to sign up'))
def step_impl(context, username):
    context['new_username'] = username


@when('an administrator enrolls the new user')
def step_impl(api, context):
    username = context['new_username']
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


@then('the user can start using the system')
def step_impl(api, context):
    response = api.get(
        '/api/notes',
        headers=headers_with_authorization(context['new_username'], 'password')
    )
    assert_that(response.status_code).is_equal_to(200)

