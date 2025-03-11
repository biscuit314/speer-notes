import pytest
from pytest_bdd import scenario, when, then
from __tests__.authentication import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Only admins can sign up a user')
def test_only_admins_can_sign_up_a_user():
    pass


# Given a user named alice is signed up


@when(parsers.parse('{username} enrolls a new user'))
def step_impl(api, context, username):
    new_user = {
        'username': 'carol',
        'name': 'Carol Markus',
        'password': 'password'
    }
    response = api.post(
        '/api/auth/signup',
        data=json.dumps(new_user),
        headers=headers_with_authorization(username, 'password')
    )
    context['response'] = response.status_code


# Then the attempt fails
