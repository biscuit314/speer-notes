import pytest
from pytest_bdd import scenario, when, then
from __tests__.authentication import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'User does not get a token if credentials are incorrect')
def test_user_with_incorrect_credentials_gets_no_token():
    pass

# Given a user named alice is signed up

@when(parsers.parse('{username} requests a token with the wrong password'))
def step_impl(api, context, username):
    credentials = {
        'username': username,
        'password': 'wrong-password'
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = api.post(
        '/api/auth/login',
        data=json.dumps(credentials),
        headers=headers
    )
    context['response'] = response.status_code


@then('a token is not issued')
def step_impl(context):
    assert_that(context['response']).is_equal_to(401)
