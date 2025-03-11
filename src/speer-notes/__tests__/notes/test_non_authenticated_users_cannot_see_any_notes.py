import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Non-authenticated users cannot see any note')
def test_non_authenticated_users_cannot_see_any_notes():
    pass

# Given a user is named alice is signed up

# When alice has added notes

@then('no notes are fetched')
def step_impl(context):
    assert_that(context['mallory']['status_code']).is_equal_to(401)
