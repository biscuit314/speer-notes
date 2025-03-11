import pytest
from pytest_bdd import scenario, when, then
from __tests__.authentication import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'User gets a token')
def test_user_gets_a_token():
    pass

# Given a user named alice is signed up

@when(parsers.parse('{username} requests a token'))
def step_impl(api, context, username):
    credentials = {
        'username': username,
        'password': 'password'
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = api.post(
        '/api/auth/login',
        data=json.dumps(credentials),
        headers=headers
    )
    context['response'] = response.json


@then('a token is issued')
def step_impl(context):
    assert_that(context['response']).contains_key('Authorization')
    assert_that(context['response']['Authorization']).starts_with('Basic')