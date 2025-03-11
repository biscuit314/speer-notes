import pytest
from pytest_bdd import scenario, when, then
from __tests__.authentication import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Only admins can manage user accounts')
def test_only_admins_can_manage_user_accounts():
    pass

# Given a user named alice is signed up

@when(parsers.parse('{username} tries to access user accounts'))
def step_impl(api, context, username):
    response = api.get(
        '/api/users',
        headers=headers_with_authorization(username, 'password')
    )
    context['response'] = response.status_code


# Then the attempt fails
